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

def to_aliased_circle(position, radius, cut_num=16, decrease=3):
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

if __name__ == '__main__':

    print('......example 1......')
    src = 0
    arr = [1,2,3,4]
    prob = get_probability(src,arr)
    prob = norm(prob)
    prob = np.array(prob)
    print(prob)
    for i in range(100):
        a = np.random.choice(arr, 2, replace=False, p=prob.ravel())
        #print(a)

    print('......example 2......')
    src = 0
    arr = [0,0,0,0]
    prob = get_probability(src,arr)
    prob = norm(prob)
    prob = np.array(prob)
    print(prob)
    for i in range(100):
        a = np.random.choice(arr, 2, replace=False, p=prob.ravel())
        #print(a)



