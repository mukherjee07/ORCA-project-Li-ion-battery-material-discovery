#!/bin/bash
# Extracting final single point energy from ORCA calculations 
if [ -f top_unsorted.txt ]; then
rm top_unsorted.txt 
fi
touch top_unsorted.txt
for ((c=1;c<=100;c++))
do
cd C_$c
###### READ ONLY IF THE CALCULATION HAS CONVERGED ######
if [ -f Final.xyz ]; then
linec=$(wc -l Orca.out | cut -d ' ' -f 1 )
if [ $linec -gt 3000 ];then 
##### READ THE OUTPUT ONLY IF SCF HAS CONVERGED CONSISTENTLY #####
Fail_No=$(grep -o 'SCF not fully converged!' Orca.out | wc -l)
#echo $Fail_No
Fail_No=${Fail_No#0}
typeset -i zero
zero=0
if [[ $Fail_No -eq $zero ]]; then
Lines=$(grep -n 'FINAL SINGLE POINT ENERGY' Orca.out | tail -1 | cut -d ':' -f 1 )
#echo $lines
Lines=${Lines#0}
ENERGY1=$(awk 'NR=='$Lines' { print $5 }' Orca.out)
#echo $ENERGY1
echo "$c $ENERGY1" >> ../top_unsorted.txt
fi
fi
fi
cd ..
done
if [ -f top_sorted.txt ]; then
rm top_sorted.txt
fi
touch top_sorted.txt
awk '{print $1, $2}' top_unsorted.txt | sort -nk2 > top_sorted.txt
rm top_unsorted.txt
