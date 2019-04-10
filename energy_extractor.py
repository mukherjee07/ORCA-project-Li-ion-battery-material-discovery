"""
Author : Krishnendu Mukherjee, Grad student @University of Buffalo, Chemical & Biological Engineering
Objective : i) To extract Final Single point energy from DFT calculatons in the subfolders named spefically in the format Zx,
where Z detones Z-axis distance of Li atoms from NTCDA plane and x distance the distance in Angstorm
ii) To tabulate all the energy extracted in format like this

Distance (Angstorm)  SPE (hartres)
	1.0		-994.2
	1.1		-995.6
	***		***			
	***		***
NOTE : The objective is to streamline the final fomratted file so that it is easier to plot in MATLAB. (or in python)
"""
import os
import os.path
import re
x = 1
y = 100
n=0

f=open("energyfile.txt","a+") #opening the energyfile. note it it didn't exist python will create it. 
f.write("Distance (Angstorm)  SPE (hartres) \n")  # Writing the table header
f.close()
pattern1 = "ORCA TERMINATED NORMALLY" # Pattern 1 to confirm whether the com	putational chemistry code completed normally 
pattern2 = "FINAL SINGLE POINT ENERGY" # Pattern 2 i.e. a signature to find the final sinal single point energy
flag = 0  # a flag to check if the computational chemistry code has run
# start of the main while loop
while ( x <= y ): #random flag
	#print(x)
	owd=os.getcwd() # current working directory
	str1=str(x)
	str2="C_"+str1

	os.system("pwd")
        if os.path.isdir(str2):
		os.chdir(str2) # Traveling to the inner subdirectory 
		if os.path.isfile("Orca.out"):
			file = open("Orca.out")
			lines=file.readlines()
			for line in lines:
				part = re.split(r'/s',line)
				for p in part:	
					if re.search(pattern1,p):	
						#print"It Seems your computational chemistry code has converged !!!. now we can look for single point energies"
						flag = 1
						break
				else:	
					continue
				break
			# Inner loop for extracting energy only when orca calculations have converged and writing down then final energy value in energyfile.txt
			if flag == 1:
				lines.reverse();
				for line in lines:
					trap = re.split(r'/s',line)
					for t in trap:
						while n == 0:
							if re.search(pattern2,t):
								with open('../energyfile.txt','a') as energy:
									energy.write('\t'+str1+'\t'+'\t'+t[28:])
									print t[28:]
									n=1
								break
							break
					
					
		os.chdir(owd) # coming back to the head folder 
	x=x+1 #updating x at the end 
	n=0 # Updating n again
