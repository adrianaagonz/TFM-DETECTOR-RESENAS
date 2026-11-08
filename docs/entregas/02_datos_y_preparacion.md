# Entrega 2 · Datos y preparación

**Proyecto:** Detector de Reseñas Manipuladas
**Autora:** Adriana González Atencia

## 0. Idea elegida y pregunta que deben responder los datos

De las tres ideas de la entrega 1 se continúa con la **idea 3**, porque es la única en la que problema, datos y variable objetivo encajan sin supuestos adicionales:

- La **idea 2** necesitaría unir cada devolución con la táctica de marketing que originó la compra. Online Retail II solo registra pedidos y cancelaciones, sin campaña ni táctica, así que esa unión no existe en los datos disponibles.
- La **idea 1** necesitaría una etiqueta de "impacto emocional real" en el lector, que no se puede obtener solo a partir del texto.

**Pregunta concreta:** dado el texto de una reseña, ¿qué probabilidad hay de que sea engañosa (escrita sin experiencia real y con intención de parecer auténtica), y qué señales lingüísticas pesan más en esa estimación?

**Variable objetivo:** `is_fake` (1 = engañosa, 0 = veraz), que viene ya etiquetada en las fuentes.

**Nota de prudencia:** cuando este proyecto habla de "lenguaje emocional" se refiere a **marcadores lingüísticos medibles** (palabras de afecto positivo o negativo, superlativos, exclamaciones, primera persona). No se afirma nada sobre la emoción real ni la intención del autor. El modelo detecta patrones asociados estadísticamente a reseñas engañosas en corpus etiquetados.

## 1. Qué datos necesita el producto

- **Observación:** una reseña escrita por una persona (o generada) sobre un producto o establecimiento.
- **Imprescindible:**
  - el texto completo de la reseña;
  - una etiqueta fiable de veraz o engañosa para entrenar y evaluar.
- **Deseable:**
  - la puntuación (estrellas), para medir la incoherencia entre texto y nota;
  - la polaridad (reseña positiva o negativa), para que el modelo no confunda "negativa" con "falsa";
  - la entidad reseñada (hotel o categoría de producto), para no mezclar entidades entre entrenamiento y test;
  - metadatos del revisor (historial, fecha), que en una plataforma real ayudarían mucho, pero que los corpus etiquetados públicos no traen.
- **Granularidad e histórico:** una fila por reseña. No hace falta serie temporal, porque el problema es de clasificación de texto. Con unos miles de reseñas etiquetadas basta para un modelo base y para comparar con la literatura.

## 2. Fuentes reales y viabilidad

| Fuente | Rol | Contenido | Acceso |
|---|---|---|---|
| **Deceptive Opinion Spam Corpus v1.4** (Ott et al., 2011; Ott, Cardie y Hancock, 2013) | Principal | 1.600 reseñas de los 20 hoteles más populares de Chicago: 800 veraces (TripAdvisor y otras webs de reservas) y 800 engañosas escritas por trabajadores de Amazon Mechanical Turk. Equilibrado por polaridad (400 por combinación). Viene dividido en 5 *folds*. | Descarga directa en <https://myleott.com/op-spam.html> (zip con un `.txt` por reseña) o versión CSV en Kaggle (`rtatman/deceptive-opinion-spam-corpus`). |
| **Fake Reviews Dataset** (Salminen et al., 2022) | Ampliación | ~40.000 reseñas de Amazon en 10 categorías: la mitad originales (`OR`) y la mitad generadas por un modelo de lenguaje (`CG`). | OSF (<https://osf.io/tyue9/>) y espejo en Kaggle. Un único CSV. |

- **Cobertura:** Ott cubre hostelería y engaño humano. Salminen cubre e-commerce y texto generado por máquina. Juntas representan los dos tipos de manipulación que interesan al producto, y la columna `fake_type` los mantiene separados.
- **Actualización y estabilidad:** las dos son corpus académicos estáticos y versionados, por lo que no cambian con el tiempo. Eso garantiza reproducibilidad, pero no captura reseñas falsas actuales (por ejemplo, las generadas con modelos de lenguaje recientes).
- **Alternativa si una fuente cae:**
  - Ott tiene dos vías de descarga, su web y Kaggle, y el script acepta las dos.
  - Si fallaran ambas, YelpChi (reseñas filtradas por el sistema de Yelp, Rayana y Akoglu, 2015) sería la sustituta, aunque sus etiquetas son las del filtro de Yelp y no una verdad confirmada.
  - Para aplicar el modelo a reseñas reales sin etiqueta se pueden usar Amazon Reviews 2023 (McAuley Lab) o el Yelp Open Dataset.

## 3. Uso, privacidad y datos personales

- **Licencias:**
  - El corpus de Ott se distribuye con licencia Creative Commons BY-NC-SA 3.0, que permite el uso académico no comercial con atribución.
  - El dataset de Salminen es de uso académico con cita al artículo. Su licencia concreta se comprobará en la página de OSF antes de incluir cualquier muestra en el repositorio.
  - Un producto comercial necesitaría reentrenarse con datos propios o con licencia compatible.
- **Datos personales:** ninguna de las dos fuentes incluye identificadores de usuario, nombres ni fechas. Solo hay texto, etiqueta, polaridad o puntuación y entidad.
- **Minimización:**
  - No se recogen nombres de usuario ni perfiles, porque no son necesarios para responder la pregunta.
  - Si en una fase posterior se usaran reseñas reales de Amazon o Yelp, se descartaría `user_id` o se sustituiría por un hash, y se eliminaría cualquier nombre propio de persona que aparezca en el texto.
- **Repositorio:** no se suben los datasets completos. Solo se incluyen el script, las instrucciones de descarga (`data/README.md`) y una muestra pequeña de la capa Gold (`data/sample/gold_sample.csv`, 200 filas) con atribución a las fuentes.

## 4. Del dato bruto al dato utilizable

Todo el flujo está en `src/pipeline.py` y se ejecuta con `python src/pipeline.py --sample`.

```
data/raw/      (Bronze)  ficheros originales + manifest.json (ruta, sha256, nº de filas)
     │
     ▼  esquema común, limpieza, etiquetas homogéneas, deduplicación
data/silver/reviews_silver.csv
     │
     ▼  señales lingüísticas + partición train / val / test
data/gold/reviews_gold.csv   →   entrada de la fase de Machine Learning
```

### Bronze / Raw

- Los ficheros se guardan tal como se descargan:
  - `op_spam_v1.4/` con su estructura de carpetas `polaridad/origen/fold/*.txt`;
  - o `deceptive-opinion.csv`;
  - y `fake_reviews_dataset.csv`.
- El script no modifica nada en esta capa. Lee los ficheros y escribe `data/raw/manifest.json`, con la fecha, el hash SHA-256 y el número de filas de cada fuente, para poder comprobar que se trabaja siempre sobre el mismo dato.
- En el corpus de Ott, la etiqueta, la polaridad, el fold y el hotel salen de la propia ruta de cada fichero. Por ejemplo, `positive_polarity/deceptive_from_MTurk/fold1/d_hilton_1.txt` es una reseña positiva, engañosa, del fold 1 y del hotel Hilton.

### Silver

| Transformación | Motivo |
|---|---|
| Esquema común: `source, domain, hotel, polarity, text, rating, is_fake, fake_type, fold` | Las dos fuentes tienen formatos distintos (ficheros sueltos frente a CSV). |
| Etiquetas: `deceptive → 1`, `truthful → 0`, `CG → 1`, `OR → 0` | Una única variable objetivo, `is_fake`. |
| `fake_type`: `escrita_por_humano_pagado` / `generada_por_maquina` / `ninguno` | No mezclar dos fenómenos distintos sin poder separarlos después. |
| Normalización Unicode (NFKC), espacios múltiples y espacios antes de signos de puntuación | Evitar que diferencias de formato entre fuentes o clases actúen como "pista" (fuga de etiqueta). |
| `rating` a número, con valores fuera de 1–5 puestos como nulos | Tipos correctos. Ott no trae puntuación, así que es nula en esa fuente. |
| Eliminar textos de menos de 3 palabras y filas sin etiqueta | Registros no utilizables. |
| Eliminar textos idénticos con etiquetas contradictorias y deduplicar por texto | Evitar ruido y que una misma reseña aparezca en train y en test. |
| `review_id` = hash de fuente + texto | Identificador estable y reproducible. |

### Gold

Archivo `data/gold/reviews_gold.csv`: **una fila es una reseña única, etiquetada y lista para modelar.**

| Columna | Significado | Uso |
|---|---|---|
| `review_id` | Identificador estable | Trazabilidad |
| `source`, `domain`, `hotel`, `polarity` | Origen y contexto | Estratificación, análisis de sesgos, partición por entidad |
| `text` | Texto limpio | Entrada de los modelos de texto (TF-IDF, embeddings, transformer) |
| `rating` | Estrellas (solo Salminen) | Incoherencia entre texto y nota |
| `is_fake` | **Variable objetivo** | Entrenamiento y evaluación |
| `fake_type` | Tipo de engaño | Evaluar el modelo por separado en cada fenómeno |
| `n_chars`, `n_words`, `avg_word_len`, `type_token_ratio` | Longitud y riqueza léxica | Modelo base interpretable |
| `exclam_ratio`, `upper_ratio`, `first_person_ratio` | Estilo | Hipótesis de la literatura (más primera persona y énfasis en reseñas engañosas) |
| `positive_word_ratio`, `negative_word_ratio`, `superlative_ratio`, `affect_polarization` | Marcadores léxicos de afecto | Contrastar la hipótesis de la entrega 1 sobre el lenguaje emocional extremo |
| `split` | `train` / `val` / `test` | Si se usa el zip original de Ott, se respetan sus folds (1–3 train, 4 val, 5 test). Con la versión CSV, o con Salminen, partición estratificada 70/15/15 con semilla 42. |

Los léxicos de afecto del script son listas cortas e interpretables, pensadas como primera aproximación. En la fase de modelado se pueden sustituir por un léxico validado (por ejemplo, NRC Emotion Lexicon o LIWC) sin cambiar el resto del flujo.

### Resultado de la ejecución con datos reales

Ejecución de `python src/pipeline.py --sample` sobre `deceptive-opinion.csv`, la versión CSV de Kaggle del corpus de Ott (SHA-256 `e98f9f94…71e3a77`, registrado en `manifest.json`):

```
[bronze] ott: 1,600 filas
[silver] 1,600 -> 1,596 filas (conflictos de etiqueta eliminados: 0)
[gold] 1,596 filas, 21 columnas
is_fake             0    1   All
source     split
ott_hotels test   120  120   240
           train  557  560  1117
           val    119  120   239
All               796  800  1596
[sample] data/sample/gold_sample.csv
```

- **Silver** elimina 4 reseñas veraces duplicadas. No hay nulos en el texto ni etiquetas contradictorias. La columna `rating` queda vacía, porque el corpus no trae puntuación.
- **Gold** tiene 1.596 reseñas de 20 hoteles, con las clases equilibradas (796 veraces y 800 engañosas). La versión CSV no trae los folds originales, así que se aplica la partición estratificada 70/15/15. La columna `hotel` permite repetir la partición agrupando por hotel en la fase de modelado, para comprobar que el modelo generaliza a hoteles que no ha visto.
- `data/sample/gold_sample.csv` contiene 200 filas (100 por clase).

### Primera comprobación: ¿los datos responden a la pregunta?

Media de algunas señales de la capa Gold por polaridad y clase:

| Señal | Negativas veraces | Negativas engañosas | Positivas veraces | Positivas engañosas |
|---|---|---|---|---|
| `n_words` | 178,6 | 177,5 | 123,0 | 115,7 |
| `first_person_ratio` | 0,054 | **0,070** | 0,048 | **0,066** |
| `exclam_ratio` | 0,006 | 0,005 | 0,008 | 0,012 |
| `superlative_ratio` | 0,003 | 0,003 | 0,003 | 0,005 |
| `affect_polarization` | 0,008 | 0,009 | 0,023 | 0,023 |
| `type_token_ratio` | 0,677 | 0,663 | 0,726 | 0,709 |

- La etiqueta existe, está equilibrada y hay diferencias medibles entre clases. La más clara es el **mayor uso de la primera persona** en las reseñas engañosas, que coincide con lo que describen Ott et al. (2011).
- En cambio, con este léxico básico **la polarización afectiva es prácticamente igual** en las dos clases. La hipótesis de la entrega 1 ("el lenguaje emocional extremo delata la reseña falsa") no se confirma con estas señales simples. La fase de modelado la contrastará con un léxico validado y con modelos de texto completos, sin darla por supuesta.

## 5. Riesgos y limitaciones

- **Dato que falta:** metadatos del revisor (historial, ráfagas temporales, compra verificada). En plataformas reales son señales muy fuertes, pero los corpus etiquetados no los incluyen.
- **Sesgos:**
  - Las reseñas engañosas de Ott las escribieron trabajadores pagados en un encargo controlado, y las de Salminen las generó GPT-2. Ninguna representa del todo a un manipulador real actual.
  - Ambos corpus están en inglés, y Ott se limita a 20 hoteles de Chicago, así que generalizar a otros sectores o al español exige validación adicional.
  - Las etiquetas indican cómo se produjo el texto, no la intención de su autor.
- **Si cae una fuente:** Ott tiene dos vías de descarga y el script acepta ambas. Salminen es solo una ampliación, y el proyecto puede seguir sin ella. Como última alternativa, YelpChi, sabiendo que sus etiquetas son menos fiables.

## Nota: encaje con proyectos afines

Antonio Rodríguez y Álvaro García trabajan también sobre reseñas: la priorización y respuesta, y la clasificación de sentimiento y problemas recurrentes. Esta capa Gold usa un esquema mínimo (`review_id`, `text`, `rating`, `domain`) que sus módulos también podrían consumir. Si se decide colaborar, el detector de manipulación podría actuar como filtro previo: descartar o marcar las reseñas sospechosas antes de analizar sentimiento o priorizar respuestas.
