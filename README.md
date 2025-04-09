# Scripts para la tesis

Scripts utilizados en diferentes etapas de la tesis. Seran documentados mejor en la sección de anexos de la tesis.

## Scripts:

- **Tojson:** Procesa el formato original de la base de datos de 2dmatpedia, para que pueda ajustarse a lo esperado por la libreria json de python.

- **incar_gen:** Genera los archivos INCAR necesarios para VASP.

- **poscar_gen:** Genera una sub-base de datos con los materiales de interes para la investigación a partir de la base de datos original procesada. Además, genera los archivos POSCAR necesarios para VASP.

- **potcar_gen:** Genera los archivos POTCAR necesarios para VASP. Estos archivos son integraciones de los archivos de potencial que proporciona VASP, y son especificos para el material que se simula.

- **run_control_pot.sh:** Es el script de control que se ejecuta en el cluster del NLHPC.
