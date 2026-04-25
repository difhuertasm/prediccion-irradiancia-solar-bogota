import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

#____________________________Carga de archivo___________________________________________#

#Data Set Export - RAD SOLAR.RSG_AUT_60@21206960 
#(IDEAM/DHIME PORTAL: http://aquariuswebportal.ideam.gov.co/Data/DataSet/Summary/Location/21206960/DataSet/RAD%20SOLAR/RSG_AUT_60/Interval/Latest)

separador = ','

df = pd.read_csv('RadiacionSolarBogota.csv', delimiter=separador, skiprows=1)
#Por alguna razón no permite visualizar correctamente el nombre de las columnas en Python, así que se importa el dataset omitiendo la primera fila.

#Se agregan de nuevo los nombres de las columnas corregidos.
df.columns = ['Timestamp (UTC-05:00)', 'Value (Wh/m^2)', 'Grade Code', 'Approval Level', 'Interpolation Type', 'Event Timestamp']

total = len(df)#Determina el número total de registros del dataset

print(f'Este dataset tiene {total} registros.')

print("\nPrimeras 5 filas archivo CSV: \n\n",df.head(5))# Imprime los cinco primeros registros del dataset

#Verificar los nombres de las columnas
print("\nNombres de columnas en el Dataset:\n")

#Recorre el arreglo df.columns y enumera sus elementos
for i, col in enumerate(df.columns):
    print(f"{i+1}. '{col}'")
#____________________________Separación de fechas___________________________________________#

#Convierte la columna 'fecha' a tipo datetime
df['Timestamp (UTC-05:00)'] = pd.to_datetime(df['Timestamp (UTC-05:00)'])

# Extraer el año
df['Year'] = df['Timestamp (UTC-05:00)'].dt.year

# Extraer el mes
df['Month'] = df['Timestamp (UTC-05:00)'].dt.month

# Extraer el día
df['Day'] = df['Timestamp (UTC-05:00)'].dt.day

# Extraer la hora
df['Hour'] = df['Timestamp (UTC-05:00)'].dt.hour

#Lista de meses a usar
mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# Reemplazar números de mes por su respectivo nombre
df['Month'] = df['Month'].map(lambda i: mes[i-1])

#____________________________Borrado de columnas y preprocesamiento___________________________________________#

df = df.drop(columns=['Event Timestamp'])
df = df.drop(columns=['Timestamp (UTC-05:00)'])

print("\nNúmero de datos Nulos: \n\n", df.isnull().sum())
print("\nDatos estadísticos del dataset: \n\n", df.describe())

print("Valor mínimo:", df['Value (Wh/m^2)'].min())
print("Valor máximo:", df['Value (Wh/m^2)'].max())

df_outliers = df[(df['Value (Wh/m^2)'] < 0) | (df['Value (Wh/m^2)'] > 1200)] #Verificación de outliers
print("Valores fuera del rango:\n", df_outliers)

print(df.head(5))
#____________________________Visualización Gráfica___________________________________________#

media_mensual = df.groupby('Month')['Value (Wh/m^2)'].mean().reindex(mes)

while True:
    opcion = input('¿Desea ver de forma gráfica la representación de los datos? (sí/no): ')
    if opcion.lower() in ['sí', 'si', 'no']:
        break
    print("Por favor, ingrese 'sí' o 'no'.")

if opcion.lower() != 'no':
    # Código de las gráficas y cálculos aquí
    plt.hist(df['Value (Wh/m^2)'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribución de irradiancia')
    plt.xlabel('Wh/m²')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.show()

    media_mensual.plot(kind='bar', color='teal')
    plt.title('Irradiancia promedio mensual')
    plt.xlabel('Mes')
    plt.ylabel('Wh/m²')
    plt.show()

    df.groupby('Hour')['Value (Wh/m^2)'].mean().plot(kind='line', marker='o', color='green')
    plt.title('Irradiancia promedio por hora')
    plt.xlabel('Hora del día')
    plt.ylabel('Wh/m²')
    plt.grid(True)
    plt.show()

    #Promedio irradiancia por hora
    promedioIrradiancia = df.groupby('Hour')['Value (Wh/m^2)'].mean()
    #Extrae el valor máximo del promedio
    valorMaximo = promedioIrradiancia.max()
    #idmax devuelve la etiqueta (hora) del valor máximo
    horaValorMaximo = promedioIrradiancia.idxmax()

    print("\n|________________________________________________________________________________|\n")
    print(f"En promedio, la hora con mayor radiación solar es a las {horaValorMaximo} PM. \n")
    print("|________________________________________________________________________________|\n")
else:
	cero_total = (df['Value (Wh/m^2)'] == 0).sum()
	porcentaje_cero = (cero_total / len(df)) * 100
	print(f"Porcentaje de registros con irradiancia cero: {porcentaje_cero:.2f}%")

df_mes = df.groupby(['Year', 'Month'])['Value (Wh/m^2)'].mean().reset_index()

#____________________________Modelo de predicción___________________________________________#

le = LabelEncoder()
df_mes['Month_num'] = le.fit_transform(df_mes['Month'])  # Enero=0, Febrero=1, Marzo=2, etc.

x = df_mes[['Year', 'Month_num']]#Creación de variable predictorias
y = df_mes['Value (Wh/m^2)']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(x_train, y_train)


##añosFuturos = [2025, 2026]
añoFuturo = [2027]
meses = list(range(12))  # 0 a 11 si usaste LabelEncoder

datosFuturos = pd.DataFrame([(año, mes) for año in añoFuturo for mes in meses],
                           columns=['Year', 'Month_num'])

predicciones = modelo.predict(datosFuturos)
datosFuturos['Predicted Irradiance'] = predicciones

opcion = input("¿Desea ver los datos predichos (si/no): ")
if opcion.lower() == "si":
    print(predicciones)

opcion = input("¿Desea ver gráficamente datos predichos (si/no): ")
if opcion.lower() == "si":

    # Graficar por año, asegurando el orden de los meses
    for año in añoFuturo:
        subConjunto = datosFuturos[datosFuturos['Year'] == año].sort_values('Month_num')
        plt.plot(subConjunto['Month_num'], subConjunto['Predicted Irradiance'], label=str(año), marker='o')

    plt.xticks(ticks=range(12), labels=mes, rotation=45)
    plt.xlabel('Mes')
    plt.ylabel('Wh/m²')
    plt.title('Predicción mensual de irradiancia solar (Scikit-learn)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("\n|-----Fin del programa-----|.")

