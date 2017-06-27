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
@aliases('ed')
@click.pass_context
def edit(ctx):
    '''
        edit various things from a project, build configuration or template
    '''
    pass


@edit.command()
@click.argument('index', type=int)
@click.argument('input', type=click.File('r'), default='-')
@click.pass_context
def runner(ctx, index, input):
    '''
        edit build runner from a build configuration or template
    '''
    doc = load_document(input)

    if doc.what == 'project':
        if ctx.obj.fail_if_missed:
            raise RuntimeError('TeamCity project is not suitable for this operation')
        return

    ctx.obj.log.debug('Edit build runner {} from {}{}'.format(index, doc.what, ' `' + doc.name + '`' if doc.name else str()))

    if index < len(doc.build_runners):
        runner = doc.build_runners[index]

        if 'script.content' in runner.parameters:
            # Launch editor to edit code snippet
            runner.parameters['script.content'].value = click.edit(runner.parameters['script.content'].value, extension='.sh')
            # Flush the result to `STDOUT`
            print(doc)

        else:
            raise RuntimeError('Don\'t know how to edit `{}` of type `{}`'.format(runner.name, runner.type))

    else:
        raise RuntimeError('Build runner index is out of range 0 to {}'.format(len(doc.build_runners) - 1))
