# Important-tools
These are important tools made by me for working with ORCA (a computational chemistry open source package) in a super-computing environment. They include multiple job submission scripts (BASH), multiple job cancellation (BASH), job setup with different geometries (in python), data extraction (BASH), final optimized geometry extraction (BASH) and many other miscellaneous codes.
#
1. Please uncomment the first few 'for' loops which goes over a number of files or perhaps if you're going to use it for the same purpose update your files indeces and their total numbers. 
2. Also job cancellation and other cluster commands could be different depending on your high performance computing protocol. So please confirm those paritions and clusters before using mine.
3. The Master_Li.py creates and folders and set up XYZ coordinate file, input file (ORCA) and slurm file. You can change the changeXYZ function to suit your needs, same goes for input and slurm file.
