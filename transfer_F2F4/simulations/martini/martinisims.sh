# M3 prep

# martinize a single peptide
martinize2 -f AAF4_1.gro -x AAF4_1_M3.pdb -o topol.top -ff martini3001 -from amber -ignore SOL -ignh

# make the box bigger
gmx editconf -f AAF4_1_M3.pdb -box 4.343 4.343 4.343 -o AAF4_1_434box.gro

gmx insert-molecules -f AAF4_1_434box.gro -ci AAF4_1_M3.pdb -nmol 31 -o F4_32_M3.gro

# antifreeze for Martini 2
gmx insert-molecules -f sol.gro -ci WF.gro -nmol 45 -o sol_withantifreeze.gro -replace

gmx solvate -cp F4_32_M3.gro -cs water.gro -radius 0.21 -o F4_32_M3_solv.gro

gmx grompp -f minim.mdp -c F4_32_M3_solv.gro -p topol.top -o em.tpr

gmx mdrun -pin on -v -deffnm em

# unrestrained NVT equlibration -- allow the system to relax into the box ~lento~
gmx grompp -f nvt2.mdp -c em.gro -p topol.top -o nvt2.tpr
gmx mdrun -ntomp 16 -v -deffnm nvt2

# ~allegro~
gmx grompp -f md.mdp -c nvt2.gro -p topol.top -o md.tpr
gmx mdrun -ntomp 16 -v -deffnm md -cpi md.cpt
