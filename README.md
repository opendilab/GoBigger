# Go-Bigger: Multi-Agent Decision Intelligence Environment

[![PyPI](https://img.shields.io/pypi/v/gobigger)](https://pypi.org/project/gobigger/)
[![Anaconda-Server Badge](https://anaconda.org/opendilab/gobigger/badges/version.svg)](https://anaconda.org/opendilab/gobigger)
[![Read the Docs](https://img.shields.io/readthedocs/gobigger)](https://gobigger.readthedocs.io/en/latest/?badge=latest)
[![Read the Docs](https://img.shields.io/readthedocs/gobigger?label=%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3)](https://gobigger.readthedocs.io/zh_CN/latest/?badge=latest)
[![unit_test](https://github.com/opendilab/GoBigger/actions/workflows/unit_test.yml/badge.svg?branch=main)](https://github.com/opendilab/GoBigger/actions/workflows/unit_test.yml)
[![codecov](https://codecov.io/gh/opendilab/GoBigger/branch/main/graph/badge.svg?token=GwOV3jn0Le)](https://codecov.io/gh/opendilab/GoBigger)

![banner](assets/banner.png)

[GoBigger Doc](https://gobigger.readthedocs.io/en/latest/index.html) ([中文版](https://gobigger.readthedocs.io/zh_CN/latest/))

GoBigger is an efficient and straightforward *agar-like* game engine and provides various interfaces for game AI development. The game is similar to [Agar](https://agar.io/), a massive multiplayer online action game created by Brazilian developer Matheus Valadares. In GoBigger, players control one or more circular balls on a map. The goal is to gain as much size as possible by eating Food Balls and other balls smaller than the player's balls while avoiding larger ones that can eat the player's balls. Each player starts with one ball, and players can split a ball into two when it reaches a sufficient size, allowing them to control multiple balls.

We pay more attention to the following points:

* Complex multi-agent game design
* Complex observation spaces built on simple rules and simple actions
* More detailed configuration
* Custom opening with support for go-explore


## Outline

* [Overview](#overview)
* [Getting Start](#getting-start)
* [Resources](#resources)
* [Join and Contribute](#join-and-contribute)
* [License](#license)

## Overview

GoBigger allows users to to interact with the multi-agent environment within the basic rules easily. Users can simply get the observation in the game and apply their operations for their agents through the given interface. GoBigger is built with simple rules and actions, though it has complicated observation spaces.

<div align=center><img width = '640' height ='197' src ="https://github.com/opendilab/GoBigger/blob/main/assets/overview.gif"/></div>

### Basic Rules

To understand the rules in the game, GoBigger provides a few concepts as follows:

* `Match`: GoBigger will allow several agents (4 by default) to join in a match. There are many different units in a match, such as food balls, thorns balls, spore balls and player balls. When this match ends, each agent should gain more size by eating other balls to get a higher rank. 
* `Agent`: Each agent control a team, including several players (3 by default). Teamwork is essential for an agent to play against other agents.
* `Player`: Each player starts with one ball. To improve the operability of the game, GoBigger provides several operations for a player ball, including `split`, `eject` and `stop`.
* `Ball`: GoBigger provides 4 kinds of balls in a match.
    - `Food Ball`: Food balls are the neutral resources in the game. If a player ball eats a food ball, the food ball’s size will be parsed to the player ball.
    - `Thorn Ball`: If a player ball eats a thorns ball, the thorns ball’s size will be parsed to the player ball. But at the same time, the player ball will explode and split into several pieces (10 by default).
    - `Spore Ball`: Spore balls are ejected by the player balls. 
    - `Player Ball`: Player balls are the balls you can control in the game. You can change its moving direction. In addition, it can eat other balls smaller than itself by covering others’ centers. 

For more details, please refer to [what-is-gobigger](https://gobigger.readthedocs.io/en/latest/tutorial/what_is_gobigger.html).

### Observation Space

GoBigger also provides a wealth of observable information, and the observation space can be divided into two parts. Here is a brief description of the observation space. For more details, please refer to [observation-space](https://gobigger.readthedocs.io/en/latest/tutorial/space.html#observation-space).

#### Global State

The global state provides information related to the whole match, such as the map size, the total time and the last time of the match, and the leaderboard with team name and score.

#### Player State

The player state should be like:

```
{
    player_name: {
        'feature_layers': list(numpy.ndarray), # features of player
        'rectangle': [left_top_x, left_top_y, right_bottom_x, right_bottom_y], # the vision's position in the map
        'overlap': {
            'food': [{'position': position, 'radius': radius}, ...], # the length of food is not sure
            'thorns': [{'position': position, 'radius': radius}, ...], # the length of food is not sure
            'spore': [{'position': position, 'radius': radius}, ...], # the length of food is not sure
            'clone': [{'position': position, 'radius': radius, 'player': player_name, 'team': team_name}, ...], # the length of food is not sure
        }, # all balls' info in vision
        'team_name': team_name, # the team which this player belongs to 
    }
}
```

We define that `feature_layers` in `player_state` represent the feature of this player. `feature_layers` has several channels, and each channel gives the info of food balls, spore balls, thorns balls, or player balls in its vision. For example, in a match, we have 4 teams and 3 players for each team, then we get `feature_layers` as a list, and the length of this list should be 15, including 12 player channels, 1 food ball channel, 1 spore ball channel and 1 thorns ball channel.

Since getting `feature_layers` costs much time, GoBigger also provides player state without `feature_layers` when you add `use_spatial=False` in your render. More details [here](https://gobigger.readthedocs.io/en/latest/tutorial/space.html#observation-space-without-feature-layers).

### Action Space

In fact, a ball can only move, eject, split, and stop in a match; thus, the action space simply includes:

* Moving direction for the player balls.
* Split: Players can split a ball into two when it reaches a sufficient size.
* Eject: Player balls can eject spore in your moving direction.
* Stop: Stop player balls and gather together.

More details in [action-space](https://gobigger.readthedocs.io/en/latest/tutorial/space.html#action-space).

## Getting Start

### Setup

We test GoBigger within the following system:

* Centos 7.6
* Windows 10
* MacOS Catalina 10.15

And we recommend that your python version is 3.6. 

### Installation

You can simply install GoBigger from PyPI with the following command:

```bash
pip install gobigger
```

If you use Anaconda or Miniconda, you can install GoBigger through the following command:

```bash
conda install -c opendilab gobigger
```

You can also install the newest version through GitHub. First, get and download the official repository with the following command line.

```bash
git clone https://github.com/opendilab/GoBigger.git
```

Then you can install it from the source:

```bash
# install for use
# Note: use `--user` option to install the related packages in the user own directory(e.g.: ~/.local)
pip install . --user
     
# install for development(if you want to modify GoBigger)
pip install -e . --user
```

### Usage

After installation, you can launch your game environment easily according the following code:

```python
import random
from gobigger.server import Server
from gobigger.render import EnvRender

server = Server()
render = EnvRender(server.map_width, server.map_height)
server.set_render(render)
server.reset()
player_names = server.get_player_names_with_team()
# get [[team1_player1, team1_player2], [team2_player1, team2_player2], ...]
for i in range(10000):
    actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
               for team in player_names for player_name in team}
    if not server.step(actions):
        global_state, screen_data_players = server.obs()
        print('[{}] leaderboard={}'.format(i, global_state['leaderboard']))
    else:
        print('finish game!')
        break
server.close()
```

You will see output as follows. It shows the frame number and the leaderboard per frame.

```
[0] leaderboard={'0': 27, '1': 27, '2': 27, '3': 27}
[1] leaderboard={'0': 27, '1': 27, '2': 27, '3': 27}
[2] leaderboard={'0': 27, '1': 30.99935, '2': 30.99935, '3': 30.998700032499997}
[3] leaderboard={'0': 27, '1': 34.99610032498374, '2': 34.99675032498374, '3': 30.9961004874675}
[4] leaderboard={'0': 27, '1': 38.99025149484726, '2': 34.99155136485701, '3': 38.992201494805016}
[5] leaderboard={'0': 30.998700032499997, '1': 42.982054039382575, '2': 34.98635344444432, '3': 38.98620350437408}
[6] leaderboard={'0': 34.9961004874675, '1': 42.973458273284024, '2': 34.98115656353774, '3': 38.98020671345127}
[7] leaderboard={'0': 34.99270152230301, '1': 46.964264256209255, '2': 38.974660754429394, '3': 38.974211121796685}
[8] leaderboard={'0': 34.98930323688059, '1': 46.954872107798515, '2': 38.96686640687893, '3': 38.96821672917049}
[9] leaderboard={'0': 38.98525563106426, '1': 46.94548183767656, '2': 38.95907361808107, '3': 38.96222353533294}
...
```

We also build a simple env following `gym.Env`. For more details, you can refer to [gobigger_env.py](https://github.com/opendilab/GoBigger/blob/main/gobigger/envs/gobigger_env.py).


### Real-time Interaction with the Game

GoBigger allows users to play the game on their personal computers in real-time. Several modes are supported for users to explore this game.

#### Single Player

If you want to play real-time game on your PC on your own, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --player-num 1 --vision-type full
```

In this mode, the `up arrow` & `down arrow` & `left arrow` & `right arrow` allows your balls to move, `Q` means to eject spore in your moving direction, `W` means to split your balls, and `E` means to stop all your balls and gather them together.

<div align=center><img width = '400' height ='400' src ="https://github.com/opendilab/GoBigger/blob/main/assets/full_single.gif"/></div>

#### Double Players

If you want to play the real-time game on your PC with your friends, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --player-num 2 --vision-type full
```

In this mode, player1 uses the `up arrow` & `down arrow` & `left arrow` & `rigth arrow` to allow the balls to move, `[` means eject spore in your moving direction, `]` means split your balls, and `\` means stop all your balls and gather them together. Player2 uses `W` & `S` & `A` & `D` to allow the balls move, `1` means eject spore in your moving direction, `2` means split your balls, and `3` means stop all your balls and gather them together.

<div align=center><img width = '400' height ='400' src ="https://github.com/opendilab/GoBigger/blob/main/assets/full_double.gif"/></div>

#### Single Players with Partial Vision

If you want to play the real-time game on your PC with only partial vision, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --player-num 1 --vision-type partial
```

Your vision depends on all your balls’ positions and their size.

<div align=center><img width = '320' height ='320' src ="https://github.com/opendilab/GoBigger/blob/main/assets/partial.gif"/></div>

#### Single Players Against Bots

If you want to play against a bot, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --vs-bot
```

You can also add more bots to your game. Try to win the game with more bots!

```bash
python -m gobigger.bin.play --vs-bot --team-num 4
```

### High-level Operations in GoBigger

#### Eject towards the center
<div align=center><img width = '312' height ='278' src ="https://github.com/opendilab/GoBigger/blob/main/assets/merge_quickly.gif"/></div>

#### Surround others by splitting
<div align=center><img width = '310' height ='144' src ="https://github.com/opendilab/GoBigger/blob/main/assets/split_eat_all.gif"/></div>

#### Eat food balls quickly
<div align=center><img width = '312' height ='278' src ="https://github.com/opendilab/GoBigger/blob/main/assets/fast_eat.gif"/></div>

#### Concentrate size
<div align=center><img width = '312' height ='278' src ="https://github.com/opendilab/GoBigger/blob/main/assets/eject_merger.gif"/></div>

## Resources

For more details, please refer to [GoBigger Doc](https://gobigger.readthedocs.io/en/latest/index.html) ([中文版](https://gobigger.readthedocs.io/zh_CN/latest/)).


## Join and Contribute

Welcome to OpenDI Lab GoBigger community! Scan the QR code and add us on Wechat:

![QR code](assets/qr.png)

Or you can contact us with [slack](https://opendilab.slack.com/join/shared_invite/zt-v9tmv4fp-nUBAQEH1_Kuyu_q4plBssQ#/shared-invite/email) or email (opendilab.contact@gmail.com).

## License

GoBigger released under the Apache 2.0 license.
