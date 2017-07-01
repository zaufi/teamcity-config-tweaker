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
from .runner import build_runners_collection

# Standard imports
import abc
from lxml import etree


_XML_PI = '<?xml version="1.0" encoding="UTF-8"?>\n'


class abstract_entity(metaclass=abc.ABCMeta):
    '''
        Class to represent one of configuration entities:

            - project
            - build configuration
            - build template

        It is capable to load/store it from/to XML file and
        exposure ``parameters`` property.
    '''
    def __init__(self, tree, what):
        self._tree = tree
        self.what = what


    @property
    def name(self):
        name_node = self._tree.getroot().find('name')
        return name_node.text if name_node is not None else str()


    @abc.abstractproperty
    def parameters(self):
        pass


    @abc.abstractproperty
    def build_runners(self):
        pass


    def __str__(self):
        out = etree.tostring(self._tree, encoding=str, pretty_print=True)
        return _XML_PI + out.replace('/>', ' />')


class project(abstract_entity):

    @property
    def parameters(self):
        params = self._tree.getroot().find('parameters')
        assert params is not None
        return parameters_collection(params)


    @property
    def build_runners(self):
        return []


class build_configuration(abstract_entity):

    @property
    def parameters(self):
        params = self._tree.getroot().find('settings/parameters')
        assert params is not None
        return parameters_collection(params)


    @property
    def build_runners(self):
        runners = self._tree.getroot().find('settings/build-runners')
        return build_runners_collection(runners) if runners is not None else []


class build_template(abstract_entity):

    @property
    def parameters(self):
        params = self._tree.getroot().find('settings/parameters')
        assert params is not None
        return parameters_collection(params)


    @property
    def build_runners(self):
        runners = self._tree.getroot().find('settings/build-runners')
        return build_runners_collection(runners) if runners is not None else []


def load_document(file_io):
    '''
        Factory function to produce one of supported entities:
            - project
            - build configuration
            - build template
    '''
    try:
        parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
        tree = etree.parse(file_io, parser)
        root = tree.getroot()

    except etree.XMLSyntaxError as ex:
        raise RuntimeError('XML syntax error: {}'.format(str(ex)))

    # Check what we have:
    if root.tag == 'project':
        cls = project
        what = 'project'

    elif root.tag == 'build-type':
        cls = build_configuration
        what = 'build configuration'

    elif root.tag == 'template':
        cls = build_template
        what = 'build template'

    else:
        raise RuntimeError('Unknown XML input')

    return cls(tree, what=what)
