# Important-ORCA-tools-for-job-submission-and-property-extraction #
These are important tools made for a project on organic molecule study for Li Ion battery electrode. I was specifically working with ORCA (a computational chemistry open source package) in a high performance computing environment. They include multiple job submission scripts (BASH), multiple job cancellation (BASH), job setup with different geometries (in python), data extraction (BASH), final optimized geometry extraction (BASH) and many other miscellaneous codes.
#
1. Please uncomment the first few 'for' loops which goes over a number of files if you don't need it or perhaps if you're going to use it for the same purpose update your files indices and their total numbers. 
#
2. Also job cancellation and other cluster commands could be different depending on your high performance computing protocol. So please confirm those partitions and clusters before using mine.
#
3. The Master_Li.py creates folders within folders and set up XYZ coordinate file, input file (ORCA) and slurm file. You can change the changeXYZ function to suit your needs, same goes for input and slurm file.
