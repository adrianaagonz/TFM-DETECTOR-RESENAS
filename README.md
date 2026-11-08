# Detector de Reseñas Manipuladas

**Proyecto final · Máster en Data Science & IA**
Adriana González Atencia · Tutor: Julio Valero

Modelo de NLP que estima la probabilidad de que una reseña online sea engañosa y explica qué señales lingüísticas pesan más en esa estimación.

---

## El problema

Las reseñas falsas, tanto las escritas por personas pagadas como las generadas con IA, distorsionan la prueba social en la que confían los consumidores. También perjudican a los negocios legítimos y exponen a las empresas a sanciones: la FTC en EE. UU. y la normativa europea de consumo prohíben las reseñas fraudulentas. Las pymes de comercio electrónico y hostelería, y las plataformas de reputación online, no tienen herramientas accesibles para detectarlas.

## Pregunta y variable objetivo

> Dado el texto de una reseña, ¿qué probabilidad hay de que sea engañosa y qué señales lingüísticas lo explican?

- **Variable objetivo:** `is_fake` (1 = engañosa, 0 = veraz).
- **Tipo de problema:** clasificación binaria de texto, con interpretabilidad.
- **Nota de prudencia:** el modelo mide *marcadores lingüísticos* (léxico de afecto, superlativos, primera persona, exclamaciones). No mide la emoción real ni la intención del autor.

## Datos

| Fuente | Rol | Contenido |
|---|---|---|
| [Deceptive Opinion Spam Corpus](https://myleott.com/op-spam.html) (Ott et al., 2011, 2013) | Principal | 1.600 reseñas de hoteles de Chicago: 800 veraces y 800 engañosas escritas por personas, equilibradas por polaridad. |
| [Fake Reviews Dataset](https://osf.io/tyue9/) (Salminen et al., 2022) | Ampliación | ~40.000 reseñas de Amazon: la mitad originales y la mitad generadas por IA. |

Los datasets completos no se suben al repositorio. Las instrucciones de descarga están en [`data/README.md`](data/README.md).

## Flujo de datos (Bronze → Silver → Gold)

| Capa | Qué hace | Salida |
|---|---|---|
| **Bronze** | Lee las fuentes tal como llegan y registra hash y número de filas. | `data/raw/` + `manifest.json` |
| **Silver** | Esquema común, etiquetas homogéneas, normalización de texto, nulos y duplicados. | `data/silver/reviews_silver.csv` |
| **Gold** | Una fila por reseña, con señales lingüísticas y partición train/val/test. | `data/gold/reviews_gold.csv` |

El detalle de cada transformación y el diccionario de columnas está en la [entrega 2](docs/entregas/02_datos_y_preparacion.md).

## Estado del proyecto

| Entrega | Contenido | Estado |
|---|---|---|
| 1 · [Ideas de producto](docs/entregas/01_ideas_producto.md) | Tres ideas iniciales y elección de la idea 3 | ✅ |
| 2 · [Datos y preparación](docs/entregas/02_datos_y_preparacion.md) | Fuentes, privacidad y flujo Bronze → Silver → Gold | ✅ |
| 3 · Modelado | Modelo base interpretable (TF-IDF + regresión logística) frente a embeddings o transformer | Próximamente |

## Estructura del repositorio

```
docs/entregas/          Documentos de cada entrega
src/pipeline.py         Script reproducible Bronze → Silver → Gold
data/README.md          Descarga de fuentes y citas
data/sample/            Muestra pequeña de la capa Gold
requirements.txt        Dependencias
```

## Cómo reproducirlo

```bash
pip install -r requirements.txt
# 1. Descarga las fuentes en data/raw/ (ver data/README.md)
# 2. Ejecuta el flujo completo y genera una muestra
python src/pipeline.py --sample
```

## Limitaciones

- Los corpus etiquetados están en inglés y son de dominios concretos (hoteles de Chicago y productos de Amazon).
- Las reseñas engañosas de los corpus se escribieron por encargo o se generaron con GPT-2, así que no representan del todo la manipulación actual.
- No hay metadatos del revisor (historial, fechas), que en plataformas reales son señales muy útiles.

## Trabajo relacionado

Este detector puede complementar otros proyectos del máster sobre análisis de reseñas, como la clasificación de sentimiento o la priorización de respuestas. Actuaría como filtro previo que marca las reseñas sospechosas antes de analizarlas.
