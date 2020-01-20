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

import pylint.epylint as lint

if __name__ == '__main__':
    # FIXME: Make this dynamic and remove fixed place
    (pylint_stdout, pylint_stderr) = lint.py_run(command_options="./censoreship", return_std=True)

    print(pylint_stdout.read())
