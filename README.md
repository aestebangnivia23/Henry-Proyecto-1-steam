# Henry_PI_SteamGames
Proyecto Individual Nº1 - Machine Learning Operations (MLOps)
Descripción del problema:
Steam es una plataforma de videojuegos donde los usuarios pueden acceder a miles de títulos y escribir reseñas. El objetivo del proyecto es crear un sistema de recomendación de videojuegos utilizando datos de la plataforma. Sin embargo, los datos iniciales no se encuentran estructurados correctamente, ya que son del tipo JSON anidado, lo que dificulta su manipulación. El objetivo es desarrollar un MVP de un sistema de recomendación basado en estos datos, generando recomendaciones personalizadas para los usuarios.

## Tareas realizadas:
### 1. Transformación de datos:
El primer paso consistió en cargar y descomprimir los archivos, que estaban comprimidos en formato gzip.

Para los datos de juegos de Steam: se utilizó la función json.loads() para convertir el texto JSON en objetos de Python.
Para las reseñas y elementos de usuario: se utilizó la librería ast para convertir cada línea de texto en un diccionario de Python.
Luego, los datos fueron transformados en dataframes para facilitar su manipulación con librerías como pandas.
### 2. Feature Engineering:
Dado que las reseñas de los usuarios no solo incluían un valor binario de recomendación (True o False), sino también comentarios textuales, se aplicó análisis de sentimiento a las reseñas escritas utilizando NLP (Natural Language Processing) con la clase SentimentIntensityAnalyzer de la biblioteca NLTK.

Se creó la columna 'sentiment_analysis' que clasifica cada reseña con un valor:
0 si es negativa,
1 si es neutral,
2 si es positiva.
Si la reseña escrita estaba ausente, se imputaba como neutral.
### 3. Preparación de los datos para la API:
Para optimizar la API y el entrenamiento del modelo, se realizaron varias tareas de preparación de datos:

Imputación de nulos: los valores nulos fueron eliminados o imputados según fuera necesario.
Selección y filtrado de columnas: se seleccionaron las columnas más relevantes y se filtraron los registros de acuerdo a las necesidades del análisis y los modelos de aprendizaje automático.
Modificación de tipos de variables: para asegurar que los datos fueran manipulables correctamente, se cambiaron los tipos de varias columnas.
Expansión de listas y diccionarios: se expandieron las columnas anidadas.
Combinación de dataframes: se combinaron los diferentes conjuntos de datos para relacionar la información de juegos, reseñas y usuarios.
Exportación de datos: los dataframes procesados se exportaron a archivos .csv, excepto el dataset utilizado para el sistema de recomendación, que fue guardado como archivo .parquet debido a su tamaño.
### 4. Desarrollo de la API y Deployment:
Se implementaron múltiples endpoints usando FastAPI para brindar acceso a los datos y al sistema de recomendaciones:

PlayTimeGenre(genero): Devuelve el año con más horas jugadas para un género específico.

Ejemplo: {"Año con más horas jugadas para el género Accion": 2013}
UserForGenre(genero): Devuelve el usuario con más horas jugadas para ese género y un resumen anual de sus horas jugadas.

Ejemplo: {"Usuario con más horas jugadas para Acción": "user123", "Horas":[{"Año":2013, "Horas":120}, {"Año":2012, "Horas":90}]}
UsersRecommend(año): Devuelve los 3 juegos más recomendados por los usuarios en un año determinado.

Ejemplo: {"Puesto 1": "GameX", "Puesto 2": "GameY", "Puesto 3": "GameZ"}
UsersNotRecommend(año): Devuelve los 3 juegos menos recomendados por los usuarios en un año determinado.

Ejemplo: {"Puesto 1": "GameX", "Puesto 2": "GameY", "Puesto 3": "GameZ"}
sentiment_analysis(año): Devuelve el conteo de reseñas negativas, neutrales y positivas de un año dado.

Ejemplo: {"Negative": 100, "Neutral": 50, "Positive": 150}
El deployment se realizó en Render, siguiendo este tutorial.
Link de la API: https://henry-pi-steamgames.onrender.com/docs

## Exploratory Data Analysis (EDA):
Durante el EDA, se analizaron las relaciones entre variables, patrones, y se identificaron outliers y valores nulos. Se generó una nube de palabras a partir de las reseñas para identificar las características más mencionadas por los usuarios. El objetivo fue reducir el número de columnas del dataset final y optimizar el rendimiento del sistema de recomendación.

## Modelo de aprendizaje automático:
El modelo desarrollado es un sistema de recomendación basado en similitud de ítems (item-item). Este sistema toma como entrada el ID de un juego y genera recomendaciones de juegos similares utilizando la similaridad de coseno. La función disponible en la API es:

recomendacion_juego(id_producto): Dado el ID de un juego, devuelve una lista de 5 juegos recomendados que son similares al ingresado.
### Proceso del modelo:
Matriz de características: Se construye una matriz donde cada juego es descrito por sus características y las reseñas de los usuarios.
Cálculo de la similaridad de coseno: Para cada par de juegos, se calcula el coseno del ángulo entre sus vectores de características, lo que permite medir la similitud entre ellos.
Generación de recomendaciones: Se recomienda al usuario aquellos juegos con una mayor similaridad de coseno respecto al juego consultado.
## Video demostrativo:
En el siguiente video se muestra el funcionamiento de la API y se ejemplifican las consultas realizadas, incluyendo el sistema de recomendación.
https://youtu.be/oD1ZF8xtb-w

