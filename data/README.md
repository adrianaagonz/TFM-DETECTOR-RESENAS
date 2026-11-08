# Datos

Los datasets completos **no se suben** al repositorio. Para reproducir el flujo, descarga las fuentes en `data/raw/`:

| Fuente | Dónde | Qué dejar en `data/raw/` |
|---|---|---|
| Deceptive Opinion Spam Corpus v1.4 (Ott et al.) · **principal** | <https://myleott.com/op-spam.html> | Carpeta descomprimida `op_spam_v1.4/` |
| Alternativa CSV del mismo corpus | Kaggle: `rtatman/deceptive-opinion-spam-corpus` | `deceptive-opinion.csv` |
| Fake Reviews Dataset (Salminen et al., 2022) · ampliación | <https://osf.io/tyue9/> (o su espejo en Kaggle) | `fake_reviews_dataset.csv` |

Con al menos una de las dos fuentes, ejecuta desde la raíz del repositorio:

```bash
pip install -r requirements.txt
python src/pipeline.py --sample
```

- `data/raw/manifest.json` registra el hash y el número de filas de cada fichero descargado.
- `data/silver/` y `data/gold/` se generan con el script (ignorados por git).
- `data/sample/gold_sample.csv` es una muestra de hasta 200 filas que sí se versiona.

## Citas

- Ott, M., Choi, Y., Cardie, C., & Hancock, J. T. (2011). *Finding Deceptive Opinion Spam by Any Stretch of the Imagination*. ACL.
- Ott, M., Cardie, C., & Hancock, J. T. (2013). *Negative Deceptive Opinion Spam*. NAACL.
- Salminen, J., Kandpal, C., Kamel, A. M., Jung, S., & Jansen, B. J. (2022). *Creating and detecting fake reviews of online products*. Journal of Retailing and Consumer Services, 64, 102771.
