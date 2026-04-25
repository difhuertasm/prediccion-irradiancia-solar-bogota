Predicción de Irradiancia Solar en Bogotá 
Este proyecto realiza un análisis exploratorio de datos (EDA) y desarrolla un modelo de regresión para predecir la radiación solar en la ciudad de Bogotá, utilizando datos históricos del portal DHIME del IDEAM (Disponible en: http://aquariuswebportal.ideam.gov.co/Data/DataSet/Summary/Location/21206960/DataSet/RAD%20SOLAR/RSG_AUT_60/Interval/Latest).


📊 Descripción del Proyecto
El objetivo es procesar registros de radiación solar global (Wh/m²) para identificar patrones horarios y mensuales, y entrenar un algoritmo de Random Forest capaz de estimar la irradiancia futura. El modelo ayuda a entender la viabilidad de proyectos de energía solar basados en la estacionalidad climática de la ciudad.


🛠️ Tecnologías Utilizadas
Python (Lenguaje principal)

* Pandas & NumPy: Limpieza de datos y manipulación de series temporales.

* Matplotlib: Visualización de distribuciones y promedios mensuales/horarios.

* Scikit-learn: * RandomForestRegressor para el modelo predictivo.

* LabelEncoder para el tratamiento de variables categóricas.

* train_test_split para la validación del modelo.


📈 Funcionalidades Clave

* Preprocesamiento de Datos: Limpieza de encabezados, manejo de valores nulos y detección de outliers (valores fuera del rango 0-1200 Wh/m²).

* Ingeniería de Características: Extracción de componentes temporales (Año, Mes, Día, Hora) a partir de marcas de tiempo UTC-05:00.

* Análisis Estadístico: Cálculo de horas pico de radiación y promedios mensuales históricos.

* Modelo Predictivo: Implementación de un bosque aleatorio para predecir la radiación mensual para el año 2027.

🚀 Cómo Ejecutar el Proyecto

Clona este repositorio mediante:
 
 git clone https://github.com/tu-usuario/nombre-del-repo.git
 
Asegúrate de tener el archivo RadiacionSolarBogota.csv en la raíz del proyecto.

Instala las dependencias:


 pip install pandas matplotlib scikit-learn

Ejecuta el script:

 python prediccion_solar.py
 
📋 Ejemplo de Resultados

Visualización: El programa genera gráficas de histogramas de distribución, barras de promedio mensual y líneas de tendencia horaria.

Insights: Identificación automática de la hora con mayor radiación solar (promedio histórico).

Predicción: Generación de un forecast para los 12 meses del año 2027.


📂 Estructura del Dataset
El dataset original proviene de estaciones automáticas del IDEAM con intervalos de 60 minutos. Las columnas procesadas incluyen:

Value (Wh/m^2): Variable objetivo (irradiancia).

Timestamp: Fecha y hora de la captura.

Year/Month/Hour: Variables predictoras generadas.


Autor: Fernando Huertas M
