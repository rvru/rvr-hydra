scripts_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Adding $scripts_dir to PATH"
export PATH=${PATH}:${scripts_dir}

echo "Adding RISC-V gcc executable path to PATH"
export PATH=${PATH}:/home/jlh24/FreedomStudio/SiFive/riscv64-unknown-elf-gcc-10.1.0-2020.08.2/bin

echo "Adding ARM executable paths to PATH"
export PATH=/home/jlh24/arm/gnu-arm-embedded/gcc-arm-none-eabi-10-2020q4/arm-none-eabi/bin:${PATH}
export PATH=/home/jlh24/arm/gnu-arm-embedded/gcc-arm-none-eabi-10-2020q4/bin:${PATH}
export PATH=/home/jlh24/arm/developmentstudio-2020.1-1/sw/ARMCompiler5.06u7/bin:${PATH}
export ARMLMD_LICENSE_FILE=8224@arm.lic.rice.edu
export ARM_PRODUCT_DEF=/home/jlh24/arm/developmentstudio-2020.1-1/sw/mappings/gold.elmap

echo "Adding ARM compiler root to PATH"
export ARM_ROOT=/home/jlh24/arm/developmentstudio-2020.1-1/sw/ARMCompiler5.06u7/
