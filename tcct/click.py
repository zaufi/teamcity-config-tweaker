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
import click


# TODO Is there any better way? (w/o global registrations dict)
_registered_aliases = {}


class aliased_group(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        global _registered_aliases

        if cmd_name in _registered_aliases:
            return ctx.command.commands[_registered_aliases[cmd_name]]



def aliases(*args):
    def _inner(fn):
        global _registered_aliases

        prev = len(_registered_aliases)
        _registered_aliases.update({name: fn.__name__ for name in args})
        assert (prev + len(args)) == len(_registered_aliases), 'Non unique aliase?'

        return fn

    return _inner
