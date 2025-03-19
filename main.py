import pandas as pd
import json

# Read the data in xlsx file
df = pd.read_csv('excel.csv')

# Select just the columns that we need
campos_deseados = ['CATEGORÍA', 'SUBCATEGORIA', 'PRODUCTO', 'TEXTO ARGUMENTOS DE VALOR', 'CARACTERISTICAS']
df_filtrado = df[campos_deseados]

# Mapa de normalización para subcategorías (clave = como aparece en CSV, valor = forma normalizada)
mapa_subcategorias = {
    # MUEVETIERRAS
    'MINI CARGADORES RUEDAS': 'MINI CARGADOR RUEDA',
    'MINI CARGADORES RUEDAS': 'MINI CARGADOR RUEDA',
    'MINI CARGADORES ORUGAS': 'MINI CARGADOR ORUGA',
    'RETROEXCAVADORAS': 'RETROEXCAVADORA',
    'EXCAVADORAS': 'EXCAVADORA',
    'BULLDOZER': 'BULLDOZER',
    'BULLDOZERS': 'BULLDOZER',
    'CARGADORES FRONTALES': 'CARGADOR FRONTAL',
    'MOTONIVELADORAS': 'MOTONIVELADORA',
    'ARTICULADOS': 'ARTICULADO',
    
    # MINERIA Y AGREGADOS
    'BULL DOZER': 'BULL DOZER',
    'BULL DOZERS': 'BULL DOZER',
    'ARTICULADOS': 'ARTICULADO',
    'CARGADORES FRONTALES': 'CARGADOR FRONTAL',
    'MARTILLOS': 'MARTILLO',
    'PERFORADORAS': 'PERFORADORA',
    
    # AGRICOLA
    'TRACTORES': 'TRACTOR',
    'FORRAJEROS': 'FORRAJERO',
    'ASPERSORAS': 'ASPERSORA',
    'GATORS': 'GATOR',
    'JARDINEROS': 'JARDINERO',
    'SEMBRADORAS': 'SEMBRADORA',
    'LABRANZA': 'LABRANZA',
    'MANEJO DE MATERIAL': 'MANEJO DE MATERIAL',
    
    # PAVIMENTACION
    'FRESADORAS': 'FRESADORA',
    'RECICLAJE': 'RECICLAJE',
    'TRITURADORAS': 'TRITURADORA',
    'EXTENDEDORAS': 'EXTENDEDORA',
    'COMPACTADORES': 'COMPACTADOR',
    'RODILLOS TÁNDEM': 'RODILLO TÁNDEM',
    'RODILLOS NEUMÁTICO': 'RODILLO NEUMÁTICO',
    
    # PLANTAS DE ASFALTO
    'PLANTAS DE ASFALTO MÓVILES': 'PLANTA DE ASFALTO MÓVIL',
    'PLANTA DE ASFALTO ESTACIONARIA': 'PLANTA DE ASFALTO ESTACIONARIA'
}

# Normalizar las subcategorías en el DataFrame
df_filtrado['SUBCATEGORIA_NORMALIZADA'] = df_filtrado['SUBCATEGORIA'].map(mapa_subcategorias)
# Para subcategorías que no estén en el mapa, mantener el valor original
df_filtrado['SUBCATEGORIA_NORMALIZADA'] = df_filtrado['SUBCATEGORIA_NORMALIZADA'].fillna(df_filtrado['SUBCATEGORIA'])

# Definir las listas normalizadas para cada categoría
subcategorias_muevetierras = [
    'MINI CARGADOR RUEDA',
    'MINI CARGADOR ORUGA',
    'RETROEXCAVADORA',
    'EXCAVADORA',
    'BULLDOZER',
    'CARGADOR FRONTAL',
    'MOTONIVELADORA',
    'ARTICULADO'
]

subcategorias_mineria = [
    'BULL DOZER',
    'ARTICULADO',
    'CARGADOR FRONTAL',
    'MARTILLO',
    'PERFORADORA'
]

subcategorias_agricola = [
    'TRACTOR',
    'FORRAJERO',
    'ASPERSORA',
    'GATOR',
    'JARDINERO',
    'SEMBRADORA',
    'LABRANZA',
    'MANEJO DE MATERIAL'
]

subcategorias_pavimentacion = [
    'FRESADORA',
    'RECICLAJE',
    'TRITURADORA',
    'EXTENDEDORA',
    'COMPACTADOR',
    'RODILLO TÁNDEM',
    'RODILLO NEUMÁTICO'
]

subcategorias_plantas_asfalto = [
    'PLANTA DE ASFALTO MÓVIL',
    'PLANTA DE ASFALTO ESTACIONARIA'
]

# Asignar categorías donde corresponda, usando la subcategoría normalizada
df_filtrado.loc[df_filtrado['SUBCATEGORIA_NORMALIZADA'].isin(subcategorias_muevetierras), 'CATEGORÍA'] = 'MUEVETIERRAS'
df_filtrado.loc[df_filtrado['SUBCATEGORIA_NORMALIZADA'].isin(subcategorias_agricola), 'CATEGORÍA'] = 'AGRICOLA'
df_filtrado.loc[df_filtrado['SUBCATEGORIA_NORMALIZADA'].isin(subcategorias_pavimentacion), 'CATEGORÍA'] = 'PAVIMENTACION'
df_filtrado.loc[df_filtrado['SUBCATEGORIA_NORMALIZADA'].isin(subcategorias_plantas_asfalto), 'CATEGORÍA'] = 'PLANTAS DE ASFALTO'
df_filtrado.loc[df_filtrado['SUBCATEGORIA_NORMALIZADA'].isin(subcategorias_mineria), 'CATEGORÍA'] = 'MINERIA Y AGREGADOS'

# También actualizar la subcategoría original con la versión normalizada
df_filtrado['SUBCATEGORIA'] = df_filtrado['SUBCATEGORIA_NORMALIZADA']

# Eliminar la columna temporal de normalización
df_filtrado = df_filtrado.drop(columns=['SUBCATEGORIA_NORMALIZADA'])

# Agregar 3 campos de rutas de imágenes genéricas
df_filtrado['IMAGEN_PRINCIPAL'] = df_filtrado.apply(
    lambda row: f"/PRODUCTOS/{row['SUBCATEGORIA']}/principal.jpg", axis=1)
df_filtrado['IMAGEN_SECUNDARIA'] = df_filtrado.apply(
    lambda row: f"/PRODUCTOS/{row['SUBCATEGORIA']}/secundaria.jpg", axis=1)
df_filtrado['IMAGEN_DETALLE'] = df_filtrado.apply(
    lambda row: f"/PRODUCTOS/{row['SUBCATEGORIA']}/detalle.jpg", axis=1)

# Convert to json
json_data = df_filtrado.to_json(orient='records', force_ascii=False)
json_formatted = json.loads(json_data)
json_pretty = json.dumps(json_formatted, indent=4, ensure_ascii=False)

# Save the json to a file
with open('datos_productos.json', 'w', encoding='utf-8') as f:
    f.write(json_pretty)
    
print('Conversion completa. Los datos se guardaron con exito padrino')