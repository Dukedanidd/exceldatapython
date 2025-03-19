import pandas as pd
import json
import os
import re

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

# Función para encontrar las imágenes de cualquier producto
def encontrar_imagenes_producto(row):
    imagenes = []
    producto = str(row['PRODUCTO'])
    subcategoria = str(row['SUBCATEGORIA'])
    
    # Extraer todos los códigos numéricos del producto
    codigos = re.findall(r'\b\d+\b', producto)
    if not codigos:
        return imagenes
    
    # Directorio base de productos
    base_dir = 'PRODUCTOS'
    
    # 1. Primero, buscar en una carpeta específica para la subcategoría
    if os.path.exists(os.path.join(base_dir, subcategoria)):
        subcategoria_dir = os.path.join(base_dir, subcategoria)
        # Buscar carpetas que coincidan con cualquiera de los códigos extraídos
        for codigo in codigos:
            for item in os.listdir(subcategoria_dir):
                item_path = os.path.join(subcategoria_dir, item)
                # Si el código está en el nombre de la carpeta o archivo
                if codigo in item and os.path.isdir(item_path):
                    # Es una carpeta, buscar imágenes dentro
                    for file in os.listdir(item_path):
                        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            imagen_path = os.path.join(item_path, file).replace('\\', '/')
                            imagenes.append(imagen_path)
                elif codigo in item and item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # Es una imagen directamente
                    imagen_path = item_path.replace('\\', '/')
                    imagenes.append(imagen_path)
    
    # 2. Si no se encontró nada, buscar en todo el directorio de productos
    if not imagenes:
        for root, dirs, files in os.walk(base_dir):
            for codigo in codigos:
                # Buscar directorios que coincidan con el código
                for dir_name in dirs:
                    if codigo in dir_name:
                        dir_path = os.path.join(root, dir_name)
                        # Buscar imágenes en ese directorio
                        for file in os.listdir(dir_path):
                            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                                imagen_path = os.path.join(dir_path, file).replace('\\', '/')
                                imagenes.append(imagen_path)
                
                # También buscar archivos de imagen que coincidan con el código
                for file in files:
                    if codigo in file and file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        imagen_path = os.path.join(root, file).replace('\\', '/')
                        imagenes.append(imagen_path)
    
    return imagenes

# Agregar imágenes a cada producto
df_filtrado['IMAGENES'] = df_filtrado.apply(encontrar_imagenes_producto, axis=1)

# Convert to json
json_data = df_filtrado.to_json(orient='records', force_ascii=False)
json_formatted = json.loads(json_data)
json_pretty = json.dumps(json_formatted, indent=4, ensure_ascii=False)

# Save the json to a file
with open('datos_productos.json', 'w', encoding='utf-8') as f:
    f.write(json_pretty)
    
print('Conversion completa. Los datos se guardaron con exito padrino')