## This directory contains the benchmarks supported by the Hydra tool.


### To add new benchmarks:
Hydra autogenerates makefiles as long as the benchmark is set up with the correct
directory hierarchy, described in the following steps:

##### 1. Create a folder with the name of the benchmark e.g. fir_filter
mkdir benchmarks/[folder-name]

##### 2. Place all .c and .cpp files in a subfolder named 'src' and all .h files
required in a subfolder named 'inc'

##### 3. Add the benchmark name to the BENCHMARKS variable in hydra/commands/constants.py

Comment out the BENCHMARKS variable for fully supported benchmarks until you have
tested the new benchmark for each toolchain.

Use a temporary BENCHMARKS variable for partially supported benchmarks and add
the new benchmark name to the list.

##### 4. Debugging
If additional/different command line switches or additional libraries are needed
for the new benchmark only, try one of the following:
1. Run Hydra to generate basic makefiles, then edit those makefiles as needed
(it will not overwrite them).
2. Edit hydra/commands/utils.py which specifies compiler flags and creates the 
    makefiles from scratch.
