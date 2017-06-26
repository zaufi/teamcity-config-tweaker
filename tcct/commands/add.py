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
from ..teamcity import load_document

# Standard imports
import click


@click.group()
@click.pass_context
def add(ctx):
    '''
        add various things to project, build configuration or template
    '''
    pass


@add.command()
@click.argument('name')
@click.argument('value')
@click.argument('input', type=click.File('r'), default='-')
@click.pass_context
def param(ctx, name, value, input):
    '''
        add parameter to project, build configuration or template
    '''
    doc = load_document(input)

    ctx.obj.log.debug('Going to add `{}` with value `{}` to {}{}'.
        format(name, value, doc.what, ' `' + doc.name + '`' if doc.name else str()))

    doc.parameters[name] = value

    # Print result
    print(str(doc))
