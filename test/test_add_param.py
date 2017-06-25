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
from context import argv, make_data_filename
from tcct.main import main as cli

# Standard imports
import pathlib
import pytest


class add_parameter_tester:

    @argv('add', 'param', 'test', 'test-value', str(make_data_filename('empty-project-config.xml')))
    @pytest.mark.usefixtures('prepare_cli')
    def to_empty_project_test(self, capfd, expected_out):
        cli()
        out, err = capfd.readouterr()
        assert expected_out == out.strip()


    @argv('add', 'param', 'test', 'test-value', str(make_data_filename('non-empty-params-project-config.xml')))
    @pytest.mark.usefixtures('prepare_cli')
    def to_non_empty_project_test(self, capfd, expected_out):
        cli()
        out, err = capfd.readouterr()
        assert expected_out == out.strip()
