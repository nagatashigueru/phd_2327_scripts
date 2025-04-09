# ------------------------------------------------
# Script generador de POSCAR y sub base de datos
# ------------------------------------------------

import json
from pymatgen.core import Structure, Element
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# Lista de grupos espaciales polares
polar_spacegroup_numbers = [
    1, 3, 4, 6, 7, 8, 9, 16, 18, 33, 36, 38, 99,
    143, 144, 145, 146, 147, 148, 149, 150, 151,
    152, 153, 154, 155, 156, 157, 158, 159, 160,
    161, 186
]

# Detectar Lantanidos
def contiene_lantanido(structure):
    elementos = {site.specie.symbol for site in structure}
    for el in elementos:
        try:
            if Element(el).is_lanthanoid:
                return True
        except:
            continue
    return False
    
# Detectar Actinidos    
def contiene_actinido(structure):
    elementos = {site.specie.symbol for site in structure}
    for el in elementos:
        try:
            if Element(el).is_actinoid:
                return True
        except:
            continue
    return False

# Leer base de datos
with open("DataBase.json", "r") as f:
    data = json.load(f)

polares_aislantes = []
estructuras = []

NS = 0

# Generación de POSCAR por material
for entry in data:
    band_gap = entry.get("bandgap")
    struct_dict = entry.get("structure")

    if band_gap is None or struct_dict is None:
        continue

    if band_gap <= 0:
        continue  # no es aislante

    try:
        estructura = Structure.from_dict(struct_dict)
        
        if contiene_lantanido(estructura):
            continue
        
        if contiene_actinido(estructura):
            continue
        
        sga = SpacegroupAnalyzer(estructura, symprec=0.01)
        spg_num = sga.get_space_group_number()
        
        if spg_num in polar_spacegroup_numbers:
            calc_settings = entry.get("calc_settings", {})
            hubbards = calc_settings.get("hubbards")
            
            #magmoms = [site.properties.get("magmom", 0) for site in estructura.sites]
            
            magmoms_por_elemento = []
            for site in estructura.sites:
                magmom = site.properties.get("magmom", 0.0)
                elemento = site.specie.symbol
                magmoms_por_elemento.append({
                    elemento: magmom
                })
                                
            polares_aislantes.append({
                "sistema": NS,
                "material_id": entry.get("material_id", "unknown"),
                "formula": entry.get("formula_pretty"),
                "elements": entry.get("elements"),
                "band_gap": band_gap,
                "spacegroup": sga.get_space_group_symbol(),
                "spg_number": spg_num,
                "hubbards": hubbards,
                "magmoms": magmoms_por_elemento
            })
            estructuras.append(estructura)
            NS = NS + 1

    except Exception as e:
        continue

# Guardar sub base de datos
with open("sistemas.json", "w") as f_out:
    json.dump(polares_aislantes, f_out, indent=2)

# Guardar archivo POSCAR
for i, estruct in enumerate(estructuras):
    estruct.to(filename=f"./POSCARS/POSCAR_{i}")

print(f"Se encontraron {len(polares_aislantes)} materiales polares aislantes.")
print(f"Archivos POSCAR generados en carpeta 'POSCARS/' para {len(polares_aislantes)} materiales.")
