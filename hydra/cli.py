"""
Hydra.

Usage:
    hydra generate [<benchmark>] [<toolchain>] [--opt <optimization_flag>] [-a | --all] [-v | --verbose]
    hydra (-h | --help)

Options:
    --opt <optimization_flag>         The optimization flag(s) to use when compiling.
    -h --help                         Show this screen.
    -a --all                          Run all benchmarks on all toolchains.
    -v --verbose                      Print what files are being created, and to where.

Examples:
    hydra generate fir_filter arm

Contact: jenniferhellar@gmail.com

Authors: Jennifer Hellar.
"""
import sys

from inspect import getmembers, isclass
from docopt import docopt

def main():
    """CLI entrypoint."""
    import commands
    try:
        options = docopt(__doc__)

        if not options['--all']:
            if options['<benchmark>'] is None or options['<toolchain>'] is None:
                raise Exception('If --all is not flagged, both <benchmark> and <toolchain> must be defined.')

        # Here we'll try to dynamically match the command the user is trying to run
        # with a pre-defined command class we've already created.
        for tag, value in options.items():
            if hasattr(commands, tag) and value:
                module = getattr(commands, tag)
                commands = getmembers(module, isclass)
                command_function = None
                for command in commands:
                    if command[0].lower() == tag.lower():
                        command_function = command[1]

                if not command_function:
                    raise Exception('Command: {} not registered'.format(tag))

                command_object = command_function(options)
                command_object.run()
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

    print("\nProgram Completed Successfully\n")
    sys.exit(0)
