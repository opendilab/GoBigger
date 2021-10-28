.. gobigger documentation master file, created by
   sphinx-quickstart on Fri Aug 27 11:46:57 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GoBigger's documentation!
=========================================

Overview
------------
GoBigger is a **multi-agent** environment for reinforce learning. It is similar to `Agar <https://agar.io/>`_, which is a massively multiplayer online action game created by Brazilian developer Matheus Valadares. In GoBigger, players control one or more circular balls in a map. The goal is to gain as much size as possible by eating food balls and other balls smaller than the player's balls while avoiding larger ones which can eat the player's balls. Each player starts with one ball, but players can split a ball into two once it reaches a sufficient size, allowing them to control multiple balls.

GoBigger allows users to interact with the multi-agent environment easily. Through the given interface, users can get observations by actions created by their policy. Users can also customize their game environments by changing the args in the config.

Indices and tables
=====================

.. toctree::
   :maxdepth: 2

   installation/index

.. toctree::
   :maxdepth: 2

   tutorial/index

.. toctree::
   :maxdepth: 1

   api_doc/index

.. toctree::
   :maxdepth: 1

   faq/index



