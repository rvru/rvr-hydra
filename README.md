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

Update the RISC-V gcc executable path in
risc-v-analyzer/bin/setup_script_env.bash to point to the compiler executables
e.g. /home/jlh24/FreedomStudio/SiFive/riscv64-unknown-elf-gcc-10.1.0-2020.08.2/bin

##### 2. Set up the ARM gcc compiler.
Download the [GNU Arm Embedded Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads).
Unzip and follow the installation instructions.

Update the ARM gcc executable paths in rvr-hydra/bin/setup_script_env.bash e.g.
/home/jlh24/arm/gnu-arm-embedded/gcc-arm-none-eabi-10-2020q4/arm-none-eabi/bin
and
/home/jlh24/arm/gnu-arm-embedded/gcc-arm-none-eabi-10-2020q4/bin

##### 3. Set up the ARM compiler (license required).
Depending on your license type and ARM compiler install location, update the
ARM compiler executable path, the license file path, and ARM product def.

Additionally, in hydra/commands/utils.py function write_sub_makefiles(), update
the ARM_ROOT (line 205) with the compiler path e.g.
/home/jlh24/arm/developmentstudio-2020.1-1/sw/ARMCompiler5.06u7/

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
