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

# Standard imports
from lxml import etree


class parameter:

    def __init__(self, node):
        self._node = node


    @property
    def name(self):
        '''
            Read-only `name` property.
        '''
        assert 'name' in self._node.attrib
        return self._node.get('name')


    @property
    def value(self):
        assert 'value' in self._node.attrib
        return self._node.get('value')


    @value.setter
    def value(self, val):
        self._node.attrib['value'] = str(val)


    def __iter__(self):
        yield self.name
        yield self.value


    def __len__(self):
        return 2


    def __str__(self):
        return '{}: {}'.format(self.name, self.value)


    def __repr__(self):
        return '{}=`{}`'.format(self.name, self.value)


class _parameter_iterator:

    def __init__(self, node_iter, value_transformer):
        self._node_iter = node_iter
        self._value_transformer = value_transformer


    def __iter__(self):
        return self


    def __next__(self):
        param_node = next(self._node_iter)
        param = parameter(param_node)
        return self._value_transformer(param)


class parameters_collection:

    def __init__(self, node):
        self._node = node


    def __iter__(self):
        return _parameter_iterator(self._node.iterchildren(), lambda x: x)


    def items(self):
        return _parameter_iterator(self._node.iterchildren(), lambda x: (x.name, x.value))


    def keys(self):
        return _parameter_iterator(self._node.iterchildren(), lambda x: x.name)


    def __getitem__(self, key):
        param = self._node.find('param[@name="{}"]'.format(key))
        if param is not None:
            return parameter(param)

        raise KeyError('Parameter `{}` not found'.format(key))


    def __setitem__(self, key, value):
        '''
            TODO If value is multiline, it should be added in other way!
        '''
        param = self._node.find('param[@name="{}"]'.format(key))
        if param is None:
            # Add new item
            self._node.append(etree.Element('param', {'name': key, 'value': value}))
        else:
            # Update existed
            param.attrib['value'] = value


    def __delitem__(self, key):
        param = self._node.find('param[@name="{}"]'.format(key))
        if param is not None:
            self._node.remove(param)


    def __contains__(self, key):
        param = self._node.find('param[@name="{}"]'.format(key))
        return param is not None


    def __len__(self):
        return len(self._node)
