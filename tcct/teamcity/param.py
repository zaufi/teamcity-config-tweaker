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
import enum
import functools
import shlex
from lxml import etree

@enum.unique
class parameter_type(enum.IntEnum):
    UNKNOWN = 0
    TEXT = 1
    SELECT = 2
    CHECKBOX = 3
    PASSWORD = 4
    MISSED = -1

    def __str__(self):
        if self == parameter_type.UNKNOWN:
            return 'unknown'

        if self == parameter_type.TEXT:
            return 'text'

        if self == parameter_type.SELECT:
            return 'select'

        if self == parameter_type.CHECKBOX:
            return 'checkbox'

        if self == parameter_type.PASSWORD:
            return 'password'

        if self == parameter_type.MISSED:
            return '-'

        return '<unexpected: {}>'.format(repr(self))


class base_specification(metaclass=abc.ABCMeta):

    def __init__(self, description=None, label=None, display=None, **kwargs):
        self.description = description
        self.label = label
        self.display = False if display == 'hidden' else True


    @abc.abstractmethod
    def kind(self):
        pass


    @abc.abstractmethod
    def __str__(self):
        result = ''

        if self.label:
            result += self.label

        if self.description:
            result += ('\n' if result else '') + self.description

        return result


class text_specification(base_specification):

    def __init__(self, validation_mode=None, **kwargs):
        super().__init__(**kwargs)
        self.validation_mode = validation_mode
        pass

    def kind(self):
        return parameter_type.TEXT


    def __str__(self):
        return super().__str__()


class select_specification(base_specification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


    def kind(self):
        return parameter_type.SELECT


    def __str__(self):
        return super().__str__()


class checkbox_specification(base_specification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


    def kind(self):
        return parameter_type.CHECKBOX


    def __str__(self):
        return super().__str__()


class password_specification(base_specification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


    def kind(self):
        return parameter_type.PASSWORD


    def __str__(self):
        return super().__str__()


class unknown_specification(base_specification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


    def kind(self):
        return parameter_type.UNKNOWN


    def __str__(self):
        return super().__str__()


class missed_specification(base_specification):

    def __init__(self, **kwargs):
        super().__init__()
        pass


    def kind(self):
        return parameter_type.MISSED


    def __str__(self):
        return '-'


class specification:

    _TEXT2TYPE = {
        'text': text_specification
      , 'select': select_specification
      , 'checkbox': select_specification
      , 'password': password_specification
      }

    def __new__(cls, text):
        kind, _, rest = text.partition(' ')
        rest = rest.replace("|'", "&quot;")

        if kind in specification._TEXT2TYPE:
            make_pair = lambda k, _, v: (k, v)
            return specification._TEXT2TYPE[kind](
                **dict([
                    *map(lambda i: make_pair(*i.partition('=')), shlex.split(rest))
                  ])
              )

        return unknown_specification()


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
        if 'value' in self._node.attrib:
            return self._node.attrib['value']

        assert self._node.text

        return self._node.text


    @property
    def spec(self):
        '''
            Read-only `spec` property.
            TODO Make it writable
        '''
        return self.__get_spec()


    @value.setter
    def value(self, val):
        _value = str(val).strip()
        if '\n' in _value:
            # Remove value if present
            if 'value' in self._node.attrib:
                del self._node.attrib['value']
            # Set value as element's text
            self._node.text = etree.CDATA(_value)

        else:
            self._node.attrib['value'] = _value


    def __iter__(self):
        yield self.name
        yield self.value

        my_spec = self.__get_spec()
        yield str(my_spec.kind()) if my_spec is not None else '-'
        yield my_spec if my_spec else '-'


    def __len__(self):
        return 2


    def __str__(self):
        return '{}: {}'.format(self.name, self.value)


    def __repr__(self):
        return '{}=`{}`'.format(self.name, self.value)


    def __get_spec(self):
        '''
            Read-only `spec` property.
            TODO Make it writable
        '''
        if 'spec' in self._node.attrib:
            return specification(self._node.attrib['spec'])

        return missed_specification()


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
        '''
            TODO Validate key?!
        '''
        param = self._node.find('param[@name="{}"]'.format(key))
        if param is not None:
            return parameter(param)

        raise KeyError('Parameter `{}` not found'.format(key))


    def __setitem__(self, key, value):
        '''
            TODO Validate key?!
        '''
        param = self._node.find('param[@name="{}"]'.format(key))

        # Add a new parameter node if not found
        if param is None:
            param = etree.Element('param', {'name': key, 'value': value})
            self._node.append(param)

        parameter(param).value = value


    def __delitem__(self, key):
        '''
            TODO Validate key?!
        '''
        param = self._node.find('param[@name="{}"]'.format(key))
        if param is not None:
            self._node.remove(param)


    def __contains__(self, key):
        param = self._node.find('param[@name="{}"]'.format(key))
        '''
            TODO Validate key?!
        '''
        return param is not None


    def __len__(self):
        return len(self._node)


    def rename(self, old_name, new_name, *, force_override=True):
        if old_name == new_name:
            return

        old_param = self._node.find('param[@name="{}"]'.format(old_name))
        assert old_param is not None

        new_param = self._node.find('param[@name="{}"]'.format(new_name))
        if new_param is None:
            # Ok, just change `name` arrtibute of existed node
            old_param.attrib['name'] = new_name

        elif force_override:
            parameter(new_param).value = parameter(old_param).value
            # Copy `spec` attribute if present
            if 'spec' in old_param.attrib:
                new_param.attrib['spec'] = old_param.attrib['spec']
            # Remove `old` node
            self._node.remove(old_param)

        else:
            raise RuntimeError('Can not rename: parameter `{}` already exists'.format(new_name))


    def clear(self):
        self._node.clear()
