#!/bin/bash
#### FIRST COUNT THE NUMBER OF JOBS CURRENTLY IN CHEMISTRY CLUSTER & BETA PARTITION ####
MAX_JOB=56
typeset -i Count
for ((c=17;c<=20;c++))
do
cd Li_A$c
pwd
for ((j=1;j<=50;j++)) 
do
cd C_$j
pwd
if [ -f Orca.out ]; then
numlines=$(wc -l Orca.out | cut -d ' ' -f 1 )
 if [ $numlines -le 60 ]; then
 Count=0
 else 
 Count=1
 fi
elif [ ! -f Orca.out ]; then
Count=0
fi
while [ $Count -eq 0 ] 
 do
  squeue -M chemistry -p beta -u kmukherj > running.txt
  CUR_JOB=$(wc -l running.txt | cut -d ' ' -f 1 )
  echo $CUR_JOB
  rm running.txt
  #converting CUR_JOB into integer
  CUR_JOB=${CUR_JOB#0}
  if [ $CUR_JOB -le $MAX_JOB ]; then
   sbatch Slurm-beta-orca
   Count=1
  else
   echo "Have to wait lots of job pending"
   sleep 300
  fi
done 
cd ..
done
cd ..
done
#finding the number of remaining jobs
#echo $Count
