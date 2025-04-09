#!/bin/bash
#SBATCH --job-name="test"
#SBATCH --partition="main"
#SBATCH -n 2
#SBATCH --ntasks-per-node=2
#SBATCH --output=vasp-srun.out 
#SBATCH --error=vasp-srun.err
#SBATCH --mem-per-cpu=2000M
#SBATCH --time=02:00:00


module purge
ml intel/2018.04 VASP/5.4.4


export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export LC_ALL=C

EXEC=vasp_std
BINVASP="${EXEC}"

for i in {0..2}; do
    poscarorigen="POSCAR_$i"
    potcarorigen="POTCAR_$i"
    incarorigen="INCAR_$i"
    mkdir "sistema_$i"
    cp "POSCARS/$poscarorigen" "./sistema_$i/POSCAR"
    cp "POTCARS/$potcarorigen" "./sistema_$i/POTCAR"
    cp "INCARS/$incarorigen" "./sistema_$i/INCAR"
    cp KPOINTS "./sistema_$i/"
    (
    cd "./sistema_$i" || exit
    srun $BINVASP
    rm CHG CHGCAR WAVECAR EIGENVAL PROCAR DOSCAR OSZICAR PCDAT XDATCAR REPORT
    )
done
