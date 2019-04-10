#!/bin/bash
##### OBJECTIVE IS TO EXTRACT COORDINATES OF LITHIUM ATOMS ALONG WITH THE ENERGY VALUES IN A CSV FILE FROM A FINAL.TRJ FILE#######
typeset -i base
base=24
for ((y=19;y<=24;y++))
do
if [ -f trj_mapper$y.csv ]; then
rm trj_mapper$y.csv
fi
touch trj_mapper$y.csv
cd Li_A$y
Conf=100
for ((k=1;k<=$Conf;k++))
do 
cd C_$k/
if [ -f Final.trj ];then
lines=$(grep -o 'Coordinates from ORCA-job Final E' Final.trj | wc -l)
lines_int=${lines#0}
total=$(awk 'FNR==1 {print $1}' Final.trj )
##### total variable represents the total number of geometry optimization cycles
total=${total#0}
Li_no=$[ $total - $base ]
echo $Li_no
#### Li_no variable has total number of Li in them ####
for ((c=1;c<=$lines_int;c++))  #looping over a number of geometry optimization cycles
do
address=$(pwd | cut -d '/' -f 7- )
echo -n "$c,$address," >> ../../trj_mapper$y.csv
ci=${c#0}
for ((j=1;j<=$Li_no;j++))  #looping over the number of Li atoms to extract their geometry
do 
ji=${j#0}
row=$[ $[ $[ $total + 2] * $[ $ci - 1 ] ] + $base + $ji +2 ]
#echo $row
x_cord=$(awk 'FNR=='$row' {print $2}' Final.trj )
y_cord=$(awk 'FNR=='$row' {print $3}' Final.trj )
z_cord=$(awk 'FNR=='$row' {print $4}' Final.trj )
echo -n "$x_cord,$y_cord,$z_cord," >> ../../trj_mapper$y.csv
done
energy_row=$[ $[ $[ $total + 2 ] * $[ $ci - 1 ] ] + 2 ] 
energy=$(awk 'FNR=='$energy_row' { print $6 }' Final.trj)
echo "$energy " >> ../../trj_mapper$y.csv
#echo "" >> Trial.txt
#echo $energy_row
done
fi
cd ../
done
cd ../
done
