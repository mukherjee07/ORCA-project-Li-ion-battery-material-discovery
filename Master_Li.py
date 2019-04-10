"""
Author :
	 Krishnendu Mukherjee, grad student @University of Buffalo
Objective : 
	To run computational chemistry calculations with ORCA, input (.xyz file, .inp file (having instructions of the simulation),slurm input) of 1-24 number of 
	Li atoms on top of NTCDA and preferabbly half the number of Li ions on top of NTCDA. We will have this number as input
Subprocesses : 
	(i) Take this number N(a) and N(i) as number of Lithium atoms and ions. First make a folder for these two sets of atom types and then the number
	of subfolders requested by the users.
	(ii) Copy input files to these subfolders from head folder.
	(iii) Make changes in these input files ---
	As we are copying these files, after the copying is done we are supposed to be changing these subfolders and then make the following changes ---
		1. Change the multiplicity of .inp files 
		2. Add the the number of Li ions/atoms based on the index number
		3. Change their geometry of Li ions/ atoms 
		4. Change the name of job name and scratch folder in the slurm files
		5. Submit the job slurm job
		6. After submitting the job, come back to the subfolder perhaps
	(iv) Come back to the subfolder. Run parameter_extractor for NBO analysis
"""
#Calling all the important libraries
import math, random
import os
import subprocess
from subprocess import call
import re
import sys
import fileinput
search="Li" # search parameters
scratch="BASEDIR" #directory name to be used in scratch folder
jobname="job-name" # search for slurm identiifer which needs to be changed
XYZ="10_Li.xyz"
xyz="xyzfile"
slurm="slurm-orca"
inp="inp_ut.inp"
j = 0 # Put j = 0 if you don't want the calculations for ions
c = 1 # counter for identifying atoms and ions (for atoms its 1 and for ions its 2), put c=2 if you don't want any atoms at all
k = 17 # DONT TOUCH k is a counter for number of folders to be created
y1 = 24 #y1 is the variable for num of Li atoms folders
y2 = 0 #y2 is the variable for num of Li ions folders
Conf = 100 # Number of Conformers or Instances you want to create
#Charge=0 # DON't change it. The code will automatically change the charge for ions

#Key functions defined in here

def changexyz(file,str1): 

# function for updating the coordinate file with number of desired Li atoms/ions and changing their distance
# Note : this is the most critical function and its objetive are outlined here
# 1. To take a XYZ file as in input from current working directory, to take number of Li atoms/ions to add as str1.
# 2. To make a random guess for only x and y position, z position we will keep at 3 A
# 3. After making the random guess we will make sure that those guesses are at least 2.5 A apart from distance with the previous guess
# 4. After 3 is done satisfactorily we will update the XYZ file with the position
# 5. Steps 2-4 would be carried out for 'str1' number of Li atoms and updated in the XYZ (or coordinate) file

	n = str1
        # making matrix for storing X,Y,Z coordinates
	X = [0 for y in range(n)]
	Y = [0 for y in range(n)]
	Z = [0 for y in range(n)]
	temp_x = 0
	temp_y = 0
	temp_z = 0
	c=0
	x=0
	trial = 0
	 # Counter 
	Dilithium = 2.0 # Li-Li Bond distance
	while (x < n) and trial < 500000:
 		trial +=1
  		#print x
  		Length = 0
  		count = 0
  		#if ( x%2 ==0 ): # Even ones at the bottom of NTCDA plane
  		temp_x = random.uniform(-4.5,4.5)
  		temp_y = random.uniform(-3,3)
  		temp_z = random.uniform(3,5) #fixing Z for this calculations
  		#else:
  		#	temp_x = random.uniform(-5,5)
		#	temp_y = random.uniform(-3,3)
  		#	temp_z = random.uniform(3,5)

  		for y in range(x):
      		# Making sure that the randomly generated coordinates are faraway from previous coordinates
      			Length = math.sqrt((temp_x-X[y])**2.0 + (temp_y-Y[y])**2.0 + (temp_z-Z[y])**2.0)
      			if Length > Dilithium:
          			count = count + 1
                
  		if count == x:
      			 X[x] = temp_x
       		 	 Y[x] = temp_y
      		 	 Z[x] = temp_z
       			 c += 1
       			 x += 1

	#for z in range(x): # You can uncomment this to check the matrices
		#print X[z],Y[z],Z[z],'\n'
	for line in fileinput.input(XYZ,inplace=True): # Replacing the number of atoms 
		print line.replace("24 "+"\n",str(24+n)+" \n"),
	filehandle = open('10_Li.xyz','a') #Appending the xyz file at last section
	for z in range(x):
		filehandle.write("  Li  	"+str(round(X[z],6))+"  	"+str(round(Y[z],6))+"  	"+str(round(Z[z],6))+"\n")
	filehandle.close()

#changexyz(XYZ,10)

def changeslurm(file,str1,str2,pattern1,pattern2,type): # function for updating the slurm file i.e. only the job name part
	for line in fileinput.input(file,inplace=1):
		if pattern1 in line:
			line="#SBATCH --job-name="+type+str(str1)+"C"+str(str2+1)+"\n"
			pass
		sys.stdout.write(line)
		
	for line in fileinput.input(file,inplace=1):
		if pattern2 in line:
			line=re.sub(pattern2,type+str(str1)+"C"+str(str2+1),line)
		sys.stdout.write(line)

def changeinp(file,count,index,xyz): # function for updating the xyz file i.e. only multiplicity is required to change
	Multiplicity = 2
	charge = 0
	if (count == 2):
		Multiplicity = 1
		charge = 1
	else:# if c ==1 charge will remain 0
		if (index % 2 == 0): # Checking if the index number is even
			Multiplicity = 1

	for line in fileinput.input(file,inplace=1):
		if xyz in line:
			line="*xyzfile "+str(charge)+" "+str(Multiplicity)+" 10_Li.xyz"+"\n" 
			pass
		sys.stdout.write(line)	
	
############################################## Main function ############################################

while (c<=2):
	N=0
	# c is the counter to change to atoms or ions
	owd=os.getcwd()
	if (c == 1 and y1 > 0):
		N=y1
		type="Li_A"  # Identifier for Li atoms
		os.mkdir("Li_Atoms_17-24") # Making folder for Li atoms
		os.system('cp slurm-orca 10_Li.xyz inp_ut.inp Li_Atoms_17-24/') #copying relevant files in the sub-directory called Li atoms
		os.chdir("Li_Atoms_17-24") # changing directory to Li atoms
		subhead=os.getcwd() # naming the directory as subhead stands for subheader
	elif (c == 2 and y2 > 0):
		N=y2
		type="Li_I" # Identifier for Li Ions
		os.mkdir("Li_Ions") # Making folder for Li ions
		os.system('cp slurm-orca 10_Li.xyz inp_ut.inp Li_Ions/') #copying relevant files in the sub-directory called Li ions
		os.chdir("Li_Ions") # changing directory to Li ions
		subhead=os.getcwd() # naming the directory as subhead stands for subheader
	while (k <= N): #creating directories, copying files and submitting jobs
	#print(k)
	### note : k is the number of Li atoms or ions ###
		str1=str(k)
		str2=type+str1 # creating folder name
		os.mkdir(str2) # making the directory an e.g. would be Li_A_1 i.e. Li with 1 atom
		os.system('cp ../Min5.sh ../energy_extractor.py '+str2+'/') #Copying energy extractor files
		os.chdir(str2) 
		secondary=os.getcwd() # Li_A_1 is the secondary directory		
		# Now creating 100 folders within the secondary folder Li_A_1 i.e geometric conformers :)
		for z in range(Conf):
			os.mkdir("C_"+str(z+1)) # Making conformer directory like C_1 
			os.chdir("C_"+str(z+1)) # Travelling to the conformer directory
			os.system('cp ../../slurm-orca ../../10_Li.xyz ../../inp_ut.inp ./') #copying relevant files in the directory from subheader
			os.system('pwd') #checking whether we were in the sub-sub-directory or not
			changeslurm(slurm,k,z,jobname,scratch,type) #Now making changes in slurm script in the subdirectory Z_k
			changexyz(XYZ,k) # Similarly making changes in XYZ (coordinate) file in the subdirectory Z_k
			changeinp(inp,c,k,xyz) #It will only change the multiplicity and charge
			#os.system('sbatch slurm-orca') # submitting the job for individual directory Z_k
			os.chdir(secondary) #making the compiler travel in the individual directory
			os.system('pwd') #checking whether we were in the directory or not 
		os.chdir(subhead) # coming back to the subhead folder
		#time.sleep(10) 
		k=k+1 #updating x at the end 
	os.chdir(owd) # coming back to the head folder
	if (j == 1): # only if you want ions to form
		c=c+1 # Updating c and the end
	k=1
	 # changing the value of y1 to y2 after the 1st loop

########################################################     END     ##############################################################
