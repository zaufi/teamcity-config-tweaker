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
# NOTE Import `context` module first, so it can update system paths!
from context import change_work_dir, expected_results_dir, output_dir
from tcct.cli import cli

# Standard imports
import pathlib
import pytest
import sys
import unittest.mock
import warnings


# Add CLI option
def pytest_addoption(parser):
    parser.addoption(
        '--save-patterns'
      , action='store_true'
        # TODO Better description
      , help='store matching patterns instead of checking them'
      )


#BEGIN Module level fixtures

#@pytest.fixture(scope='module', autouse=True)
#def update_environment(request):
    #'''
        #Set/update environment variables from :var:`ENV` dict declared at module level
    #'''
    #env = getattr(request.module, 'ENV', dict())

    #_save, _del = modify_environment(env)

    #yield

    #if _save or _del:
        #restore_environment(_save, _del)


#END Module level fixtures

#BEGIN Class level fixtures

#@pytest.fixture(scope='class')
#def class_environment(request):
    #'''
        #Update environment for class methods.

        #Environment will be updated from the class's :var:`ENV` data member,
        #which must have a type dict of strings.
    #'''
    #_save, _del = modify_environment(getattr(request.cls, 'ENV', dict()))

    #yield

    #if _save or _del:
        #restore_environment(_save, _del)

#END Class level fixtures

#BEGIN Function level fixtures

@pytest.fixture
def prepare_cli(request, monkeypatch):
    '''
        Prepare CLI parameters to ``sys.args``.
        Prevent ``argparse`` to exit if "serivce" options found (like ``--help`).
    '''
    # Initial CLI parameters
    argv = ['tcct']

    # Try to add parameters from test class, if present
    if request.cls is not None and hasattr(request.cls, 'argv'):
        argv += request.cls.argv

    # Now try to collect parameters given to test method via :fun:`argv` decorator
    if hasattr(request.function, 'argv'):
        argv += request.function.argv

    print('Gathered CLI args:\n{}'.format(repr(argv)))

    # Patch ``sys`` module, so ``click`` would see collected parameters
    monkeypatch.setattr(sys, 'argv', argv)
    # Prevent ``click`` from calling ``exit`` function in case of CLI errors
    monkeypatch.setattr(sys, 'exit', lambda *args, **kwargs: 0)

    return None


@pytest.fixture
def output_dir(request):
    '''
        Make sure the output directory for a given test case is:

        * present
        * fresh -- i.e. no files in it

        Base directory is :file:`${srcdir}/test/data/output/`.
        Also this fixture takes care about *build directory*, if test simulate
        running under TeamCity.
    '''
    result = pathlib.Path(
        output_dir()
      , request.module.__name__
      )
    if request.cls is not None:
        result /= request.cls.__name__

    result /= request.function.__name__

    return result


class _content_check_or_store_pattern:

    def __init__(self, filename, store):
        self._filename = filename
        self._store = store


    def _store_pattern_handle_error(fn):
        def _inner(self, text):
            # Check if `--save-patterns` has given to CLI
            if self._store:
                # Make directory to store pattern file if it doesn't exist yet
                if not self._filename.parent.exists():
                    self._filename.parent.mkdir(parents=True)

                # Store!
                self._filename.write_text(text)
                return True

            # Ok, this is the "normal" check:
            # - make sure the pattern file exists
            if not self._filename.exists():
                warnings.warn('Pattern file not found `{}`'.format(self._filename), RuntimeWarning)
                return False

            # - call wrapped function to
            return fn(self, text)

        return _inner


    @_store_pattern_handle_error
    def __eq__(self, text):
        expected_text = self._filename.read_text().strip()
        return expected_text == text


    @_store_pattern_handle_error
    def match(self, text):
        content = ' '.join(self._filename.read_text().strip().splitlines())
        what = re.compile(content)
        transformed_text = ' '.join(text.splitlines())
        return bool(what.match(transformed_text))



def _make_expected_filename(request, ext: str) -> pathlib.Path:
    result = expected_results_dir()

    if request.cls is not None:
        result /= request.cls.__name__

    result /= request.function.__name__ + ext

    return result


@pytest.fixture
def expected_out(request):
    return _content_check_or_store_pattern(
        _make_expected_filename(request, '.out')
      , request.config.option.save_patterns
      )


@pytest.fixture
def expected_err(request):
    return _content_check_or_store_pattern(
        _make_expected_filename(request, '.err')
      , request.config.option.save_patterns
      )

#END Function level fixtures
