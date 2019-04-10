#!/bin/bash
#### THIS CODE WILL EXTRACT THE FINAL GEOMTERY FROM THE ORCA OUTPUT FILE TO RESTART THE GEOMETRY OPTIMIZATION CALCULATION ####
for ((c=17;c<=18;c++))
do
cd Li_A$c
for ((j=53;j<=100;j++))
do
cd C_$j
if [ ! -f Final.xyz ]; then
touch interim.xyz
## getting total numer of optimization cycles in main row variable ##
mainrow=$(grep -n 'GEOMETRY OPTIMIZATION CYCLE' Orca.out | tail -1 | cut -d ':' -f 1 )
echo $mainrow
total=$(awk 'FNR==1 {print $1} ' 10_Li.xyz)
echo $total >> interim.xyz
echo " " >> interim.xyz
rm 10_Li.xyz
total=${total#0}
mainrow=${mainrow#0}
interim=$[ $mainrow + $total + 4 ]
head -$interim Orca.out | tail -$total >> interim.xyz
mv interim.xyz 10_Li.xyz
sbatch slurm-gc-orca
fi
cd ..
done
cd ..
done
