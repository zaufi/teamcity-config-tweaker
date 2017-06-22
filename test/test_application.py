# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Alex Turbov <i.zaufi@gmail.com>
#
# TeamCity Configuration Tweaker is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TeamCity Configuration Tweaker is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

''' Unit tests for application '''

# Project specific imports
from context import argv
from tcct.cli import cli

# Standard imports
import pathlib
import pytest


class application_tester:

    @argv('--help')
    @pytest.mark.usefixtures('prepare_cli')
    def help_test(self, capfd):
        cli()

        out, err = capfd.readouterr()
        assert 'Usage:' in out
