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
from ..click import aliases, aliased_group
from ..teamcity import load_document

# Standard imports
import click
import tabulate
import textwrap
import pygments
import pygments.lexers
import pygments.formatters


@click.group(cls=aliased_group)
@aliases('list')
@click.pass_context
def ls(ctx):
    '''
        list various things from a project, build configuration or template
    '''
    pass


@ls.command()
@click.option(
    '--headers/--no-headers'
  , ' /-H'
  , default=True
  , is_flag=True
  , help='Show table headers'
  )
@click.option(
    '--style'
  , '-s'
  , type=click.Choice(['plain', 'simple', 'grid', 'jira', 'rst'])
  , default='simple'
  , help='Table style'
  )
@click.argument('input', type=click.File('r'), default='-')
@aliases('p', 'params')
@click.pass_context
def param(ctx, headers, style, input):
    '''
        list parameters from a project, build configuration or template
    '''
    doc = load_document(input)

    ctx.obj.log.debug('List parameters from {}{}'.format(doc.what, ' `' + doc.name + '`' if doc.name else str()))

    _show_parameters(doc.parameters, headers, style)


def _show_parameters(params, headers, style):
    aux = {'tablefmt': style }
    if headers:
        aux['headers'] = ['name', 'value', 'type', 'spec']

    if len(params):
        print(tabulate.tabulate(list(params), **aux))


@ls.command()
@click.option('--details', '-d', default=False, is_flag=True, help='Show details')
@click.argument('input', type=click.File('r'), default='-')
@aliases('ru', 'br')
@click.pass_context
def runners(ctx, details, input):
    '''
        list build runners from a build configuration or template
        TODO Add `OUTPUT` parameter!
    '''
    doc = load_document(input)

    if doc.what == 'project':
        if ctx.obj.fail_if_missed:
            raise RuntimeError('TeamCity project is not suitable for this operation')
        return

    ctx.obj.log.debug('List build runners from {}{}'.format(doc.what, ' `' + doc.name + '`' if doc.name else str()))

    for idx, runner in enumerate(doc.build_runners):
        if details:
            # TODO Get term size?
            print('---{:-<80}'.format('[ ' + '{:02}: '.format(idx) + str(runner) + ' ]'))

            if runner.type == 'simpleRunner':

                if 'teamcity.build.workingDir' in runner.parameters:
                    print('Run at `{}`'.format(runner.parameters['teamcity.build.workingDir'].value))

                if 'command.executable' in runner.parameters:
                    print('Command: {} {}'.format(runner.parameters['command.executable'].value, runner.parameters['command.parameters'].value))

                elif 'script.content' in runner.parameters:
                    script = runner.parameters['script.content'].value
                    lexer = pygments.lexers.get_lexer_by_name('shell', stripall=True)
                    formatter = pygments.formatters.get_formatter_by_name('console')
                    script = pygments.highlight(script, lexer, formatter)
                    print('\n' + script)

                print()

            else:
                # NOTE For other type of runners, just print its parameters
                _show_parameters(runner.parameters, True, 'plain')

        else:
            tail = str()
            if runner.type == 'simpleRunner':
                tail = runner.parameters['command.executable'].value if 'command.executable' in runner.parameters else 'custom script'

            if tail:
                tail = ' ({})'.format(tail)

            print('{:02}: {}{}'.format(idx, str(runner), tail))
