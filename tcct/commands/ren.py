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
from ..teamcity import load_entity

# Standard imports
import click


@click.group()
@click.pass_context
def ren(ctx):
    '''
        add various things to project, build configuration or template
    '''
    pass


@ren.command()
@click.argument('old-name')
@click.argument('new-name')
@click.argument('input', type=click.File('r'), default='-')
@click.pass_context
def param(ctx, old_name, new_name, input):
    '''
        add parameter to project, build configuration or template
    '''
    doc = load_entity(input)

    ctx.obj.log.debug('Going to rename `{}` to `{}` in {}{}'.
        format(old_name, new_name, doc.what, ' `' + doc.name + '`' if doc.name else str()))

    if old_name in doc.parameters:
        '''
            .. todo:: Implement via real replace name of the ``param`` element
        '''
        doc.parameters[new_name] = doc.parameters[old_name].value

    elif ctx.obj.fail_if_missed:
        raise RuntimeError('Parameter `{}` not found in {}{}'.format(old_name, doc.what, ' `' + doc.name + '`' if doc.name else str()))

    # Print result
    print(str(doc))
