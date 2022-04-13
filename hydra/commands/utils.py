"""
Utility Functions

This file contains multiple different utility functions used by the program,
these functions are listed below:

Makefile Creator:
These functions create makefiles for benchmarks given that the makefiles
don't already exist. This allows for the addition of new benchmarks or toolchains
to this tool without having to remember to write custom makefiles every time.

IMPORTANT NOTE: this function assumes that all benchmarks added have all of their
source code in a folder named 'src' and that all benchmarks added have all their
dependencies included in a folder named 'inc'.
Additionally, when a new benchmark is added, its folder name needs to be added to
the constant variables BENCHMARKS in constants.py.

Contact: jenniferhellar@gmail.com

Authors: Jennifer Hellar
"""
import os
import sys

from .constants import BENCHMARKS

def get_cc_objdump_optflags(benchmark_name, toolchain):
        """
        Return parameters for given toolchain.

        Returns the compiler, disassembler, and default optimization
        flags for the given toolchain.
        """
        if toolchain == 'arm':
            cc = 'armcc'
            ld = 'armar'
            objdump = 'objdump'
            ARM_ROOT = os.environ.get('ARM_ROOT')
            ccflags = '-c --preinclude=' + ARM_ROOT + 'include/stdint.h --cpu=Cortex-M0plus --c99 --no-inline -O2 -Ospace'
            # ccflags = '-c --preinclude=$(ARM_ROOT)include/stdint.h --cpu=Cortex-M4 --c99 --no-inline -O2 -Ospace'
            ldflags = '-r'
        elif toolchain == 'rvgcc':
            cc = 'riscv64-unknown-elf-gcc'
            ld = 'riscv64-unknown-elf-gcc'
            objdump = 'riscv64-unknown-elf-objdump'
            ccflags = '-c -std=c99 -march=rv32imc -mabi=ilp32 -msave-restore -fno-inline -O2 -Os'
            ldflags = '-nostartfiles -march=rv32imc -mabi=ilp32 -o'
        elif toolchain == 'armgcc':
            cc = 'arm-none-eabi-gcc'
            ld = 'arm-none-eabi-gcc'
            objdump = 'objdump'
            ccflags = '-c -mthumb -mtune=cortex-m0plus -std=c99 -O2 -Os'
            ldflags = '-nostartfiles -o'
        elif toolchain == 'armclang':
        	cc = 'armclang'
        	ld = 'armar'
        	objdump = 'objdump'
        	ccflags = '-c -target=arm-arm-none-eabi -mthumb -mcpu=Cortex-M0plus -std=c99 -fno-inline-functions -Oz'
        	ldflags = '-r'

        return cc, ld, objdump, ccflags, ldflags

def create_makefiles(cwd, toolchains, verbose):
    """
    Create New Makefiles.

    Handler function to autogenerate makefiles for new benchmarks. Checks all
    of the benchmark files within risc-v-benchmarks that should be passed in
    as cwd and determines whether they already have makefiles. For each file,
    if it does nothing happens, if the benchmark does not have makefiles, this
    function autogenerates them.

    NOTE: For this function to work, the benchmark must be formatted in such a way
    that all .c and .cpp files are in a sub-folder called src and all .h files are
    in a sub-folder called inc.
    """
    sub_directories = [x[0] for x in os.walk(cwd)]

    cwd_parts = cwd.split('/')

    try:
        for sub_path in sub_directories:
            sub_split = sub_path.split('/')
            if sub_split[len(sub_split) - 1] not in BENCHMARKS:
                continue

            benchmark_name = sub_split[len(sub_split) - 1]

            os.chdir(sub_path)
            sub_files = [f for f in os.listdir(sub_path) if os.path.isfile(os.path.join(sub_path, f))]

            files_already_exist = True
            if 'makefile' in sub_files:
                for tool in toolchains:
                    if tool == 'arm':
                        tool = 'armcc'
                    sub_makefile_name = tool + '.mk'
                    if sub_makefile_name not in sub_files:
                        files_already_exist = False
                        break
            else:
                files_already_exist = False

            if files_already_exist:
                os.chdir(cwd)
                continue

            if verbose:
                print("Generating new makefiles for the benchmark: {}".format(benchmark_name))

            write_main_makefile(cwd, sub_path, benchmark_name, toolchains, verbose)
            for tool in toolchains:
                toolchain = tool
                if tool == 'arm':
                    tool = 'armcc'
                sub_makefile_name = tool + '.mk'
                if verbose:
                    print("Generating {} for {}".format(sub_makefile_name, benchmark_name))
                write_sub_makefiles(benchmark_name, sub_makefile_name, toolchain)

            os.chdir(cwd)

    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

def write_main_makefile(cwd, sub_path, benchmark_name, toolchains, verbose):
    """
    Make The Parent Makefile.

    Makes the benchmark's main makefile named 'makefile' that handles all of
    the general makefile duties and imports all of the sub-makefiles

    cwd: the current working directory of the overarching system (risc-v-benchmarks)
    sub_path: the directory of the specific benchmark the makefile is being created for
    benchmark_name: the nqme of the current benchmark
    toolchains: list of the toolchains
    """
    source_path = sub_path + '/src'

    source_files = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))]
    source_files = [f for f in source_files if f.split('.')[1] == 'c' or f.split('.')[1] == 'cpp']

    if verbose:
        print("Creating the main makefile for {}".format(benchmark_name))

    with open('makefile', 'w+') as makefile:
        makefile.write('THIS_DIR=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))\n')
        makefile.write('SDK_ROOT=$(THIS_DIR)\n')
        makefile.write(benchmark_name.upper() + '_LIB_PATH=$(THIS_DIR)src\n\n')

        for i in range(len(toolchains)):
            tool = toolchains[i]

            cc, ld, objdump, flags, ldflags = get_cc_objdump_optflags(benchmark_name, tool)
            if tool == 'arm':
                tool = 'armcc'
            tool = tool + '.mk'

            if i == 0:
                makefile.write('ifeq ($(CC),' + cc + ')\n')
                makefile.write('\t-include ' + tool + '\n')
            else:
                makefile.write('else ifeq ($(CC),' + cc + ')\n')
                makefile.write('\t-include ' + tool + '\n')
        makefile.write('endif\n\n')

        sub_directories = [x[0] for x in os.walk(cwd)]
        sub_directories_names = []
        for sub in sub_directories:
            sub_split = sub.split('/')
            directory_name = sub_split[len(sub_split) - 1]
            sub_directories_names.append(directory_name)

        if 'src' not in sub_directories_names:
            raise Exception("There is no src directory in this directory")

        inc_included = False
        if 'inc' in sub_directories_names:
            inc_included = True

        makefile.write('INCLUDES := $(' + benchmark_name.upper() + '_LIB_PATH)')
        if inc_included:
            makefile.write(' \\\n')
            makefile.write('$(SDK_ROOT)inc')
        makefile.write('\n\n')

        makefile.write('INC_PARAMS=$(foreach d, $(INCLUDES), -I$d)\n')
        makefile.write('$(info INC_PARAMS=$(INC_PARAMS))\n\n')

        makefile.write('LIB_PARAMS=$(foreach d, $(LIBS), -L$d)\n')
        makefile.write('RM = rm -rf\n\n')

        makefile.write('OBJS = $(' + benchmark_name.upper() + '_LIB_PATH)/')
        for i in range(len(source_files)):
            file_parts = source_files[i].split('.')
            file_name = file_parts[0] + '.o'
            if i < len(source_files) - 1:
                makefile.write(file_name + ' \\\n')
                makefile.write('$(' + benchmark_name.upper() + '_LIB_PATH)/')
            else:
                makefile.write(file_name + '\n\n')

        makefile.write('all: $(TARGET)\n\n')

        makefile.write('$(TARGET): $(OBJS)\n')
        makefile.write('\t$(LD) $(LDFLAGS) $(TARGET) $(OBJS) $(LIB_PARAMS)\n\n')

        makefile.write('.c.o:\n')
        makefile.write('\t$(CC) $(CFLAGS) $(INC_PARAMS) -o $@ $<\n\n')

        makefile.write('clean:\n')
        makefile.write('\t-$(RM) $(TARGET) $(OBJS)\n\n')

        makefile.write('.PHONY: clean all\n')

def write_sub_makefiles(benchmark_name, file_name, toolchain):
    """
    Write Each Sub-Makefile.

    This function creates individual makefiles that define the compilation rules for
    each individual toolchain per benchmark.

    benchmark_name: name of the current benchmark
    file_name: <toolchain>.mk, the name of the makefile being generated
    toolchain: the toolchain for the current makefile
    """
    cc, ld, objdump, ccflags, ldflags = get_cc_objdump_optflags(benchmark_name, toolchain)

    with open(file_name, 'w+') as makefile:
        if toolchain == 'arm':
            makefile.write('ARM_ROOT=' + os.environ.get('ARM_ROOT') + '\n\n')

        makefile.write('CC = ' + cc + '\n')
        makefile.write('override CFLAGS += ' + ccflags + '\n')
        makefile.write('LD = ' + ld + '\n')
        makefile.write('LDFLAGS = ' + ldflags + '\n')
        makefile.write('TARGET = ' + toolchain + '_' + benchmark_name + '.a\n')
