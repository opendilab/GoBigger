import math
import random
import numpy as np


def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]

def get_probability(src,arr):
    diff = [abs(i-src)+0.001 for i in arr]
    return [1/i if 1/i<1 else 1 for i in diff]

def norm(arr):
    return [i/sum(arr) for i in arr]

def to_aliased_circle(position, radius, cut_num=8, decrease=1):
    point_list = []
    radius_decrease = radius - decrease
    assert radius_decrease > 0
    piece_angle = math.pi / (cut_num)
    for i in range(cut_num*2):
        angle = piece_angle * i
        if i % 2 == 0:
            point_list.append([position.x + radius * math.cos(angle), position.y + radius * math.sin(angle)])
        else:
            point_list.append([position.x + radius_decrease * math.cos(angle), position.y + radius_decrease * math.sin(angle)])
    return point_list

def to_arrow(position, radius, direction, out=1.2):
    x0, y0 = position.x, position.y
    x, y = direction.x, direction.y
    point_list = [
        [x0 + out * radius * x, y0 + out * radius * y],
        [x0 - math.sqrt(2)/2 * radius * (y - x), y0 + math.sqrt(2)/2 * radius * (x + y)],
        [x0 + math.sqrt(2)/2 * radius * (x + y), y0 + math.sqrt(2)/2 * radius * (y - x)],
    ]
    return point_list
