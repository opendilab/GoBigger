# Go-Bigger: Multi-Agent Decision Intelligence Environment

GoBigger is a **multi-agent** environment not only for reinforce learning. It is similar to [Agar](https://agar.io/), which is a massively multiplayer online action game created by Brazilian developer Matheus Valadares. In GoBigger, players control one or more circular balls in a map. The goal is to gain as much size as possible by eating food balls and other balls smaller than the player's balls while avoiding larger ones which can eat the player's balls. Each player starts with one ball, but players can split a ball into two when it reaches a sufficient size, allowing them to control multiple balls.

GoBigger allows users to interact with the multi-agent environment easily. Through the given interface, users can get observations by actions created by their policy. Users can also customize their game environments by changing the args in the config.

<div align=center><img width = '640' height ='200' src ="https://github.com/opendilab/GoBigger/blob/main/assets/overview.gif"/></div>

## Getting Started

### Installation

#### Prerequisites

We test GoBigger within following system version:

* Centos 7.6
* Windows 10
* MacOS Catalina 10.15

And we recommend that your python version is 3.6. 

#### Get and install GoBigger

First get and download the official repository with the following command line.

```bash
git clone https://github.com/opendilab/GoBigger.git
```

You can install from source:

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

<div align=center><img width = '640' height ='640' src ="https://github.com/opendilab/GoBigger/blob/main/assets/full_single.jpg"/></div>


#### Double Players
If you want to play real-time game on your PC with your friends, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --player-num 2 --vision-type full
```

In this mode, player1 use `up arrow` & `down arrow` & `left arrow` & `rigth arrow` allows the balls move, `[` means eject spore on your moving direction, `]` means split your balls, and `\` means stop all your balls and gather them together. player2 use `W` & `S` & `A` & `D` allows the balls move, `1` means eject spore on your moving direction, `2` means split your balls, and `3` means stop all your balls and gather them together.

<div align=center><img width = '640' height ='640' src ="https://github.com/opendilab/GoBigger/blob/main/assets/full_double.jpg"/></div>

#### Single Players with partial vision
If you want to play real-time game on your PC with only partial vision, you can launch a game with the following code:

```bash
python -m gobigger.bin.play --player-num 1 --vision-type partial
```

Your vision depends on all your balls’ positions and their size.

<div align=center><img width = '320' height ='320' src ="https://github.com/opendilab/GoBigger/blob/main/assets/partial.jpg"/></div>

## Resources

For more details, please refer to [GoBigger Doc](https://opendilab.github.io/GoBigger/).

