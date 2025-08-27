echo "making topol.top. does it look right?"
echo "#include \"martini_v3.0.0.itp\"" > topol.top
echo "#include \"martini_v3.0.0_ions_v1.itp\"" >> topol.top
echo "#include \"martini_v3.0.0_solvents_v1.itp\"" >> topol.top
echo "#include \"molecule_0.itp\"" >> topol.top
echo "#include \"${POLYNAME}.itp\"" >> topol.top
echo >> topol.top

echo "[ system ]" >> topol.top
echo "protein and polymers" >> topol.top
echo >> topol.top

echo "[ molecules ]" >> topol.top
echo "molecule_0 1
CA 1
NA 2
M3POL 100
W 6912" >> topol.top
