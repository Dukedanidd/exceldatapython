import pandas as pd
import json

# Read the data in xlsx file
df = pd.read_excel('')

# Select just the columns that we need
campos_deseados = ['CATEGORÍA', 'SUBCATEGORÍA', 'PRODUCTO', 'TEXTO ARGUMENTOS DE VALOR', 'CARACTERÍSTICAS']
df_filtrado = df[campos_deseados]

# Convert to json
json_data =df_filtrado.to_json(orient='records', force_ascii=False)
json_formatted = json.loads(json_data)
json_pretty = json.dumps(json_formatted, indent=4, ensure_ascii=False)

# Save the json to a file
with open('datos_productos.json', 'w', encoding='utf-8') as f:
    f.write(json_pretty)
    
print('Conversion completa. Los datos se guardaron con exito padrino')