.. image:: https://api.travis-ci.org/tzengerink/groceries-cli.svg
  :target: https://travis-ci.org/tzengerink/groceries-cli

.. image:: https://coveralls.io/repos/github/tzengerink/groceries-cli/badge.svg?branch=master
  :target: https://coveralls.io/github/tzengerink/groceries-cli?branch=master

=============
GROCERIES CLI
=============

A command line interface for the `Groceries API <https://github.com/tzengerink/groceries-api>`_.

Installation
------------

To install the ``groceries`` command, use pip::

  sudo pip install https://github.com/tzengerink/groceries-cli/zipball/master

To alter the path of the configuration file, set the ``GROCERIES_CONFIG``
environment variable. For example::

  GROCERIES_CONFIG='/home/johndoe/.groceries.yml'

Development
-----------

After checking out the source, execute ``make install`` to install the
``groceries`` command in the current work directory. The use of a virtualenv
is advised.
