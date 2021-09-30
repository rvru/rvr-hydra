## Hydra compiles and disassembles benchmarks for various ISA's and toolchains.


### SUPPORTED TOOLCHAINS:
1.	arm
3.	rvgcc
4.	armgcc


### SUPPORTED BENCHMARKS:
See benchmarks/ directory. To add new benchmarks, follow the steps outlined in
benchmarks/README.


### SETUP:

##### 1. Set up the RISC-V gcc compiler.
Download the [Linux Freedom Studio](https://www.sifive.com/software) package
from SiFive.  Unzip/install Freedom Studio and note the install directory.

Create a new file **rvr-hydra/bin/setup_script_env.bash** based on the provided
template setup_script_env_template.bash. Update the RISC-V gcc executable path
in setup_script_env.bash to point to the RISC-V compiler executables.

##### 2. Set up the ARM gcc compiler.
Download the [GNU Arm Embedded Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads). Unzip and follow the installation instructions.

Update the ARM gcc executable paths in setup_script_env.bash.

##### 3. Set up the ARM compiler (license required).
Depending on your license type and ARM compiler install location, update the
ARM compiler paths, the license file path, and ARM product def in
setup_script_env.bash.

##### 4. Set up a virtual environment 'env' and install Python requirements:
cd rvr-hydra/

virtualenv -p python3 env

source ./env/bin/activate

pip3 install -r requirements.txt

deactivate


### EXECUTION:
##### 1. Activate the virtual environment:
source rvr-hydra/env/bin/activate

##### 2. Add executables to PATH:
source rvr-hydra/bin/setup_script_env.bash

##### 3. Generate the desired disassembly:
On all benchmarks/toolchains at once:
* See the list in hydra/commands/constants.py
* hydra generate [--all | -a]

On a single benchmark:
* hydra generate 'benchmark' 'toolchain'

##### 4. Deactivate the virtual environment:
deactivate
