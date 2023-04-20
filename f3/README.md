# Hybrid CG for Aromatic Peptides - FFF

This repository consists of files required to build and analyze CG models for phenylalanine tripeptides.

Our coarse-graining workflow is: 

1. [AA Reference](AA) : First, we sample trajectories from AA simulations using the Amber99 force field. This repo includes setup files to run 1-peptide and 25-peptide simulations, which are the concentrations used in the Force Field Development sections.

2. Force Field Development: We have used Force Matching (FM) [[1](https://doi.org/10.1021/jp044629q)] and Iterative Boltzmann Inversion (IBI) [[2](https://doi.org/10.1002/1439-7641(20020916)3:9%3C754::AID-CPHC754%3E3.0.CO;2-U),[4](https://doi.org/10.1002/jcc.10307)] to derive CG potentials. Both coarse-graining techniques are implememted using the VOTCA [[3](https://doi.org/10.1021/ct900369w)] package.
    [AR1 ff-development](AR1/ff-development)
    [AR3 ff-development](AR3/ff-development)
    
3. CG Simulation: We have included files required to run CG simulations a single peptide in aqueous solution and for 25 peptides in aqueous solution. Other files are included to allow easy preparation of systems at other concentrations.
    [AR1 simulation](AR1/simulations)
    [AR3 simulation](AR3/simulations)

4. [CG Analysis](analysiis) : We analyze local and overall properties of the CG model. For example, we compare the end-to-end distance of the peptide across AA and CG resolutions. 

## Issues and Support

If you believe you have found a bug, please open a ticket [here](https://github.com/duttm/Hybrid_Bottom-Up_Coarse-Grained_Model_for_Aromatic_Peptides/issues)

For other feedback, please email the authors:

Mason Hooten (Graduate Student): mason.simulation@gmail.com

Meenakshi Dutt (Principal Investigator): meenakshi.dutt@rutgers.edu 

## Acknowledgements

The developers gratefully acknowledge financial support from the National Science Foundation (NSF) CAREER award DMR-1654325 and NSF OAC-1835449, and the use of computational resources enabled via an allocation from NSF ACCESS (allocation DMR-140125).

Thank you for using our coarse-graining toolkit!



