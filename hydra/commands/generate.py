"""
Tool that runs and combines all of the different sub-commands.

Contact: jenniferhellar@gmail.com

Authors: Jennifer Hellar
"""
import os

from .constants import BENCHMARKS, SUPPORTED_TOOLCHAINS
from .disassemble import Disassemble
from .utils import create_makefiles


class Generate(Disassemble):
    """Generate class, runs all sub-commands on given benchmarks and toolchains."""

    def run(self):
        """Public class, runs the generate command."""
        cwd = os.getcwd()

        # Code to find/create makefiles for all of the benchmarks:
        create_makefiles(cwd, SUPPORTED_TOOLCHAINS, self.options['--verbose'])

        if self.options['--all']:
            # Run every benchmark and every toolchain
            for benchmark in BENCHMARKS:
                self.call_disassembly(os.path.join('benchmarks', benchmark), cwd)
        else:
            self.call_disassembly(self.options['<benchmark>'], cwd)

    def call_disassembly(self, benchmark, cwd):
        """Determine which toolchain(s) to run on the given benchmark."""
        os.chdir(cwd)
        benchmark_path = os.path.abspath(benchmark)

        super(Disassemble, self).check_file_valid(benchmark_path)

        # Run all toolchains for specified benchmark:
        if self.options['--all']:
            first_toolchain = True
            for toolchain in SUPPORTED_TOOLCHAINS:
                self.get_disassembly(benchmark_path, toolchain)
        else:
            toolchain = self.options['<toolchain>'].lower()
            self.get_disassembly(benchmark_path, toolchain)
