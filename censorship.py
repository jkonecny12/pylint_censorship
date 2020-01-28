#! /bin/python3

# Pylint censorship -- The smart filtering of false positives for Pylint.
#
# Copyright (C) 2020  Red Hat, Inc.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""This is just an example implementation."""


__all__ = []

import sys

from censorship import CensorshipConfig, CensorshipLinter


class MyConfig(CensorshipConfig):
    """This is basic test class for configuration."""
    def __init__(self):
        super().__init__()

        self.command_line_args = sys.argv[1:]
        self.pylintrc_path = "./pylintrc"

    @property
    def check_paths(self):
        """Get paths to check.

        These can be python modules or files.

        :return: list of paths
        """
        return ["./censorship", __file__]


if __name__ == '__main__':
    config = MyConfig()
    linter = CensorshipLinter(config)

    linter.run()
