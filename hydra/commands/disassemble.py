"""
Disassemble Class.

This class disassembles the assembly into something readable by humans.  It
also defines the default compiler/linker options in get_cc_objdump_optflags().

Contact: jenniferhellar@gmail.com

Authors: Jennifer Hellar
"""
import os

from .base import Base
from .utils import get_cc_objdump_optflags


class Disassemble(Base):
    """Disassemble benchmark and display."""

    def get_makefile_path(self, benchmark_path):
        """Find path to Benchmark's makefile if valid."""
        for root, dirs, files in os.walk(benchmark_path):
            if 'makefile' in files:
                break
        makefile_path = '{}/makefile'.format(root)
        self.check_file_valid(makefile_path)
        return makefile_path

    def get_disassembly(self, benchmark_path, toolchain):
        """Return text file containing generated disassembly."""
        # Make sure input toolchain is supported
        self.check_toolchain_valid(toolchain)

        # Navigate to directory containing makefile
        makefile_path = self.get_makefile_path(benchmark_path)
        os.chdir(os.path.dirname(makefile_path))
        os.system('make clean')

        # Get the compiler, disassembler, and default optimization flags
        # for the given benchmark
        cc, ld, objdump, flags, ldflags = get_cc_objdump_optflags(os.path.basename(benchmark_path), toolchain)

        # Use input optimization flags instead of default optimization flags
        # if there are any present
        requested_opt_flags = self.options['--opt']
        if requested_opt_flags:
            flags = ' '.join(requested_opt_flags)

        command = 'all'

        # Compile with makefile and optimization flags
        os.system('make -f makefile CC={} "CFLAGS={}" {}'.format(cc, '', command))
        artifact = '{}_{}.a'.format(toolchain, os.path.basename(benchmark_path))
        print(artifact)
        assembly_file = '{}_{}_disassembly.txt'.format(toolchain, os.path.basename(benchmark_path))

        # Ensure build artifact generated with makefile execution is valid
        self.check_file_valid(os.path.abspath(artifact))

        # Disassemble build artifact
        os.system('{} -d --section=.text {} > {}'.format(objdump, artifact, assembly_file))

        # Ensure disassembly dump was successful
        self.check_file_valid(os.path.abspath(assembly_file))

        # Inform user that disassembly has been generated
        if self.options['--verbose']:
            print('Disassembly generation successful! The disassembly file, named {}, is stored here: {}' \
                  .format(assembly_file, os.path.dirname(makefile_path)))

        return assembly_file

    def run(self):
        """Create disassembled file."""
        benchmark_path = os.path.abspath(self.options['<benchmark>'])

        # Ensure benchmark directory is valid
        self.check_file_valid(benchmark_path)

        # Generate disassembly
        toolchain = self.options['<toolchain>'].lower()
        assembly_file = self.get_disassembly(benchmark_path, toolchain)
