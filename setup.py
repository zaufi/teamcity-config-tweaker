#!/usr/bin/env python3
#
# Install script for TeamCity Configuration Tweaker
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
import tcct

# Standard imports
import pathlib
from setuptools import setup, find_packages


def sources_dir():
    return pathlib.Path(__file__).parent


def readfile(filename):
    with (sources_dir() / filename).open(encoding='UTF-8') as f:
        return f.read()


def get_requirements_from(filename):
    with (sources_dir() / filename).open(encoding='UTF-8') as f:
        return f.readlines()

setup(
    name             = 'teamcity-config-tweaker'
  , version          = tcct.__version__
  , description      = 'TeamCity Configuration Tweaker'
  , long_description = readfile('README.rst')
  , author           = 'Alex Turbov'
  , author_email     = 'I.zaufi@gmail.com'
  , url              = ''
  , download_url     = 'https://github.com/zaufi/teamcity-config-tweaker/archive/release/{}.tar.gz'.format(tcct.__version__)
  , packages         = find_packages(exclude=('test'))
  , entry_points       = {
        'console_scripts': [
            'tcct = tcct.main:main'
          ]
      , 'tcct.commands': [
            'add = tcct.commands.add:add'
          , 'get = tcct.commands.get:get'
          , 'ls = tcct.commands.ls:ls'
          , 'rm = tcct.commands.rm:rm'
          , 'ren = tcct.commands.ren:ren'
          ]
      }
  , license          = 'GNU General Public License v3 or later (GPLv3+)'
  , classifiers      = [
        'Development Status :: 4 - Beta'
      , 'Intended Audience :: Developers'
      , 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
      , 'Natural Language :: English'
      , 'Programming Language :: Python :: 3'
      ]
  , keywords         = 'teamcity'
  , install_requires = get_requirements_from('requirements.txt')
  , test_suite       = 'test'
  , tests_require    = get_requirements_from('test-requirements.txt')
  , zip_safe         = True
  )
