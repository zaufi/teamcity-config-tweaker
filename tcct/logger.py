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
import logging


def setup_logger(verbose):
    # Create logger
    logger = logging.getLogger('tcct')

    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Create console handler and set level to debug
    handler = logging.StreamHandler()                       # NOTE Write everything to `stderr`!
    handler.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(name)s[%(levelname)s]: %(message)s')
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger
