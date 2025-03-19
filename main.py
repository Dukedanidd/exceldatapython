import pandas as pd
import json

# Read the data in xlsx file
df = pd.read_csv('excel.csv')

# Select just the columns that we need
campos_deseados = ['CATEGORÍA', 'SUBCATEGORIA', 'PRODUCTO', 'TEXTO ARGUMENTOS DE VALOR', 'CARACTERISTICAS']
df_filtrado = df[campos_deseados]

# Lista de subcategorías que pertenecen a MUEVETIERRAS
subcategorias_muevetierras = [
    'MINI CARGADORES RUEDAS',
    'MINI CARGADORES ORUGAS',
    'RETROEXCAVADORAS',
    'EXCAVADORAS',
    'BULLDOZER',
    'CARGADORES FRONTALES',
    'MOTONIVELADORAS',
    'ARTICULADOS'
]

# Lista de subcategorías que pertenecen a MINERIA Y AGREGADOS
subcategorias_mineria = [
    'BULL DOZER',
    'ARTICULADOS',
    'CARGADORES FRONTALES',
    'MARTILLOS',
    'PERFORADORAS'
]

# Lista de subcategorías que pertenecen a AGRICOLA
subcategorias_agricola = [
    'TRACTORES',
    'FORRAJEROS',
    'ASPERSORAS',
    'GATORS',
    'JARDINEROS',
    'SEMBRADORAS',
    'LABRANZA',
    'MANEJO DE MATERIAL'
]

# Lista de subcategorías que pertenecen a PAVIMENTACION
subcategorias_pavimentacion = [
    'FRESADORAS',
    'RECICLAJE',
    'TRITURADORAS',
    'EXTENDEDORAS',
    'COMPACTADORES',
    'RODILLOS TÁNDEM',
    'RODILLOS NEUMÁTICO'
]

# Lista de subcategorías que pertenecen a PLANTAS DE ASFALTO
subcategorias_plantas_asfalto = [
    'PLANTAS DE ASFALTO MÓVILES',
    'PLANTA DE ASFALTO ESTACIONARIA'
]

# Asignar categorías donde corresponda
df_filtrado.loc[df_filtrado['SUBCATEGORIA'].isin(subcategorias_muevetierras), 'CATEGORÍA'] = 'MUEVETIERRAS'
df_filtrado.loc[df_filtrado['SUBCATEGORIA'].isin(subcategorias_agricola), 'CATEGORÍA'] = 'AGRICOLA'
df_filtrado.loc[df_filtrado['SUBCATEGORIA'].isin(subcategorias_pavimentacion), 'CATEGORÍA'] = 'PAVIMENTACION'
df_filtrado.loc[df_filtrado['SUBCATEGORIA'].isin(subcategorias_plantas_asfalto), 'CATEGORÍA'] = 'PLANTAS DE ASFALTO'
df_filtrado.loc[df_filtrado['SUBCATEGORIA'].isin(subcategorias_mineria), 'CATEGORÍA'] = 'MINERIA Y AGREGADOS'

# Convert to json
json_data = df_filtrado.to_json(orient='records', force_ascii=False)
json_formatted = json.loads(json_data)
json_pretty = json.dumps(json_formatted, indent=4, ensure_ascii=False)

# Save the json to a file
with open('datos_productos.json', 'w', encoding='utf-8') as f:
    f.write(json_pretty)
    
print('Conversion completa. Los datos se guardaron con exito padrino')