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
from ..click import aliases
from ..teamcity import load_document

# Third-party imports
import click

# Standard imports
import fnmatch


@click.group()
@aliases('rm', 'del')
@click.pass_context
def remove(ctx):
    '''
        remove various things from a project, build configuration or template
    '''
    pass


@remove.command()
@click.argument('name')
@click.argument('input', type=click.File('r'), default='-')
@click.pass_context
def param(ctx, name, input):
    '''
        remove parameter from a project, build configuration or template
    '''

    doc = load_document(input)

    ctx.obj.log.debug('Removing parameter `{}` from {}{}'.format(name, doc.what, ' `' + doc.name + '`' if doc.name else str()))

    if name in doc.parameters:
        del doc.parameters[name]

    elif ctx.obj.fail_if_missed:
        raise RuntimeError('Parameter `{}` not found in {}{}'.format(name, doc.what, ' `' + doc.name + '`' if doc.name else str()))

    # Print result
    print(str(doc))


@remove.command()
@click.argument('pattern')
@click.argument('input', type=click.File('r'), default='-')
@click.pass_context
def params(ctx, pattern, input):
    '''
        remove parameters matching a given pattern from a project,
        build configuration or template

        TODO Tests
    '''

    doc = load_document(input)

    ctx.obj.log.debug('Removing parameters matching pattern `{}` from {}{}'.format(pattern, doc.what, ' `' + doc.name + '`' if doc.name else str()))

    if pattern == 'all' or pattern == '*':
        doc.parameters.clear()
    else:
        for param in doc.parameters:
            if fnmatch.fnmatch(param.name, pattern):
                ctx.obj.log.debug('Removing `{}`'.format(param.name))
                del doc.parameters[param.name]

    # Print result
    print(str(doc))
