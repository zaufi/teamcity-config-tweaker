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


class application_tester:

    @argv('--help')
    @pytest.mark.usefixtures('prepare_cli')
    def help_test(self, capfd):
        cli()

        out, err = capfd.readouterr()
        assert 'Usage:' in out


    @argv('invalid-command')
    @pytest.mark.usefixtures('prepare_cli')
    def invalid_command_test(self, capfd):
        cli()

        out, err = capfd.readouterr()
        assert 'Error: No such command "invalid-command".' in err


    @argv('get', 'param', 'whatever', 'not-existed-file')
    @pytest.mark.usefixtures('prepare_cli')
    def not_existed_file_test(self, capfd):
        cli()

        out, err = capfd.readouterr()
        assert 'Error: Could not open file: not-existed-file: No such file or directory' in err


    @argv('get', 'param', 'whatever', str(make_data_filename('empty.file')))
    @pytest.mark.usefixtures('prepare_cli')
    def invlalid_input_test_1(self, capfd):
        cli()

        out, err = capfd.readouterr()
        assert 'Error: XML syntax error: Document is empty' in err


    @argv('get', 'param', 'whatever', str(make_data_filename('just-a-text.file')))
    @pytest.mark.usefixtures('prepare_cli')
    def invlalid_input_test_2(self, capfd):
        cli()

        out, err = capfd.readouterr()
        assert 'Error: XML syntax error: Start tag expected' in err
