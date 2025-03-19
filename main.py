import pandas as pd
import json

# Read the data in xlsx file
df = pd.read_excel('')

# Select just the columns that we need
campos_deseados = ['CATEGORÍA', 'SUBCATEGORÍA', 'PRODUCTO', 'TEXTO ARGUMENTOS DE VALOR', 'CARACTERÍSTICAS']
df_filtrado = df[campos_deseados]