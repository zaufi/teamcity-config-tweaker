What is this
============

TeamCity Configuration Tweaker is a tool aimed to help in mass-editing of build
configurations (via XML files) to do things, that is really hard to do via web UI,
which is mostly *single thing* oriented.

.. note::

    There is no releases yet, so it can't be installed via :command:`pip`.
    So, better way to play w/ this tool is to install it locally after cloning the repository:

    ::

        $ ./setup.py develop --user


Usage Examples
--------------

In my experience, the following shell options are very useful when you want to "select"
files for editting:

    ::

        $ shopt -s extglob globstar nullglob


Add build parameter
^^^^^^^^^^^^^^^^^^^

Select a group of files and check the output result:

::

    $ ls */builtTypes/*Windows_VS14_x64.xml | while read f; do tcct add param build.vs.version 14 $f; done

To add multiple parameters and replace files:

::

    $ ls */*/*VS14_x64.xml | while read f; do tcct add param build.vs.version 14 $f | tcct add param build.vs.year 2015 > $f.tmp && mv $f.tmp $f; done


.. To be continued
