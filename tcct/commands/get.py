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
def get(ctx):
    '''
        get various things from project, build configuration or template
    '''
    pass


@get.command()
@click.argument('name')
@click.argument('input', type=click.File('r'), default='-')
@click.pass_context
def param(ctx, name, input):
    '''
        get parameter value from project, build configuration or template
    '''
    ctx.obj.log.debug('Getting parameter `{}`'.format(name))
    doc = load_entity(input)
    print(str(doc.parameters[name]))
