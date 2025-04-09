# ---------------------------
# Script generador de INCAR
# ---------------------------

import json

# Función para leer elementos y cantidades desde POSCAR
def leer_elementos_y_cantidades(poscar_path):
    with open(poscar_path, "r") as f:
        lines = f.readlines()
        elementos = lines[5].split()
        cantidades = list(map(int, lines[6].split()))
    return elementos, cantidades

# Leer base de datos
with open("sistemas.json", "r") as f:
    data = json.load(f)

# Diccionario LDAUL
ldaul_map = {
    'Sc': 2,
    'Ti': 2,
    'V': 2,
    'Cr': 2,
    'Mn': 2,
    'Fe': 2,
    'Co': 2,
    'Ni': 2,
    'Cu': 2,
    'Zn': 2,
    'Y': 2,
    'Zr': 2,
    'Nb': 2,
    'Mo': 2,
    'Tc': 2,
    'Ru': 2,
    'Rh': 2,
    'Pd': 2,
    'Ag': 2,
    'Cd': 2,
    'Hf': 2,
    'Ta': 2,
    'W': 2,
    'Re': 2,
    'Os': 2,
    'Ir': 2,
    'Pt': 2,
    'Au': 2,
    'Hg': 2
}

# Diccionario HUBBARD (U)
hubbard_map = {
	"Cr": 3.71012,
	"W": 2.75903,
	"V": 4.67147,
	"Mo": 2.46599,
	"Mn": 5.18033,
	"Ni": 6.07158,
	"Co": 5.7629,
	"Fe": 5.77643,
	"Zn": 8.0,
	"Ti": 4.72136,
	"Re": 0.960243,
	"Ta": 3.66113,
	"Nb": 0.79064,
	"Cu": 8.78354,
	"Sc": 2.71808,
	"Y": 4.86443,
	"Zr": 4.04646,
	"Tc": 2.84086,
	"Ru": 3.5866,
	"Rh": 1.86307,
	"Pd": 3.99531,
	"Ag": 4.17711,
	"Cd": 0.629696,
	"Hf": 3.73579,
	"Os": 2.38264,
	"Ir": 1.67973,
	"Pt": 1.7264,
	"Au": 1.42857,
	"Hg": 0.892857,
}

# Template de INCAR
template_incar = """SYSTEM = {formula}
NWRITE = 2
ENCUT = 520
LREAL = .FALSE.
PREC = Accurate
ADDGRID = .TRUE.
EDIFF = 1E-05
ISMEAR = 0
SIGMA = 0.05

ISPIN = 2
LORBIT = 11
MAGMOM = {magmom_line}

LDAU = {ldau_flag}
LDAUTYPE = 2
LDAUPRINT = 0
LDAUL = {ldaul_line}
LDAUU = {ldauu_line}
LDAUJ = {ldauj_line}
LMAXMIX = 4

LPLANE = .TRUE.
LVHAR = .TRUE.
"""

# Generación de INCAR por material
for entry in data:
    formula = entry.get("formula", "Unknown")
    material_id = entry.get("material_id", "no_id")
    sistema_id = entry.get("sistema")

    # Leer POSCAR correspondiente
    poscar_path = f"POSCARS/POSCAR_{sistema_id}"
    elementos_poscar, cantidades_poscar = leer_elementos_y_cantidades(poscar_path)

    # Asignacionn de MAGMOM
    magmom_parts = []
    for el, count in zip(elementos_poscar, cantidades_poscar):
        valor = 5 if el in ldaul_map else 0
        magmom_parts.append(f"{count}*{valor}")
    magmom_line = " ".join(magmom_parts)

    # LDAUL / LDAUU / LDAUJ
    ldaul_line = " ".join(str(ldaul_map.get(el, -1)) for el in elementos_poscar)
    ldauu_line = " ".join(str(hubbard_map.get(el, 0.0)) for el in elementos_poscar)
    ldauj_line = " ".join("0.0" for _ in elementos_poscar)

    # LDAU TRUE / FALSE
    usar_ldau = any(el in ldaul_map for el in elementos_poscar)
    ldau_flag = ".TRUE." if usar_ldau else ".FALSE."

    # Completar template
    incar_text = template_incar.format(
        formula=formula,
        magmom_line=magmom_line,
        ldaul_line=ldaul_line,
        ldauu_line=ldauu_line,
        ldauj_line=ldauj_line,
        ldau_flag=ldau_flag
    )

    # Guardar archivo INCAR
    with open(f"INCARS/INCAR_{sistema_id}", "w") as f_out:
        f_out.write(incar_text)

print("Generacion de INCAR terminada")


