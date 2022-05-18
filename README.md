## Hydra compiles and disassembles benchmarks for various ISA's and toolchains.


### SUPPORTED TOOLCHAINS:
1.	armcc (Arm Compiler 5)
2.	armclang (Arm Compiler 6)
3.	rvgcc
4.	armgcc


### SUPPORTED BENCHMARKS:
See benchmarks/ directory. To add new benchmarks, follow the steps outlined in
benchmarks/README.


### SETUP:

##### 1. Prepare the setup script for toolchain installation paths.

Create a new file **rvr-hydra/bin/setup_script_env.bash** based on the provided template setup_script_env_template.bash. Keep this new file open in the background, as you will be editing it throughout the setup process.

##### 2. Set up the RISC-V gcc compiler.
Download the pre-built [RISC-V GNU toolchain](https://www.sifive.com/software) from the SiFive Software page. Untar the package to the desired install location. Note the directory path e.g. /home/your-username/riscv64-unknown-elf-toolchain-10.2.0-2020.12.8-x86_64-linux-ubuntu14

Edit line 7 of the setup_script_env.bash file with the path to the RISC-V gcc executables.
```console
export PATH=${PATH}:/home/your-username/riscv64-unknown-elf-toolchain-10.2.0-2020.12.8-x86_64-linux-ubuntu14/bin
```


##### 3. Set up the ARM gcc compiler.
Download the pre-built [ARM GNU toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/downloads) from the ARM Developer site. Select the 'AArch32 bare-metal target (arm-none-eabi)' option under 'x86_64 Linux hosted cross toolchains'. Untar the package, move it to the Home directory, and note the directory path as above e.g. /home/your-username/gcc-arm-11.2-2022.02-x86_64-arm-none-eabi

Edit lines 10-11 of setup_script_env.bash with the path to the ARM GNU toolchain.
```console
export PATH=/home/your-username/gcc-arm-11.2-2022.02-x86_64-arm-none-eabi/arm-none-eabi/bin:${PATH}
export PATH=/home/your-username/gcc-arm-11.2-2022.02-x86_64-arm-none-eabi/bin:${PATH}
```


##### 4. Set up the ARM compilers (optional - license required).
Depending on your license type and ARM compiler install location, update the ARM compiler paths, the license file path, and ARM product def in setup_script_env.bash.

###### Typical Arm Compiler 5 (armcc) installation
Download Arm Compiler 5 from the [legacy list](https://developer.arm.com/tools-and-software/embedded/arm-compiler/downloads/legacy-compilers). Untar the downloaded file, navigate to the Installer directory from the Terminal, and execute the installation script using sudo privileges. Follow the prompts to complete installation.
```console
cd Downloads/Installer/
sudo sh setup.sh
```
Recommended install location: /home/your-username/ARM_Compiler_5.xxxx

Update executable permissions and install the required library to run 32-bit executables on a 64-bit machine.
```console
sudo chmod 777 -R /home/your-username/ARM_Compiler_5.xxxx/
sudo apt-get install lib32z1
```

Edit lines 14 and 21 of setup_script_env.bash with the path to the armcc executable and the compiler root directory.
```console
export PATH=/home/your-username/ARM_Compiler_5.xxxx/bin:${PATH}
export ARM_ROOT=/home/your-username/ARM_Compiler_5.xxxx/
```

###### Typical Arm Compiler 6 (armclang) installation
Download [Arm Compiler 6](https://developer.arm.com/tools-and-software/embedded/arm-compiler/downloads/version-6). Untar the downloaded file, navigate to the Installer directory from the Terminal, and execute the installation script using sudo privileges. Follow the prompts to complete installation.
```console
cd Downloads/Installer/
sudo sh setup.sh
```
Recommended install location: /home/your-username/ARM_Compiler_6.xxxx

Update the executable permissions.
```console
sudo chmod 777 -R /home/your-username/ARM_Compiler_6.xxxx/
```

Edit line 15 of setup_script_env.bash with the path to the armclang executable.
```console
export PATH=/home/your-username/ARM_Compiler_6.xxxx/bin:${PATH}
```

###### Update product definition and license information.
Edit lines 17-18 of the setup_script_env.bash file with the appropriate paths to the Arm license port and product definition file e.g. for an ARM DS install,
```console
export ARMLMD_LICENSE_FILE=port@license-server-host
export ARM_PRODUCT_DEF=/home/your-username/arm/developmentstudio-xxxx.x/sw/mappings/gold.elmap
```

##### 5. Set up a virtual environment 'env' and install Python requirements:
(Recommended) Update your Linux installation.
```console
sudo apt update && sudo apt upgrade -y
```

Install Python 3 pip and virtualenv.
```console
sudo apt-get install python3-pip
sudo apt install python3-virtualenv
```

Create the Python virtual environment, activate it, and install dependencies.
```console
cd rvr-hydra/
virtualenv -p python3 env
source ./env/bin/activate
pip3 install -r requirements.txt
deactivate
```


### EXECUTION:
##### 1. Activate the virtual environment and add the toolchain executables to PATH:
```console
source rvr-hydra/bin/setup_script_env.bash
```

##### 2. Generate the desired disassembly:
On all benchmarks/toolchains at once (see the list in hydra/commands/constants.py):
```console
hydra generate [--all | -a]
```

On a single benchmark:
```console
hydra generate [benchmark] [toolchain]
```
e.g.
```console
hydra generate benchmark/fir_filter armgcc
```

##### 4. Deactivate the virtual environment:
```console
deactivate
```
