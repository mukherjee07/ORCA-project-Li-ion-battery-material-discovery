#!/bin/bash
Minline=100
touch total_fn.txt 
touch u_fn.txt
cd Li_Atoms/
for ((c=16;c<=18;c++))
do
cd Li_A$c
for ((j=1;j<=20;j++))
do
cd C_$j
if [ -e Orca.out ]; then
NUMLINES=$(wc -l < Orca.out)
echo $NUMLINES
if [ $NUMLINES -le $Minline ]; then
FAULTY_NODES=$(awk 'FNR==6 { print $4 }' Orca.out)
echo $FAULTY_NODES 
echo $FAULTY_NODES >> ../../../total_fn.txt
fi
fi
cd ..
done
cd ..
done
cd ..
awk '{print $1 }' total_fn.txt | sort -u >> u_fn.txt
rm total_fn.txt


