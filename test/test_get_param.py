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


class get_parameter_tester:

    @argv('get', 'param', 'test', str(make_data_filename('empty-project-config.xml')))
    @pytest.mark.usefixtures('prepare_cli')
    def not_existed_param_test(self, capfd):
        cli()
        out, err = capfd.readouterr()
        assert len(out.strip()) == 0
        assert len(err.strip()) == 0


    @argv('--fail-if-missed', 'get', 'param', 'test', str(make_data_filename('empty-project-config.xml')))
    @pytest.mark.usefixtures('prepare_cli')
    def fail_if_not_existed_param_test(self, capfd, expected_err):
        cli()
        out, err = capfd.readouterr()
        assert len(out.strip()) == 0
        assert expected_err == err.strip()


    @argv('get', 'param', 'empty-value', str(make_data_filename('multiline-params-project-config.xml')))
    @pytest.mark.usefixtures('prepare_cli')
    def empty_value_test(self, capfd):
        cli()
        out, err = capfd.readouterr()
        assert len(out.strip()) == 0
        assert len(err.strip()) == 0


    @argv('get', 'param', 'some-param', str(make_data_filename('multiline-params-project-config.xml')))
    @pytest.mark.usefixtures('prepare_cli')
    def non_empty_value_test(self, capfd):
        cli()
        out, err = capfd.readouterr()
        assert out.strip() == 'some-value'
        assert len(err.strip()) == 0


    @argv('get', 'param', 'multiline', str(make_data_filename('multiline-params-project-config.xml')))
    @pytest.mark.usefixtures('prepare_cli')
    def multiline_value_test(self, capfd):
        cli()
        out, err = capfd.readouterr()
        assert out.strip() == 'some\ntest\nvalue'
        assert len(err.strip()) == 0
