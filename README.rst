.. image:: https://api.travis-ci.org/Mytho/groceries-cli.svg
  :target: https://travis-ci.org/Mytho/groceries-cli

.. image:: https://coveralls.io/repos/Mytho/groceries-cli/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/Mytho/groceries-cli?branch=master

=============
GROCERIES CLI
=============

A command line interface for the `Groceries API <https://github.com/Mytho/groceries-api>`_.

Installation
------------

To install the ``groceries`` command, use pip::

  sudo pip install https://github.com/Mytho/groceries-cli/zipball/master

To alter the path of the configuration file, set the ``GROCERIES_CONFIG``
environment variable. For example::

  GROCERIES_CONFIG='/home/johndoe/.groceries.yml'

Development
-----------

After checking out the source, execute ``make install`` to install the
``groceries`` command in the current work directory. The use of a virtualenv
is advised.
