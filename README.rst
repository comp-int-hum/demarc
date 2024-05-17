#####
DeMARC
#####

****************************************************
Resolving and reconstructing information from MARC records
****************************************************

.. _installation:

============
Installation
============

This package can be installed via `pip`.  It's advisable to employ Python `virtual environments <https://docs.python.org/3/library/venv.html>`_ (here and in other situations).  If you will be using the package as a library in your own code, you might create a new directory and set it up by running something like the following::

  $ mkdir my_new_project
  $ cd my_new_project
  $ python3 -m venv local
  $ source local/bin/activate
  $ pip install git+https://github.com/comp-int-hum/demarc.git
