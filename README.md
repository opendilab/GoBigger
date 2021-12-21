## CPP version of GoBigger

This is the GoBigger implemented by c++. We overwrite the game engine with c++ code to make it step much faster than
the python version. 

### Performance

The test is based on the following config:

```python
team_num=4,
player_num_per_team=3,
map_width=1000,
map_height=1000,
match_time=60*10,
state_tick_per_second=10, # frame
action_tick_per_second=5,
save_video=False,
obs_settings=dict(
    with_spatial=False,
    with_speed=False,
    with_all_vision=False,
)
```

In our testing machine(AMD EPYC 7742 64-Core Processor), we get the following testing results:

version | step(ms) | obs(ms) | total
---|---|---|---
python | 9.966 | 4.608 | 14.574
cpp | 0.573 | 0.985 | 1.558


### What is not supported compared to the python version

* Spatial info in obs
* Custom opening 
* Config in manager module

We are working on these issues and they will be solved in the next version.

### Installation

#### Prerequisites

* boost >= 1.6.7
* pybind11 >= 2.0.0 
* python ~= 3.6.8
* gcc ~= 7.3.0 or support c++11

#### Install

```shell
git clone https://github.com/opendilab/GoBigger.git
cd GoBigger
git checkout cpp
python -u setup.py install --user
```

### Test

After installation, you can try the following code to test.

```shell
python -u cgobigger/bin/demo_bot.py
```

It will print some log and finally save videos.



