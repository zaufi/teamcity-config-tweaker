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
import abc
from lxml import etree


class parameter:

    def __init__(self, node):
        self._node = node


    @property
    def name(self):
        assert 'name' in self._node.attrib
        return self._node.get('name')


    @name.setter
    def name(self):
        raise RuntimeError('Setting name is not implemented yet')


    @property
    def value(self):
        assert 'value' in self._node.attrib
        return self._node.get('value')


    @value.setter
    def value(self):
        raise RuntimeError('Setting value is not implemented yet')


    def __str__(self):
        return '{}: {}'.format(self.name, self.value)


    def __repr__(self):
        return '{}=`{}`'.format(self.name, self.value)


class _parameter_iterator:

    def __init__(self, node_iter):
        self._node_iter = node_iter


    def __iter__(self):
        return self


    def __next__(self):
        param_node = next(self._node_iter)
        return parameter(param_node)



class _parameters_dict:

    def __init__(self, node):
        self._node = node


    def __iter__(self):
        return _parameter_iterator(self._node.iterchildren())


    def __getitem__(self, key):
        param = self._node.find('param[@name="{}"]'.format(key))
        if param is not None:
            return parameter(param)

        raise KeyError('Parameter `{}` not found'.format(key))


    def __setitem__(self, key, value):
        param = self._node.find('param[@name="{}"]'.format(key))
        if param is None:
            # Add new item
            self._node.append(etree.Element('param', {'name': key, 'value': value}))
        else:
            # Update existed
            param.attrib['value'] = value


    def __contains__(self, key):
        param = self._node.find('param[@name="{}"]'.format(key))
        return param is not None


    def __len__(self):
        return len(self._node)



class abstract_entity(metaclass=abc.ABCMeta):
    '''
        Class to represent one of configuration entities:

            - project
            - build configuration
            - build template

        It is capable to load/store it from/to XML file and
        exposure ``parameters`` property.
    '''
    def __init__(self, tree):
        self._tree = tree

    @abc.abstractproperty
    def parameters(self):
        pass


    def __str__(self):
        return etree.tostring(self._tree, encoding='UTF-8', pretty_print=True, xml_declaration=True).decode('UTF-8')


class project(abstract_entity):

    def __init__(self, tree):
        super().__init__(tree)


    @property
    def parameters(self):
        params = self._tree.getroot().find('parameters')
        assert params is not None
        return _parameters_dict(params)


class build_configuration(abstract_entity):

    def __init__(self, tree):
        super().__init__(tree)


    @property
    def parameters(self):
        params = self._tree.getroot().find('settings/parameters')
        assert params is not None
        return _parameters_dict(params)


class build_template(abstract_entity):

    def __init__(self, tree):
        super().__init__(tree)


    @property
    def parameters(self):
        params = self._tree.getroot().find('settings/parameters')
        assert params is not None
        return _parameters_dict(params)


def load_entity(file_io):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_io, parser)
    root = tree.getroot()

    # Check what we have:
    if root.tag == 'project':
        cls = project

    elif root.tag == 'build-type':
        cls = build_configuration

    elif root.tag == 'template':
        cls = build_template

    else:
        raise RuntimeError('Unknown XML input')

    return cls(tree)
