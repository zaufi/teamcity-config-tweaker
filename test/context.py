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

''' Helper functions for tests '''

# Standard imports
import contextlib
import os
import pathlib
import sys


# NOTE DO NOT REMOVE
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_data_dir = pathlib.Path(__file__).parent / 'data'


def data_dir_base():
    return _data_dir


def output_dir_base():
    return data_dir_base() / 'output'


def make_data_filename(filename):
    return data_dir_base() / filename


def argv(*args):
    def _inner(fn):
        setattr(fn, 'argv', args)
        return fn

    return _inner

@contextlib.contextmanager
def change_work_dir(directory):
    assert isinstance(directory, pathlib.Path)
    assert directory.is_dir()

    save_current = pathlib.Path.cwd()
    os.chdir(str(directory))

    try:
        yield

    finally:
        os.chdir(str(save_current))
