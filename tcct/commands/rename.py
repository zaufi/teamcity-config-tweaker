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

# Standard imports
import click


@click.group()
@aliases('ren')
@click.pass_context
def rename(ctx):
    '''
        rename various things in a project, build configuration or template
    '''
    pass


@rename.command()
@click.option('--force', '-v', default=False, is_flag=True, help='Force override possible existed parameter')
@click.argument('old-name')
@click.argument('new-name')
@click.argument('input', type=click.File('r'), default='-')
@click.pass_context
def param(ctx, force, old_name, new_name, input):
    '''
        rename parameter in a project, build configuration or template
    '''
    doc = load_document(input)

    ctx.obj.log.debug('Going to rename `{}` to `{}` in {}{}'.
        format(old_name, new_name, doc.what, ' `' + doc.name + '`' if doc.name else str()))

    if old_name in doc.parameters:
        '''
            .. todo:: Implement via real replace name attribute of the ``param`` element
        '''
        doc.parameters.rename(old_name, new_name, force_override=force)

    elif ctx.obj.fail_if_missed:
        raise RuntimeError('Parameter `{}` not found in {}{}'.format(old_name, doc.what, ' `' + doc.name + '`' if doc.name else str()))

    # Print result
    print(str(doc))
