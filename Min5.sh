#!/bin/bash
awk '{print $1, $2}' energyfile.txt | sort -nk2 | head -n 5 > top5.txt
typeset -i LeastE
for ((c=1;c<=5;c++))
do
LeastE=$(awk 'FNR=='$c' {print $1}' top5.txt)
#echo $LeastE
cd C_$LeastE 
pwd

cd ../
done
#rm top5.txt

