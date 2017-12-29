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

# Project specific imports
from .param import parameters_collection

# Standard imports


class build_runner:

    def __init__(self, node):
        self._node = node


    @property
    def name(self):
        return self._node.attrib['name']


    @name.setter
    def name(self, new_name):
        '''
            TODO Verify name parameter? (string type, non empty, not a multiline, ...)
        '''
        self._node.attrib['name'] = new_name


    @property
    def type(self):
        '''
            TODO Add `enum` for this...
        '''
        return self._node.attrib['type']


    @property
    def parameters(self):
        params = self._node.find('parameters')
        assert params is not None
        return parameters_collection(params)


    def __str__(self):
        return '{}: {} [{}]'.format(self.type, self.name if self.name else '<unnamed>', self._node.attrib['id'])


    def __repr__(self):
        return '{} [{}, {}]'.format(repr(self.name), self.type, self._node.attrib['id'])


class _build_runner_iterator:

    def __init__(self, node_iter):
        self._node_iter = node_iter


    def __iter__(self):
        return self


    def __next__(self):
        runner_node = next(self._node_iter)
        return build_runner(runner_node)



class build_runners_collection:

    def __init__(self, node):
        self._node = node


    def __iter__(self):
        return _build_runner_iterator(self._node.iterchildren())


    def __getitem__(self, index):
        if index < len(self._node):
            return build_runner(self._node[index])

        raise IndexError('Requested index is out of range')


    def __setitem__(self, index, value):
        assert 0, 'Runners collection do not support set item! Code review required!'


    def __len__(self):
        return len(self._node)
