#!/bin/bash
#### To Check if the job converged or not (specificially ORCA in GC) ####
K=1
V=1
#cd Li_Atoms
for ((c=23;c<=23;c++))
do
cd Li_A$c
for ((j=1;j<=100;j++)) 
do
cd C_$j
if [ -f Final.xyz ]; then
echo " Li_A$c with conformer number $j has converged"
K=$[$K + $V] 
fi
cd ..
done
cd ..
done
#cd ..
echo "This many number of jobs has converged $K"
