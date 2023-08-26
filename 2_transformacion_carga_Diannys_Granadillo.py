# Se importan las librerias
import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt

# Se cargan la data desde un archivo csv
data = pd.read_csv('test_data.csv', sep='|', decimal=',', parse_dates=['Fecha de Nacimiento'])

# Visualizacion de columnas
print(data.columns.values)

# Visualizacion del tamaño de la data
print(data.shape)

# Se elimina la columna ID de prestamo (Primario)
del(data['ID de préstamo (Primario)'])

# Se observa la estructura de los datos visualizando dos registros
print(data.head(2).T)

# Se adecuan las columnas para mejor analisis de los datos
data.columns = data.columns.str.replace(' ', '_')

# Se crea columna con Nombre completo
data['Nombre_Completo'] = data['Nombres']+' '+data['Apellidos']
print(data.head(2).T)

# Funcion para calcular edad
def edad(fechaNacimiento):
  today= date.today()
  Calculo_edad = today.year - fechaNacimiento.year - ((today.month, today.day)< (fechaNacimiento.month, fechaNacimiento.day))
  return Calculo_edad

# Se crea una columna en el dataframe para asignar la edad calculada
data['Edad_Cliente'] = data['Fecha_de_Nacimiento'].apply(edad)
print(data.head(3).T)

# Se procesa la fecha del extracto de la base de datos asignando la fecha y hora a columnas independientes
data['Fecha_del_extracto_de_la_base_de_datos'] = pd.to_datetime(data['Fecha_del_extracto_de_la_base_de_datos'],errors='coerce').dt.date
data['Hora_del_extracto_de_la_base_de_datos'] =  pd.to_datetime(data['Fecha_del_extracto_de_la_base_de_datos'],errors='coerce').dt.time
print(data.head(3).T)

# Se reemplaza el valor del genero por masculino y femenino segun corresponda
data['Genero'] = data['Genero'].replace({'mujer': 'femenino', 'hombre': 'masculino'})
print(data.head(4).T)

# Se crea un dataset con los clientes que tienen saldo superior a 200.000 pesos
Clientes_filtrados_saldo = data[data['Saldo_en_mora'] > 200000]
# Nota: De acuerdo al analisis realizado no hay clientes con este saldo actualmente, por lo que el filtro arroja
# la misma cantidad de datos del dataframe original

# Se grafica el total de negociaciones por tipo de negociacion
total_negociaciones = data.groupby(["Tipo_de_Negociacion","Tomo_negociacion"]).agg({"ID_de_cliente": "count"}).reset_index()
total_negociaciones = total_negociaciones.pivot(index="Tomo_negociacion", columns="Tipo_de_Negociacion", values="ID_de_cliente").fillna(0)
print(total_negociaciones)

# Se grafica los productos que presentan mayor saldo en mora
Producto_en_mora = data.groupby(["Tipo_de_producto"]).agg({"Saldo_en_mora":"sum"}).reset_index()
Producto_en_mora.describe()

plt.bar( Producto_en_mora.Tipo_de_producto,  Producto_en_mora.Saldo_en_mora)
plt.title('Saldo en mora por tipo de producto')
plt.xlabel('Tipo de producto')
plt.ylabel('Saldo en mora')
plt.show()