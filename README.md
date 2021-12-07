# Go-Bigger: Multi-Agent Decision Intelligence Environment

[![PyPI](https://img.shields.io/pypi/v/gobigger)](https://pypi.org/project/gobigger/)
[![Anaconda-Server Badge](https://anaconda.org/opendilab/gobigger/badges/version.svg)](https://anaconda.org/opendilab/gobigger)
[![Read the Docs](https://img.shields.io/readthedocs/gobigger)](https://gobigger.readthedocs.io/en/latest/?badge=latest)
[![Read the Docs](https://img.shields.io/readthedocs/gobigger?label=%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3)](https://gobigger.readthedocs.io/zh_CN/latest/?badge=latest)
[![unit_test](https://github.com/opendilab/GoBigger/actions/workflows/unit_test.yml/badge.svg?branch=main)](https://github.com/opendilab/GoBigger/actions/workflows/unit_test.yml)
[![codecov](https://codecov.io/gh/opendilab/GoBigger/branch/main/graph/badge.svg?token=GwOV3jn0Le)](https://codecov.io/gh/opendilab/GoBigger)

[GoBigger Doc](https://gobigger.readthedocs.io/en/latest/index.html) ([中文版](https://gobigger.readthedocs.io/zh_CN/latest/))

## Ongoing

* 2021.11.13 We are holding a [competition](https://github.com/opendilab/GoBigger-Challenge-2021) —— Go-Bigger: Multi-Agent Decision Intelligence Environment. Come and make your agents in the game!

GoBigger is a simple and efficient *agar-like* game engine and provides various interfaces for game AI development. The game is similar to [Agar](https://agar.io/), which is a massively multiplayer online action game created by Brazilian developer Matheus Valadares. In GoBigger, players control one or more circular balls in a map. The goal is to gain as much size as possible by eating food balls and other balls smaller than the player's balls while avoiding larger ones which can eat the player's balls. Each player starts with one ball, but players can split a ball into two when it reaches a sufficient size, allowing them to control multiple balls.

<div align=center><img width = '640' height ='197' src ="https://github.com/opendilab/GoBigger/blob/main/assets/overview.gif"/></div>

## Introduction

GoBigger allows users to interact with the multi-agent environment easily within the basic rules. Through the given interface, users can simply get the observation in game and apply their operations for their agents.

### Basic Rules

In order to understand the rules in the game, GoBigger provides a few concepts as following:

* `Match`: GoBigger will allow serveral agents (4 by default) to join in a match. There are many different units in a match, such as food balls, thorns balls, spore balls and player balls. Each agent should gain more size by eating other balls to get a higher rank when this match ends.
* `Agent`: Each agent control a team including serveral players (3 by default). Teamwork is important for a agent to play against other agents.
* `Player`: Each player starts with one ball. In order to improve the operability of the game, GoBigger provides serveral operation for a player ball, including `split`, `eject` and `stop`.
* `Ball`: GoBigger provides 4 kinds of balls in a match.
    - `Food Ball`: Food balls are the neutral resources in the game. If a player ball eat a food ball, the food ball’s size will be parsed to the player ball.
    - `Thorn Ball`: If a player ball eat a thorns ball, the thorns ball’s size will be parsed to the player ball. But at the same time, the player ball will explode and will be splited into several pieces (10 by default).
    - `Spore Ball`: Spore balls are ejected by the player balls. 
    - `Player Ball`: Player balls are the balls you can control in the game. You can change its moving direction. In addition, it can eat other balls smaller than itself by covering others’ center. 

For more details, please refer to [what-is-gobigger](https://gobigger.readthedocs.io/en/latest/tutorial/what_is_gobigger.html).

### Observation Space

GoBigger also provide a wealth of observable information, and the observation space can be devided into two part. Here is the brief description of the observation space. For more details, please refer to [observation-space](https://gobigger.readthedocs.io/en/latest/tutorial/space.html#observation-space).

#### Global State

Global state provides information related to the whole match, such as the map size, the total time and the last time of the match, and the leaderboard within team name and score.

#### Player State

Player state should be like:

```
{
    player_name: {
        'feature_layers': list(numpy.ndarray), # features of player
        'rectangle': [left_top_x, left_top_y, right_bottom_x, right_bottom_y], # the vision's position in the map
        'overlap': {
            'food': [[position.x, position.y, radius], ...], 
            'thorns': [[position.x, position.y, radius], ...],
            'spore': [[position.x, position.y, radius], ...],
            'clone': [[[position.x, position.y, radius, player_name, team_name], ...],     
        }, # all balls' info in vision
        'team_name': team_name, # the team which this player belongs to 
    }
}
```

We define that `feature_layers` in `player_state` represents the feature of this player. `feature_layers` has several channels, and each channel gives the info of food balls, or spore balls, or thorns balls, or player balls in its vision. For example, in a match we have 4 teams and 3 players for each team, then we get `feature_layers` as a list, and the length of this list should be 15, including 12 player channel, 1 food ball channel , 1 spore ball channel and 1 thorns ball channel.

Since getting `feature_layers` costs much time, GoBigger also provides player state without `feature_layers` when you add `use_spatial=False` in your render. More details [here](https://gobigger.readthedocs.io/en/latest/tutorial/space.html#observation-space-without-feature-layers).

### Action Space

In fact, a ball can only move, eject, split, and stop in a match, thus the action space simply includes:

* Moving direction for the player balls.
* Split: Players can split a ball into two when it reaches a sufficient size.
* Eject: Player balls can eject spore on your moving direction.
* Stop: Stop player balls and gather together together.

More details in [action-space](https://gobigger.readthedocs.io/en/latest/tutorial/space.html#action-space).

## Getting Started

### Installation

#### Prerequisites

We test GoBigger within the following system:

* Centos 7.6
* Windows 10
* MacOS Catalina 10.15

And we recommend that your python version is 3.6. 

#### Get and install GoBigger

You can simply install GoBigger from PyPI with the following command:

```bash
pip install gobigger
```

If you use Anaconda or Miniconda, you can install GoBigger through the following command:

```bash
conda install -c opendilab gobigger
```

You can also install with newest version through GitHub. First get and download the official repository with the following command line.

```bash
git clone https://github.com/opendilab/GoBigger.git
```

Then you can install from source:

```bash
# install for use
# Note: use `--user` option to install the related packages in the user own directory(e.g.: ~/.local)
pip install . --user
     
# install for development(if you want to modify GoBigger)
pip install -e . --user
```

### Launch a game environment

After installation, you can launch your game environment easily according the following code:

```python
import random
from gobigger.server import Server
from gobigger.render import EnvRender

server = Server()
render = EnvRender(server.map_width, server.map_height)
server.set_render(render)
server.start()
player_names = server.get_player_names_with_team()
# get [[team1_player1, team1_player2], [team2_player1, team2_player2], ...]
for i in range(10000):
    actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
               for team in player_names for player_name in team}
    if not server.step(actions):
        global_state, screen_data_players = server.obs()
    else:
        print('finish game!')
        break
server.close()
```

We also build a simple env following gym.Env. For more details, you can refer to [gobigger_env.py](https://github.com/opendilab/GoBigger/blob/main/gobigger/envs/gobigger_env.py).

### Real-time Interaction with game

GoBigger allow users to play game on their personal computer in real-time. Serveral modes are supported for users to explore this game.

#### Single Player

If you want to play real-time game on your PC on your own, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --player-num 1 --vision-type full
```

In this mode, `up arrow` & `down arrow` & `left arrow` & `rigth arrow` allows your balls move, `Q` means eject spore on your moving direction, `W` means split your balls, and `E` means stop all your balls and gather them together.

<div align=center><img width = '400' height ='400' src ="https://github.com/opendilab/GoBigger/blob/main/assets/full_single.gif"/></div>

#### Double Players

If you want to play real-time game on your PC with your friends, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --player-num 2 --vision-type full
```

In this mode, player1 use `up arrow` & `down arrow` & `left arrow` & `rigth arrow` allows the balls move, `[` means eject spore on your moving direction, `]` means split your balls, and `\` means stop all your balls and gather them together. player2 use `W` & `S` & `A` & `D` allows the balls move, `1` means eject spore on your moving direction, `2` means split your balls, and `3` means stop all your balls and gather them together.

<div align=center><img width = '400' height ='400' src ="https://github.com/opendilab/GoBigger/blob/main/assets/full_double.gif"/></div>

#### Single Players with partial vision

If you want to play real-time game on your PC with only partial vision, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --player-num 1 --vision-type partial
```

Your vision depends on all your balls’ positions and their size.

<div align=center><img width = '320' height ='320' src ="https://github.com/opendilab/GoBigger/blob/main/assets/partial.gif"/></div>

#### Single Players against bots

If you want to play against a bot, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --vs-bot
```

You can also add more bots in your game. Try to win the game with more bots!

```bash
python -m gobigger.bin.play --vs-bot --team-num 4
```

#### bots test with Visualization

If you want to test agent without human player, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --bot-only --player-num 3 --team-num 1
```

You can also test your custom agent with `--agent-class` argument:

```bash
python -m gobigger.bin.play --bot-only --player-num 3 --team-num 4 --agent-class submit.bot_submission.BotSubmission
```

Beware your agent class should implement `__init__(self, team_name, player_names)` `get_actions(self, obs) -> action` method.

## High-level Operations in GoBigger

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

## License

GoBigger released under the Apache 2.0 license.


