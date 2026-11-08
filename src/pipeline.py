"""
Pipeline Bronze -> Silver -> Gold para el detector de reseñas manipuladas.

Uso:
    python src/pipeline.py            # ejecuta las tres capas
    python src/pipeline.py --sample   # además guarda data/sample/gold_sample.csv (200 filas)

Fuentes (descargar a mano en data/raw/, ver data/README.md):
  - PRINCIPAL  data/raw/op_spam_v1.4/  o  data/raw/deceptive-opinion.csv
               Deceptive Opinion Spam Corpus (Ott et al., 2011, 2013)
  - AMPLIACIÓN data/raw/fake_reviews_dataset.csv  (Salminen et al., 2022)
Basta con tener una de las dos; el script usa lo que encuentre.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, SILVER, GOLD, SAMPLE = (ROOT / "data" / d for d in ("raw", "silver", "gold", "sample"))
SEED = 42

SALMINEN_FILE = RAW / "fake_reviews_dataset.csv"
OTT_DIR = RAW / "op_spam_v1.4"
OTT_KAGGLE = RAW / "deceptive-opinion.csv"   # versión CSV alternativa del mismo corpus (Kaggle)


# --------------------------------------------------------------------------- utilidades
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_text(t: str) -> str:
    """Normaliza unicode y espacios. Quita espacios antes de signos de puntuación,
    un artefacto de formato que puede delatar el origen del texto (fuga de etiqueta)."""
    t = unicodedata.normalize("NFKC", str(t))
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+([.,!?;:])", r"\1", t)
    return t


# --------------------------------------------------------------------------- BRONZE
def bronze() -> dict[str, pd.DataFrame]:
    """Lee las fuentes tal como llegan, sin transformar, y deja un manifiesto de trazabilidad."""
    out, manifest = {}, {"generado": datetime.now(timezone.utc).isoformat(), "ficheros": []}

    if SALMINEN_FILE.exists():
        df = pd.read_csv(SALMINEN_FILE, dtype=str, keep_default_na=False)
        out["salminen"] = df
        manifest["ficheros"].append({"fuente": "salminen", "ruta": str(SALMINEN_FILE.relative_to(ROOT)),
                                     "sha256": sha256(SALMINEN_FILE), "filas": len(df)})

    if not OTT_DIR.exists() and OTT_KAGGLE.exists():
        k = pd.read_csv(OTT_KAGGLE, dtype=str, keep_default_na=False)
        df = pd.DataFrame({
            "path": "", "polarity": k["polarity"].str.lower() + "_polarity",
            "origin": k["deceptive"].str.lower(), "fold": "",
            "hotel": k["hotel"].str.lower(), "text": k["text"]})
        out["ott"] = df
        manifest["ficheros"].append({"fuente": "ott", "ruta": str(OTT_KAGGLE.relative_to(ROOT)),
                                     "sha256": sha256(OTT_KAGGLE), "filas": len(df)})

    if OTT_DIR.exists():
        rows = []
        for p in sorted(OTT_DIR.rglob("*.txt")):
            parts = [x.lower() for x in p.relative_to(OTT_DIR).parts]
            rows.append({
                "path": "/".join(parts),
                "polarity": next((x for x in parts if x.endswith("_polarity")), ""),
                "origin": next((x for x in parts if x.startswith(("deceptive", "truthful"))), ""),
                "fold": next((x for x in parts if x.startswith("fold")), ""),
                # nombre de fichero tipo d_hilton_1.txt -> hotel = hilton
                "hotel": (m.group(1) if (m := re.match(r"^[dt]_(.+)_\d+\.txt$", parts[-1])) else ""),
                "text": p.read_text(encoding="utf-8", errors="replace"),
            })
        df = pd.DataFrame(rows)
        out["ott"] = df
        manifest["ficheros"].append({"fuente": "ott", "ruta": str(OTT_DIR.relative_to(ROOT)),
                                     "ficheros_txt": len(df)})

    if not out:
        sys.exit("No hay datos en data/raw/. Sigue las instrucciones de data/README.md.")

    (RAW / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    for k, v in out.items():
        print(f"[bronze] {k}: {len(v):,} filas")
    return out


# --------------------------------------------------------------------------- SILVER
def silver(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Esquema común, tipos, nulos, duplicados y etiquetas homogéneas."""
    frames = []

    if "salminen" in raw:
        s = raw["salminen"].rename(columns={"text_": "text"})
        frames.append(pd.DataFrame({
            "source": "salminen_amazon",
            "domain": s["category"].str.replace(r"_5$", "", regex=True),
            "text": s["text"],
            "rating": pd.to_numeric(s["rating"], errors="coerce"),
            # CG = computer-generated (falsa), OR = original
            "is_fake": s["label"].str.strip().str.upper().map({"CG": 1, "OR": 0}),
            "fake_type": np.where(s["label"].str.strip().str.upper() == "CG", "generada_por_maquina", "ninguno"),
            "polarity": pd.NA,
            "hotel": pd.NA,
            "fold": pd.NA,
        }))

    if "ott" in raw:
        o = raw["ott"]
        frames.append(pd.DataFrame({
            "source": "ott_hotels",
            "domain": "hotels",
            "text": o["text"],
            "rating": np.nan,  # el corpus no trae puntuación
            "is_fake": o["origin"].str.startswith("deceptive").astype(int),
            "fake_type": np.where(o["origin"].str.startswith("deceptive"), "escrita_por_humano_pagado", "ninguno"),
            "polarity": o["polarity"].str.replace("_polarity", "", regex=False),
            "hotel": o["hotel"].replace("", pd.NA),
            "fold": o["fold"].replace("", pd.NA),
        }))

    df = pd.concat(frames, ignore_index=True)
    n0 = len(df)

    df["text"] = df["text"].map(normalize_text)
    df = df[df["text"].str.split().str.len() >= 3]                 # vacíos o casi vacíos
    df = df.dropna(subset=["is_fake"])                             # etiqueta desconocida
    df["is_fake"] = df["is_fake"].astype(int)
    df.loc[~df["rating"].between(1, 5), "rating"] = np.nan          # puntuación fuera de rango
    df["text_key"] = df["text"].str.lower()
    conflict = df.groupby("text_key")["is_fake"].transform("nunique") > 1
    n_conflict = int(conflict.sum())
    df = df[~conflict]                                             # mismo texto con etiquetas distintas
    df = df.drop_duplicates(subset="text_key").drop(columns="text_key")

    df.insert(0, "review_id", [hashlib.md5(f"{s}|{t}".encode()).hexdigest()[:16]
                               for s, t in zip(df["source"], df["text"])])
    SILVER.mkdir(parents=True, exist_ok=True)
    df.to_csv(SILVER / "reviews_silver.csv", index=False)
    print(f"[silver] {n0:,} -> {len(df):,} filas (conflictos de etiqueta eliminados: {n_conflict})")
    return df


# --------------------------------------------------------------------------- GOLD
FIRST_PERSON = re.compile(r"\b(i|me|my|mine|we|our|us)\b", re.I)
# Léxicos mínimos e interpretables. Miden SEÑALES LINGÜÍSTICAS, no emociones reales del autor.
POSITIVE = re.compile(r"\b(great|amazing|excellent|perfect|love|loved|awesome|fantastic|wonderful|beautiful|comfortable)\b", re.I)
NEGATIVE = re.compile(r"\b(bad|terrible|awful|horrible|worst|dirty|rude|disappointed|disappointing|poor|never)\b", re.I)
SUPERLATIVE = re.compile(r"\b(best|worst|most|least|\w{3,}est)\b", re.I)


def gold(df: pd.DataFrame) -> pd.DataFrame:
    """Una fila = una reseña con su etiqueta, señales lingüísticas simples y partición."""
    g = df.copy()
    words = g["text"].str.split()
    g["n_chars"] = g["text"].str.len()
    g["n_words"] = words.str.len()
    g["avg_word_len"] = (g["n_chars"] / g["n_words"]).round(3)
    g["exclam_ratio"] = (g["text"].str.count("!") / g["n_words"]).round(4)
    g["upper_ratio"] = (g["text"].str.count(r"[A-Z]") / g["n_chars"]).round(4)
    g["first_person_ratio"] = (g["text"].str.count(FIRST_PERSON) / g["n_words"]).round(4)
    g["positive_word_ratio"] = (g["text"].str.count(POSITIVE) / g["n_words"]).round(4)
    g["negative_word_ratio"] = (g["text"].str.count(NEGATIVE) / g["n_words"]).round(4)
    g["superlative_ratio"] = (g["text"].str.count(SUPERLATIVE) / g["n_words"]).round(4)
    g["affect_polarization"] = (g["positive_word_ratio"] - g["negative_word_ratio"]).abs().round(4)
    g["type_token_ratio"] = (words.map(lambda w: len(set(x.lower() for x in w))) / g["n_words"]).round(4)

    # Partición. Ott trae 5 folds originales: fold1-3 train, fold4 val, fold5 test.
    # Resto (o Ott en CSV sin folds): estratificada por fuente y etiqueta, 70 / 15 / 15.
    rng = np.random.default_rng(SEED)
    g["split"] = "train"
    has_fold = g["fold"].notna()
    g.loc[g["fold"] == "fold4", "split"] = "val"
    g.loc[g["fold"] == "fold5", "split"] = "test"
    for _, idx in g[~has_fold].groupby(["source", "is_fake"]).groups.items():
        idx = rng.permutation(np.asarray(idx))
        n = len(idx)
        g.loc[idx[int(n * .70):int(n * .85)], "split"] = "val"
        g.loc[idx[int(n * .85):], "split"] = "test"

    cols = ["review_id", "source", "domain", "hotel", "polarity", "text", "rating", "is_fake", "fake_type",
            "n_chars", "n_words", "avg_word_len", "exclam_ratio", "upper_ratio", "first_person_ratio",
            "positive_word_ratio", "negative_word_ratio", "superlative_ratio", "affect_polarization",
            "type_token_ratio", "split"]
    g = g[cols]
    GOLD.mkdir(parents=True, exist_ok=True)
    g.to_csv(GOLD / "reviews_gold.csv", index=False)

    print(f"[gold] {len(g):,} filas, {g.shape[1]} columnas")
    print(pd.crosstab([g["source"], g["split"]], g["is_fake"], margins=True).to_string())
    return g


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true", help="guarda una muestra de 200 filas en data/sample/")
    args = ap.parse_args()
    g = gold(silver(bronze()))
    if args.sample:
        SAMPLE.mkdir(parents=True, exist_ok=True)
        groups = g.groupby(["source", "is_fake"])
        per_group = max(1, 200 // groups.ngroups)
        pd.concat(x.sample(min(len(x), per_group), random_state=SEED) for _, x in groups
                  ).to_csv(SAMPLE / "gold_sample.csv", index=False)
        print(f"[sample] data/sample/gold_sample.csv")


if __name__ == "__main__":
    main()
