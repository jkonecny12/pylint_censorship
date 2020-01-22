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

import pylint.lint

from io import StringIO

from pylint.reporters.text import TextReporter


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

    @property
    def check_paths(self):
        """Get paths to check.

        These can be python modules or files.

        :return: string with paths separated by space
        """
        raise AttributeError("No test paths are specified. Please override "
                             "CensoreshipConfig.check_paths property!")


class CensoreshipLinter(object):
    """Run pylint linter and modify it's output."""

    def __init__(self, config):
        """Create CenshoreshipLinter class.

        :param config: configuration class for this Linter
        :type config: CensoreshipConfig class instance
        """
        self._stdout = StringIO()
        self._config = config

    def run(self):
        """Run the pylint static linter.

        :return: return code of the linter run
        :rtype: int
        """
        args = self._prepare_args()

        print("Running pylint with args: ", args)

        pylint.lint.Run(args,
                        reporter=TextReporter(self._stdout),
                        do_exit=False)

        return self._process_output()

    def _prepare_args(self):
        args = []

        if self._config.command_line_args:
            args = self._config.command_line_args

        if self._config.pylintrc_path and "--rcfile" not in args:
            args.append("--rcfile")
            args.append(self._config.pylintrc_path)

        args.append(self._config.check_paths)

        return args

    def _process_output(self):
        stdout = self._stdout.getvalue()
        self._stdout.close()

        if stdout:
            print(stdout)
            return 1

        return 0
