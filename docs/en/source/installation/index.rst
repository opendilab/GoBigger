Installation
##############

Prerequisites
=================

System version:

    * Centos 7
    * Windows 10
    * MacOS 

Python version: 3.6.8

Get and install GoBigger
=============================

You can simply install GoBigger from PyPI with the following command:

.. code-block:: bash

    pip install gobigger


If you use Anaconda or Miniconda, you can install GoBigger through the following command:

.. code-block:: bash

    conda install -c opendilab gobigger


You can also install with newest version through GitHub. First get and download the official repository with the following command line.

.. code-block:: bash

    git clone https://github.com/opendilab/GoBigger.git

Then you can install from source:

.. code-block:: bash

    # install for use
    # Note: use `--user` option to install the related packages in the user own directory(e.g.: ~/.local)
    pip install . --user
     
    # install for development(if you want to modify GoBigger)
    pip install -e . --user


