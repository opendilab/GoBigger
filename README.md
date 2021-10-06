## Go-Bigger: Multi-Agent Decision Intelligence Challenge

GoBigger is a **multi-agent** environment for reinforce learning. It is similar to [Agar](https://agar.io/), which is a massively multiplayer online action game created by Brazilian developer Matheus Valadares. In GoBigger, players control one or more circular balls in a map. The goal is to gain as much size as possible by eating food balls and other balls smaller than the player's balls while avoiding larger ones which can eat the player's balls. Each player starts with one ball, but players can split a ball into two once it reaches a sufficient size, allowing them to control multiple balls.

GoBigger allows users to interact with the multi-agent environment easily. Through the given interface, users can get observations by actions created by their policy. Users can also customize their game environments by changing the args in the config.

<div align=center><img width = '640' height ='256' src ="https://github.com/opendilab/GoBigger/blob/main/images/overview.gif"/></div>

## Installation

#### Prerequisites

System version:

    * Centos 7
    * Windows 10
    * MacOS 

Python version: 3.6.8

#### Get and install GoBigger

First get and download the official repository with the following command line.

```
git clone git@github.com:opendilab/GoBigger.git
```

You can install from source:

```
# install for use
# Note: use `--user` option to install the related packages in the user own directory(e.g.: ~/.local)
pip install . --user
     
# install for development(if you want to modify GoBigger)
pip install -e . --user
```

## Resources
For more details, please refer to [GoBigger Doc](https://opendilab.github.io/GoBigger/).

