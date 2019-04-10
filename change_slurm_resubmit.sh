#!/bin/bash
cd Li_Atoms
for ((c=16;c<=20;c++))
do
cd Li_A$c
for ((j=1;j<=20;j++))
do
cd C_$j
if [ -e Orca.out ]; then
NUMLINES=$(wc -l < Orca.out)
#echo $NUMLINES
if [ $NUMLINES -le 60 ]; then
#FAULTY_NODES=$(awk 'FNR==6 { print $4 }' Orca.out)
#echo $FAULTY_NODES >> ../../../total_fn.txt
echo "Yo !!! Again resubmitting the job Li $c ions with conformer C_$j with updating slurm-orca"
sed -i 's/cpn-u25-33/cpn-u25-33,cpn-u24-23,cpn-u24-28/' slurm-orca
sbatch slurm-orca
fi
fi
cd ..
done
cd ..
done
cd ..
#awk '{print $1 }' total_fn.txt | sort -u >> u_fn3.txt
#rm total_fn.txt
