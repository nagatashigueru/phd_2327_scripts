# Script para transformar el formato JSON
# de la base de datos a un formato JSON
# entendible por PANDAS

import json
import pandas as pd

# ---
# Convierte cada linea a un diccionario

with open("./db.json", encoding="utf8") as f:
    data = f.readlines()
    data = [json.loads(line) for line in data]

# ---
# escribe los datos a un archivo

with open("DataBase.json", "w") as j:
    json.dump(data,j)
