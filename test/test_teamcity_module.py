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
from context import make_data_filename
from tcct.teamcity import load_document

# Standard imports
import pathlib
import pytest


class teamcity_entities_tester:

    def empty_project_test(self):
        ent = load_document(make_data_filename('empty-project-config.xml').open('r'))

        assert ent.what == 'project'
        assert ent.name == 'Unit Test'
        assert len(ent.parameters) == 0
        assert len(ent.build_runners) == 0


    def non_empty_project_test(self, capfd, expected_out):
        ent = load_document(make_data_filename('non-empty-params-project-config.xml').open('r'))

        params = ent.parameters

        # check __len__
        assert len(params) == 3

        # check iteration protocol
        # - iterate over list of parameters
        for param in params:
            print('param(repr): {}'.format(repr(param)))
            print('param(str): {}'.format(str(param)))

        # - iterate over dict of key-value pairs
        for k, v in params.items():
            print('{}={}'.format(k, v))

        # - iterate over parameter names
        for k in params.keys():
            print('{}'.format(k))

        # check __contains__
        assert 'some-param' in params
        assert 'unknown' not in params

        # check __getitem__
        some = params['some-param']
        assert some.name == 'some-param'
        assert some.value == 'some-value'

        with pytest.raises(KeyError):
            params['unknown']

        # check __setitem__
        # - update existed
        params['some-param'] = 'new-value'
        some = params['some-param']
        assert some.value == 'new-value'

        # check `parameter` conversion to `tuple`
        assert len(some) == 2
        kvp = tuple(some)
        assert kvp[0] == 'some-param'
        assert kvp[1] == 'new-value'

        # check value assign to `parameter`
        some.value = 'new-new-value'

        # check `name` constantness
        with pytest.raises(AttributeError) as ex:
            some.name = 'new'
        assert "can't set attribute" in str(ex)

        # check __setitem__
        # - add a new one
        params['unknown'] = 'now-is-known'
        assert 'unknown' in params
        assert len(params) == 4

        # check __delitem__
        del params['unknown']
        assert len(params) == 3

        out, err = capfd.readouterr()
        assert expected_out == out.strip()


    def multiline_params_project_test(self):
        ent = load_document(make_data_filename('multiline-params-project-config.xml').open('r'))

        params = ent.parameters

        assert len(params) == 3
        assert params['some-param'].value == 'some-value'
        assert params['multiline'].value == 'some\ntest\nvalue'
        assert params['empty-param'].value == ''


    def build_runners_test(self, capfd, expected_out):
        ent = load_document(make_data_filename('sample-build-template.xml').open('r'))

        runners = ent.build_runners

        assert len(runners) == 1

        # Check interation protocol
        for runner in runners:
            print('runner(repr): {}'.format(repr(runner)))
            print('runner(str): {}'.format(str(runner)))

        runner = runners[0]

        # - iterate over dict of key-value pairs
        for k, v in runner.parameters.items():
            print('{}={}'.format(k, v))

        out, err = capfd.readouterr()
        assert expected_out == out.strip()
