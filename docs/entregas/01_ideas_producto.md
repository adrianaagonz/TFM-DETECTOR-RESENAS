# Entrega 1 · Propuesta inicial de ideas de producto

**Autora:** Adriana González Atencia
**Máster en Data Science & IA**

> Este fichero recoge en formato repositorio el contenido de la entrega 1, que en su momento se presentó como PDF. El texto de las tres ideas se mantiene como se entregó. Al final se añade una nota posterior con el feedback recibido y la decisión que se toma para la entrega 2.

## Introducción y contexto estratégico

Las tres propuestas comparten un hilo conductor: la intersección entre el marketing estratégico, el análisis de datos y la inteligencia artificial, con un fuerte anclaje en el neuromarketing (la psicología del consumidor aplicada a decisiones comerciales reales). El proyecto aborda tres momentos consecutivos del embudo y del comportamiento de compra:

1. **Antes de comprar:** la persuasión mediante el diseño del lenguaje y la auditoría emocional de los copys.
2. **Durante la decisión de compra:** los sesgos psicológicos que empujan a la conversión y su impacto secundario (la tasa de devolución).
3. **Después de la compra:** la validación social y la detección computacional de la manipulación en las opiniones de los usuarios.

Cada propuesta cuenta con una base teórica sólida y con datasets públicos verificados para su viabilidad técnica.

---

## Idea 1 · Neuroíndice de Persuasión: auditoría emocional y psicológica de textos de venta con IA

### Problema que resuelve

- **Qué ocurre actualmente:** la proliferación masiva de contenido de marketing generado mediante modelos de lenguaje (anuncios, copys, correos electrónicos) provoca que muchos negocios publiquen textos sin verificar si aplican principios de persuasión con respaldo psicológico, ni qué impacto emocional real generan en el lector.
- **Por qué supone un problema:** un texto puede utilizar correctamente una técnica de persuasión (como la escasez), pero desencadenar una activación emocional negativa o de urgencia agresiva. Esto puede generar conversiones a corto plazo, pero erosiona el valor de la marca a largo plazo. Actualmente, los negocios carecen de herramientas automatizadas para auditar esta combinación antes de publicar.
- **Qué decisión, proceso o situación podría mejorar con datos:** un modelo analítico capaz de procesar un texto, identificar los principios de persuasión utilizados (por ejemplo, los seis principios de Cialdini) y predecir su nivel de activación emocional y valencia. Esto aporta a los equipos de marketing un diagnóstico objetivo de neuromarketing digital.
- **Por qué no es simplemente un ejercicio técnico:** traduce un marco teórico validado en la psicología del consumidor en una solución accesible para empresas que no disponen de presupuesto para agencias o estudios tradicionales de laboratorio (como EEG o eye-tracking).

### Motivación para realizar el proyecto

- **Relevancia:** conecta de forma directa con el interés profesional en el neuromarketing y la experiencia del consumidor.
- **Utilidad potencial para un colectivo concreto:** ofrece una solución directa para pymes, copywriters y creadores de contenido que necesitan optimizar sus textos sin depender de costosos estudios de laboratorio.
- **Posibilidad de aplicar contenidos del máster:** técnicas de Procesamiento del Lenguaje Natural (NLP), análisis de sentimiento basado en aspectos y clasificación de texto.
- **Existencia de datos:** datasets públicos como SemEval-2023 (Task 3), PersuasionForGood, el Pitt Ads Dataset y normas psicolingüísticas de emoción por palabra.

### A quién impacta

- Pymes y emprendedores sin recursos para contratar agencias especializadas.
- Freelancers de marketing, copywriters y creadores de contenido digital.
- Agencias de marketing que necesiten un control de calidad ético y emocional sobre los textos generados mediante IA.

### Por qué tiene valor

- **Mejor toma de decisiones y control de riesgos:** diagnóstico preventivo que evita campañas con impacto reputacional negativo.
- **Automatización y escalabilidad:** permite industrializar auditorías de contenido de forma rápida para múltiples canales.

---

## Idea 2 · Gatillos de Compra Impulsiva: qué tácticas de marketing generan ventas que acaban en devolución

### Problema que resuelve

- **Qué ocurre actualmente:** gran parte de las compras impulsivas en el comercio electrónico son inducidas por tácticas que explotan sesgos cognitivos (urgencia artificial, escasez, FOMO). Estas mismas transacciones son las que experimentan mayores tasas de devolución cuando el impulso desaparece, agravado por prácticas como el *bracketing* (comprar varias variantes para quedarse con una).
- **Por qué supone un problema:** los equipos de marketing evalúan sus campañas por ventas brutas a corto plazo, ignorando el coste logístico y operativo de las devoluciones, lo que distorsiona la rentabilidad real de las acciones comerciales.
- **Qué decisión, proceso o situación podría mejorar con datos:** cruzar el tipo de comunicación o campaña promocional de un pedido con su probabilidad histórica de devolución, generando un indicador de sostenibilidad comercial.
- **Por qué no es simplemente un ejercicio técnico:** aborda un problema tradicionalmente confinado a la logística o la prevención de fraude desde la perspectiva del comportamiento del consumidor y la estrategia comercial.

### Motivación para realizar el proyecto

- **Relevancia:** reorienta una métrica financiera y logística hacia el análisis del comportamiento del consumidor.
- **Utilidad potencial para un colectivo concreto:** directores de marketing y gestores de comercio electrónico (especialmente en moda).
- **Posibilidad de aplicar contenidos del máster:** clasificación supervisada, ingeniería de características e IA tabular.
- **Existencia de datos:** repositorio público Online Retail / Online Retail II del UCI Machine Learning Repository.

### A quién impacta

- Directores de marketing y gestores de comercio electrónico en sectores con alta devolución (como la moda).
- Empresas interesadas en optimizar el ROI neto de devoluciones de sus campañas.

### Por qué tiene valor

- **Eficiencia de costes y planificación:** identificar y frenar tácticas que inflan la conversión inicial a costa de márgenes negativos por logística inversa.
- **Generación de conocimiento estratégico:** alinea los objetivos de marketing con la rentabilidad a largo plazo.

---

## Idea 3 · Detector de Reseñas Manipuladas: cómo el lenguaje emocional delata una opinión falsa

### Problema que resuelve

- **Qué ocurre actualmente:** la proliferación de reseñas falsas o generadas artificialmente en plataformas de comercio y hostelería dificulta que los consumidores identifiquen valoraciones auténticas. A nivel regulatorio, agencias como la FTC en EE. UU. sancionan el uso comercial de reseñas fraudulentas.
- **Por qué supone un problema:** la investigación en lingüística computacional indica que las reseñas falsas no son neutras: tienden a mostrar un sesgo emocional más extremo, un uso excesivo de superlativos y una mayor polarización afectiva para compensar su falta de autenticidad.
- **Qué decisión, proceso o situación podría mejorar con datos:** un modelo predictivo que analice patrones lingüísticos y anomalías emocionales en un corpus de reseñas para estimar su autenticidad y los factores que delatan manipulación.
- **Por qué no es simplemente un ejercicio técnico:** responde a una exigencia de cumplimiento normativo y a un problema de confianza y transparencia para los consumidores.

### Motivación para realizar el proyecto

- **Relevancia:** conecta con la actualidad regulatoria y la protección de la reputación de los negocios legítimos.
- **Utilidad potencial para un colectivo concreto:** pymes de comercio electrónico y hostelería, y consumidores particulares.
- **Posibilidad de aplicar contenidos del máster:** detección de anomalías textuales, embeddings y clasificación con modelos de lenguaje.
- **Existencia de datos:** Deceptive Opinion Spam Corpus (Ott et al.).

### A quién impacta

- Pymes de comercio electrónico y hostelería que dependen de su reputación digital.
- Consumidores que buscan apoyo para decisiones informadas.
- Plataformas de gestión de reputación online.

### Por qué tiene valor

- **Reducción de riesgos legales:** protege frente a sanciones derivadas de malas prácticas en la gestión de valoraciones.
- **Protección del consumidor:** aporta rigor analítico a la validación de la prueba social.

---

## Criterios de evaluación y coherencia de las propuestas

| Criterio | Cumplimiento de las propuestas |
|---|---|
| Claridad del problema | Cada idea define un reto comercial real y actual vinculado al comportamiento del consumidor. |
| Motivación de la idea | Se justifica su relevancia por la unión entre estrategia de marketing, neuromarketing y analítica avanzada. |
| Identificación del público | Se segmenta a pymes, equipos de marketing y consumidores finales. |
| Adecuación técnica | Todas son viables en un máster de Data Science e IA con datasets públicos. |

---

## Nota posterior (tras el feedback de la entrega 1)

Feedback del tutor y cómo se incorpora:

- **Idea 1:** a partir del texto solo se pueden medir o clasificar *señales lingüísticas* (léxico emocional, marcadores de persuasión), no el efecto psicológico real en el lector. Si se retomara, se hablaría de "perfil lingüístico emocional" y no de "impacto emocional real", y cualquier relación con el efecto en personas tendría que validarse con datos de respuesta (por ejemplo, clics o encuestas).
- **Idea 2:** Online Retail II registra pedidos y cancelaciones (facturas con prefijo `C`), pero no qué campaña o táctica originó cada compra. Sin esa unión pedido–táctica la pregunta no se puede responder con esos datos, por lo que la idea queda aparcada.
- **Idea 3:** es la más limpia porque problema, datos y variable a predecir están alineados (el corpus de Ott trae la etiqueta engañosa/veraz). **Es la idea elegida para continuar** a partir de la entrega 2, aplicando la misma prudencia: el modelo detecta patrones lingüísticos asociados a reseñas engañosas, no la intención del autor.
