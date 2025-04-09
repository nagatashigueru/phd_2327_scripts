# ----------------------------
# Script generador de POTCAR
# ----------------------------

import os
from pathlib import Path

# Constantes
PoscarPath = "./POSCARS"
PotcarPath = "./PBE"
POTCARSPath = "./POTCARS"

# Listar POSCARS
def PoscarList(PosLRuta):
    PoscarRuta = Path(PosLRuta)
    PoscarsList = [poscar.name for poscar in PoscarRuta.iterdir() if poscar.is_file()]
    return PoscarsList

# Listar POTCARS
def PotcarList(PotLRuta):
    PotcarRuta = Path(PotLRuta)
    PotcarsList = [potcar.name for potcar in PotcarRuta.iterdir() if potcar.is_dir()]
    return PotcarsList

# Obtener elementos
def PoscarElement(PosERuta,PosEName):
    PoscarFile = open(PosERuta+"/"+PosEName, "r")
    PoscarLines = PoscarFile.readlines()
    for i,Line in enumerate(PoscarLines):
        if (i == 5):
            Components = Line.split()
        else:
            continue
    PoscarFile.close()
    return Components

# Integrar POTCARS
def PotcarJoin(PotcarPath,PotJRuta,PotJPots,PotJElem,PotJPosName):
    name = PotJPosName.split("_")
    SalidaRuta = PotJRuta+"/POTCAR_"+name[1]
    for element in PotJElem:
        if (element in PotJPots):
            poscar_ruta = PotcarPath+"/"+element+"/"+"POTCAR"
            with open(SalidaRuta, "a") as salida:
                with open(poscar_ruta, "r") as posfile:
                    contenido = posfile.read()
                    salida.write(contenido)
        elif(element+"_sv" in PotJPots):
            poscar_ruta = PotcarPath+"/"+element+"_sv"+"/"+"POTCAR"
            with open(SalidaRuta, "a") as salida:
                with open(poscar_ruta, "r") as posfile:
                    contenido = posfile.read()
                    salida.write(contenido)
        else:
            print("fallo")

Potcars = PotcarList(PotcarPath)
Poscars = PoscarList(PoscarPath)

Pots = 0

for PoscarName in Poscars:
    Elements = PoscarElement(PoscarPath,PoscarName)
    PotcarJoin(PotcarPath,POTCARSPath,Potcars,Elements,PoscarName)
    Pots = Pots + 1

print("Se hallaron : %s POSCAR"%len(Poscars))
print("Se crearon : %s POTCAR unidos"%Pots)
print(f"Archivos POTCAR generados en carpeta 'POTCARS/' para {Pots} materiales.")

