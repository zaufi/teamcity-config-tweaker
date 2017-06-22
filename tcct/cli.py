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
from .logger import setup_logger
from .version import __version__

# Standard imports
from pkg_resources import iter_entry_points
from click_plugins import with_plugins
import click


class app_data:
    '''
        Class to keep "global" program data and options.

        It'll be assigned to ``click.context.obj`` member, so all commands
        may have access to logging facility or program options.
    '''
    verbose = False
    log = None


@with_plugins(iter_entry_points('tcct.commands'))
@click.group()
@click.option('--verbose', default=False, help='show more details on execution')
@click.version_option(version=__version__, prog_name='TeamCity Configuration Tweaker')
@click.pass_context
def cli(ctx, verbose):
    '''
        Program entry point
    '''
    ctx.obj = app_data()
    ctx.obj.verbose = verbose
    ctx.obj.log = setup_logger(verbose)
