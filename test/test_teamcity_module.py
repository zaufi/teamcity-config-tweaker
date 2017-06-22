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
from tcct.teamcity import load_entity

# Standard imports
import pathlib
import pytest


class teamcity_entities_tester:

    def empty_project_test(self):
        ent = load_entity(make_data_filename('empty-project-config.xml').open('r'))

        assert len(ent.parameters) == 0

        assert 0


    def non_empty_project_test(self):
        ent = load_entity(make_data_filename('non-empty-params-project-config.xml').open('r'))

        params = ent.parameters

        # check __len__
        assert len(params) == 3

        # check iteration protocol
        for i in params:
            print('i={}'.format(repr(i)))

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

        # - add a new one
        params['unknown'] = 'now-is-known'
        assert 'unknown' in params
