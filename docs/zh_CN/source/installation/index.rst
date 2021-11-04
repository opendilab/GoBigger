安装
##############

前置需求
=================

我们已经在以下系统版本中进行过测试:

    * Centos 7
    * Windows 10
    * MacOS 

同时，我们推荐使用 Python 版本为 ``3.6.8``。


快速安装 GoBigger
=============================

我们可以通过 PyPI 直接安装：

.. code-block:: bash

    pip install gobigger

同样，也可以通过 conda 进行安装：

.. code-block:: bash

    conda install -c opendilab gobigger

如果想要使用最新的版本，可以通过源码进行安装。首先，通过 Github 下载 GoBigger 源码。

.. code-block:: bash

    git clone https://github.com/opendilab/GoBigger.git

然后，我们从源代码进行安装。

.. code-block:: bash

    # install for use
    # Note: use `--user` option to install the related packages in the user own directory(e.g.: ~/.local)
    pip install . --user
     
    # install for development(if you want to modify GoBigger)
    pip install -e . --user


