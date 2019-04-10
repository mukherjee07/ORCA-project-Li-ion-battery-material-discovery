#!/bin/bash
count=0
num=1
test="Li_I"
squeue -p general-compute -u kmukherj > BHAi_TEST.txt
numlines=$(wc -l < BHAi_TEST.txt)
echo $numlines
for ((c=1;c<=$numlines;c++))
do
job_name=$(awk 'FNR=='$c' {print $3}' < BHAi_TEST.txt)
field=${job_name:0:4}
if [[ $field == $test ]]; then
 job_id=$(awk 'FNR=='$c' {print $1}' < BHAi_TEST.txt)
#echo $job_id
 count=$[count + num]
 scancel -p general-compute $job_id
fi
done
echo $count
rm BHAi_TEST.txt
