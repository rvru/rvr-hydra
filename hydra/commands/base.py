"""
Base class and BaseError class.

Definitions for both the Base class, an abstract parent class
for all the other commands, as well as constant variables used
throughout the program, and a custom error class: BaseError.

Contact: jenniferhellar@pm.me

Authors: Jennifer Hellar, Colin Page
"""
import os
import sys

from .constants import SUPPORTED_TOOLCHAINS


class BaseError(Exception):
    """Generic Exception class for handling errors."""

    def __init__(self, msg):
        """Print error message, exit program."""
        super()
        print('ERROR: ' + str(msg))
        sys.exit(1)


class Base():
    """
    Basic form of command.

    Creates structure for other command classes to follow by
    allowing all command classes to have access to the passed
    in arguments as well as file and toolchain validity checking
    functions.
    """

    def __init__(self, options, *args, **kwargs):
        """All commands have access to options defined by user."""
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def check_file_valid(self, file_path):
        """Check if file exists and is not empty."""
        file_name = os.path.basename(file_path)
        if not os.path.exists(file_path):
            raise BaseError('File {} does not exist'.format(file_name))

        if not os.path.getsize(file_path) > 0:
            raise BaseError('File {} is empty'.format(file_name))

    def check_toolchain_valid(self, toolchain):
        """Check if toolchain supported."""
        toolchain = toolchain.lower()
        input_toolchain_supported = False
        for tool in SUPPORTED_TOOLCHAINS:
            if toolchain == tool:
                input_toolchain_supported = True

        if input_toolchain_supported is False:
            raise BaseError('Requested toolchain {} is not supported by Hydra. Supported toolchains are: {}' \
                            .format(toolchain, ', '.join(SUPPORTED_TOOLCHAINS)))

    def run(self):
        """Conceptually pure virtual function for override in child classes."""
        raise NotImplementedError('Subclass Base and implement run!')
