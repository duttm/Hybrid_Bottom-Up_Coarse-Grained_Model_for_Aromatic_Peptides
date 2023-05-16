#!/bin/bash

#SBATCH --mail-user=mh1314@scarletmail.rutgers.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=ibi
#SBATCH --partition RM-shared
# -N 1 --ntasks-per-node=32
#SBATCH -N 1 --ntasks-per-node=32
#SBATCH --time=24:00:00
#SBATCH --output=slurm.%N.%j.out
#SBATCH --export=ALL

#GMX_APP=/ocean/projects/dmr170002p/hooten/dmref/gmx21_5.sif

module load gromacs/2018

echo 'running csg_inverse --options "settings.xml"'
## csg_inverse --debug --options settings.xml
csg_inverse --options settings.xml

datadir=ibi-pep-wat-data
cg_dir=/ocean/projects/dmr170002p/hooten/fff/second_cg/forcefield/peptide-peptide/gen1/gridsearch
settings_dir=
mkdir $datadir
for i in {010..150..010}
do
  cd step_$i
  echo 1 1 | mpirun -np 1 gmx_mpi rms -f traj.xtc -s topol.tpr -n index.ndx -pbc yes -o ../$datadir/rms-step_$i.xvg
  echo 7 7 | mpirun -np 1 gmx_mpi rms -f traj.xtc -s topol.tpr -n index.ndx -pbc yes -o ../$datadir/rms-step_$i-bb.xvg
  echo 1 | mpirun -np 1 gmx_mpi gyrate -f traj.xtc -s topol.tpr -n index.ndx -p -nmol 1 -o ../$datadir/rg-step_$i.xvg
  echo 1 1 | mpirun -np 1 gmx_mpi trjconv -f traj.xtc -s topol.tpr -n index.ndx -o trajectory.gro -center -pbc mol
  echo 1 | mpirun -np 1 gmx_mpi gyrate -f trajectory.gro -s topol.tpr -n index.ndx -p -nmol 1 -o ../$datadir/rg_cent-step_$i.xvg
  mkdir dist-step_$i; cd dist-step_$i
  csg_stat --trj ../traj.xtc --cg "../../second_cg_CG.xml;../../water_CG.xml" --top ../topol.tpr --options ../../settings_water.xml
  cd ..
  mv dist-step_$i ../
done

for i in {001..009..001}
do
  cd step_$i
#  echo 1 1 | mpirun -np 1 gmx_mpi rms -f traj.xtc -s topol.tpr -n index.ndx -pbc yes -o ../$datadir/rms-step_$i.xvg
#  echo 7 7 | mpirun -np 1 gmx_mpi rms -f traj.xtc -s topol.tpr -n index.ndx -pbc yes -o ../$datadir/rms-step_$i-bb.xvg
#  echo 1 | mpirun -np 1 gmx_mpi gyrate -f traj.xtc -s topol.tpr -n index.ndx -p -nmol 1 -o ../$datadir/rg-step_$i.xvg
#  echo 1 1 | mpirun -np 1 gmx_mpi trjconv -f traj.xtc -s topol.tpr -n index.ndx -o trajectory.gro -center -pbc mol
#  echo 1 | mpirun -np 1 gmx_mpi gyrate -f trajectory.gro -s topol.tpr -n index.ndx -p -nmol 1 -o ../$datadir/rg_cent-step_$i.xvg
  mkdir dist-step_$i; cd dist-step_$i
  csg_stat --trj ../traj.xtc --cg "../../second_cg_CG.xml;../../water_CG.xml" --top ../topol.tpr --options ../../settings_water.xml
  cd ..
  mv dist-step_$i ..
done
