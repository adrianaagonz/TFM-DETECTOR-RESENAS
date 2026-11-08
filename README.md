# Detector de Reseñas Manipuladas

Proyecto final del Máster en Data Science & IA · Adriana González Atencia

Modelo que estima la probabilidad de que una reseña sea engañosa a partir de señales lingüísticas medibles, y explica qué señales pesan más.

## Estructura

```
docs/entregas/
  01_ideas_producto.md        Entrega 1: tres ideas iniciales
  02_datos_y_preparacion.md   Entrega 2: datos, fuentes y flujo Bronze → Silver → Gold
src/pipeline.py               Script reproducible Bronze → Silver → Gold
data/README.md                Instrucciones de descarga y citas
data/sample/                  Muestra pequeña de la capa Gold
```

## Reproducir

```bash
pip install -r requirements.txt
# descarga las fuentes en data/raw/ (ver data/README.md)
python src/pipeline.py --sample
```
