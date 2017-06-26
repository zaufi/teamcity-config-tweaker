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
from .click import aliased_group
from .logger import setup_logger
from .version import __version__

# Standard imports
import click
import click_plugins
import pkg_resources


class app_data:
    '''
        Class to keep "global" program data and options.

        It'll be assigned to ``click.context.obj`` member, so all commands
        may have access to logging facility or program options.
    '''
    fail_if_missed = False
    verbose = False
    log = None


@click_plugins.with_plugins(pkg_resources.iter_entry_points('tcct.commands'))
@click.group(cls=aliased_group, context_settings={'help_option_names': ['-h','--help']})
@click.option('--verbose', '-v', default=False, is_flag=True, help='Show more details on execution')
@click.option('--fail-if-missed/--no-fail-if-missed', '-m/-M', default=False, is_flag=True, help='Return failure if something has missed')
@click.version_option(version=__version__, prog_name='TeamCity Configuration Tweaker')
@click.pass_context
def cli(ctx, verbose, fail_if_missed):
    '''
        Program entry point
    '''
    ctx.obj = app_data()
    ctx.obj.fail_if_missed = fail_if_missed
    ctx.obj.verbose = verbose
    ctx.obj.log = setup_logger(verbose)
