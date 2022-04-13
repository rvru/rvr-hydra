scripts_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Adding $scripts_dir to PATH"
export PATH=${PATH}:${scripts_dir}

echo "Adding RISC-V GNU executable path to PATH"
export PATH=${PATH}:PATH_TO_riscv64-unknown-elf-gcc-xx.x.x-xxxx.xx.x/bin

echo "Adding ARM GNU executable paths to PATH"
export PATH=PATH_TO_gcc-arm-none-eabi-xx-xxxxxx/arm-none-eabi/bin:${PATH}
export PATH=PATH_TO_gcc-arm-none-eabi-xx-xxxxxx/bin:${PATH}

echo "Adding ARM Compiler executable paths to PATH"
export PATH=PATH_TO_ARM_Compiler_5.xx/bin:${PATH}
export PATH=PATH_TO_ARM_Compiler_6.xx/bin:${PATH}

export ARMLMD_LICENSE_FILE=port@host
export ARM_PRODUCT_DEF=IF_NECESSARY_PATH_TO_ARM_TOOL_INSTALL/developmentstudio-xxxx.x-x/sw/mappings/xxxx.elmap

echo "Adding ARM compiler root to PATH"
export ARM_ROOT=PATH_TO_ARM_Compiler_x.xx/
