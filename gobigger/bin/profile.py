import time
from pygame.math import Vector2
import numpy as np
import numexpr as ne
import random

from pygame.math import Vector2

from gobigger.agents import BotAgent
from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender


def method1(food_balls, cx, cy, r):
    food_count = 0
    food = len(food_balls) * [3 * [None]]
    food_radius = 2
    for ball in food_balls:
        x = ball.x
        y = ball.y
        if (x-cx)**2 + (y-cy)**2 < r**2:
            food[food_count] = [x, y, food_radius]
            food_count += 1
    return food[:food_count]


def method2(food_balls, cx, cy, r):
    t1 = time.time()
    X = np.array([ball.x for ball in food_balls])
    Y = np.array([ball.y for ball in food_balls])
    t2 = time.time()
    res = ne.evaluate('((X-cx)**2 + (Y-cy)**2)<r**2')
    res_x = X[res==True]
    res_y = Y[res==True]
    t3 = time.time()
    return res_x, res_y, t2-t1, t3-t2


def profile():
    ball_num = 2000
    border = 1000
    cx = 500
    cy = 500
    r = 100
    balls = []
    for _ in range(ball_num):
        balls.append(Vector2(random.random() * border, random.random() * border))
    t1 = time.time()
    for i in range(1000):
        res1 = method1(balls, cx, cy, r)
    t2 = time.time()
    tt1_all = 0
    tt2_all = 0
    count = 10000
    for i in range(count):
        res_x, res_y, tt1, tt2 = method2(balls, cx, cy, r)
        tt1_all += tt1
        tt2_all += tt2
    print(tt1_all/count, tt2_all/count)
    t3 = time.time()
    print((t2-t1)/count, (t3-t2)/count)
    import pdb; pdb.set_trace()
    print('end')


if __name__ == '__main__':
    profile()
