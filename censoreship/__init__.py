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

__all__ = ["CensoreshipLinter", "CensoreshipConfig"]

import pylint.epylint as lint


class CensoreshipConfig(object):
    """Configuration of False Positives you want to run by Pylint."""
    def __init__(self):
        """Create a configuration object.

        Attributes:

        false_possitives: List of false positives you want to filter out.

        pylintrc_path: Path to the Pylint configuration file. Everything except false positives
                       should be configured there. You can also pass pylintrc as argument to
                       command_line_args in that case the command_line_args rc file will
                       taken instead.

        command_line_args: Pass this list of command_line_args to pylint.
        """
        self.false_positives = []
        self.pylintrc_path = ""
        self.command_line_args = []


class CensoreshipLinter(object):
    """Run pylint linter and modify it's output."""

    def __init__(self, config):
        """Create CenshoreshipLinter class.

        :param config: configuration class for this Linter
        :type config: CensoreshipConfig class instance
        """
        self._stdout = None
        self._stderr = None
        self._config = config

    def run(self):
        """Run the pylint."""
        args = self._prepare_args()

        if args:
            (self._stdout, self._sterr) = lint.py_run(command_options=args, return_std=True)
        else:
            (self._stdout, self._sterr) = lint.py_run(return_std=True)

    def _prepare_args(self):
        if not self._config.command_line_args:
            return ""

        args = self._config.command_line_args

        if self._config.pylintrc_path and "--pylintrc" not in args:
            args.append("--pylintrc")
            args.append(self._config.pylintrc_path)

        if args:
            args = args.join(" ")

        return args
