import os
import matplotlib.pyplot as plt
import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import random
import numpy as np
import cv2
import time

from gobigger.utils import Border, create_collision_detection
from gobigger.balls import BaseBall

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestCollisionDection:

    def test_exhaustive(self):
        border = Border(0, 0, 1000, 1000)
        totol_num = 1000
        query_num = 200
        gallery_list = []
        for i in range(totol_num):
            x = random.randint(border.minx, border.maxx) + random.random()
            y = random.randint(border.miny, border.maxy) + random.random()
            gallery_list.append(BaseBall(i, position=Vector2(x, y), border=border))
        collision_detection = create_collision_detection("exhaustive", border=border)
        query_list = random.sample(gallery_list, query_num)
        collision_detection.solve(query_list, gallery_list)
        assert True

    def test_precision(self):
        border = Border(0, 0, 1000, 1000)
        totol_num = 1000
        query_num = 200
        gallery_list = []
        for i in range(totol_num):
            x = random.randint(border.minx, border.maxx) + random.random()
            y = random.randint(border.miny, border.maxy) + random.random()
            gallery_list.append(BaseBall(i, position=Vector2(x, y), border=border))
        collision_detection = create_collision_detection("precision", border=border)
        query_list = random.sample(gallery_list, query_num)
        collision_detection.solve(query_list, gallery_list)
        assert True
        
    def test_rebuild_quadtree(self):
        border = Border(0, 0, 1000, 1000)
        totol_num = 1000
        query_num = 200
        gallery_list = []
        for i in range(totol_num):
            x = random.randint(border.minx, border.maxx) + random.random()
            y = random.randint(border.miny, border.maxy) + random.random()
            gallery_list.append(BaseBall(i, position=Vector2(x, y), border=border))
        collision_detection = create_collision_detection("rebuild_quadtree", border=border)
        query_list = random.sample(gallery_list, query_num)
        collision_detection.solve(query_list, gallery_list)
        assert True

    def test_remove_quadtree(self):
        border = Border(0, 0, 1000, 1000)
        totol_num = 1000
        query_num = 200
        change_num = 100
        gallery_list = []
        for i in range(totol_num):
            x = random.randint(border.minx, border.maxx) + random.random()
            y = random.randint(border.miny, border.maxy) + random.random()
            gallery_list.append(BaseBall(i, position=Vector2(x, y), border=border))
        collision_detection = create_collision_detection("remove_quadtree", border=border)
        collision_detection.solve([], gallery_list)
        change_list = []
        for ball in gallery_list:
            p = random.random()
            if p < change_num / totol_num:
                x = random.randint(border.minx, border.maxx) + random.random()
                y = random.randint(border.miny, border.maxy) + random.random()
                ball.postion = Vector2(x, y)
                change_list.append(ball)
        query_list = random.sample(gallery_list, query_num)
        collision_detection.solve(query_list, change_list)
        assert True
        

class SpeedTest:

    def __init__(self, totol_num, border) -> None:
        self.border = border
        self.totol_num = totol_num
        self.gallery_list = []
        for i in range(totol_num):
            x = random.randint(border.minx, border.maxx) + random.random()
            y = random.randint(border.miny, border.maxy) + random.random()
            self.gallery_list.append(BaseBall(i, position = Vector2(x, y), border = border))
        self.exhaustive = create_collision_detection("exhaustive", border = border)
        self.precision = create_collision_detection("precision", border = border)
        self.rebuild_quadtree = create_collision_detection("rebuild_quadtree", border = border)
        self.remove_quadtree = create_collision_detection("remove_quadtree", border = border)

    def cal_speed(self, query_num: int, change_num: int, iters: int):
        exhustive_ava_time = 0
        precision_ava_time = 0
        rebuild_tree_ava_time = 0
        remove_tree_ava_time = 0
        self.remove_quadtree.solve([], self.gallery_list)
        for iter in range(iters):
            change_list = []
            for ball in self.gallery_list:
                p = random.random()
                if p < change_num / self.totol_num:
                    x = random.randint(self.border.minx, self.border.maxx) + random.random()
                    y = random.randint(self.border.miny, self.border.maxy) + random.random()
                    ball.postion = Vector2(x, y)
                    change_list.append(ball)
            query_list = random.sample(self.gallery_list, query_num)

            time1 = time.time()
            self.exhaustive.solve(query_list, self.gallery_list)
            time2 = time.time()
            self.precision.solve(query_list, self.gallery_list)
            time3 = time.time()
            self.rebuild_quadtree.solve(query_list, self.gallery_list)
            time4 = time.time()
            self.remove_quadtree.solve(query_list, change_list)
            time5 = time.time()
            
            exhustive_ava_time += time2 - time1
            precision_ava_time += time3 - time2
            rebuild_tree_ava_time += time4 - time3
            remove_tree_ava_time += time5 - time4
        
        exhustive_ava_time = int(round(exhustive_ava_time * 1000))
        precision_ava_time = int(round(precision_ava_time * 1000))
        rebuild_tree_ava_time = int(round(rebuild_tree_ava_time * 1000))
        remove_tree_ava_time = int(round(remove_tree_ava_time * 1000))

        return exhustive_ava_time/iters, precision_ava_time/iters, rebuild_tree_ava_time/iters, remove_tree_ava_time/iters

def get_speed_by_query_num(total_num=3000, start_num=0, end_num=1, stride=0.1, changed_p=0.2, iter=1):
    speed_test = SpeedTest(total_num , border=Border(0,0,1000,1000))
    exhaustive_time = []
    precision_time = []
    rebuild_time = []
    remove_time = []
    x_index = []
    for epoch in np.arange(start_num, end_num, stride):
        logging.debug("epoch " + str(epoch) + " begin")
        x_index.append(epoch)
        result = speed_test.cal_speed(int(total_num * epoch), int(total_num * changed_p), int(iter))
        exhaustive_time.append(result[0])
        precision_time.append(result[1])
        rebuild_time.append(result[2])
        remove_time.append(result[3])
    return x_index, exhaustive_time, precision_time, rebuild_time, remove_time

def get_speed_by_change_num(total_num=3000, start_num=0, end_num=1, stride=0.1, query_p=0.2, iter=1):
    speed_test = SpeedTest(total_num , border=Border(0,0,1000,1000))
    exhaustive_time = []
    precision_time = []
    rebuild_time = []
    remove_time = []
    x_index = []
    for epoch in np.arange(start_num, end_num, stride):
        logging.debug("epoch " + str(epoch) + " begin")
        x_index.append(epoch)
        result = speed_test.cal_speed(int(total_num * query_p), int(total_num * epoch), int(iter))
        exhaustive_time.append(result[0])
        precision_time.append(result[1])
        rebuild_time.append(result[2])
        remove_time.append(result[3])
    return x_index, exhaustive_time, precision_time, rebuild_time, remove_time

def get_speed_by_iter(total_num=3000, start_num=1, end_num=51, stride=5, query_p=0.2, changed_p=0.2):
    speed_test = SpeedTest(total_num , border=Border(0,0,1000,1000))
    exhaustive_time = []
    precision_time = []
    rebuild_time = []
    remove_time = []
    x_index = []
    for epoch in np.arange(start_num, end_num, stride):
        logging.debug("epoch " + str(epoch) + " begin")
        x_index.append(epoch)
        result = speed_test.cal_speed(int(total_num * query_p), int(total_num * changed_p), int(epoch))
        exhaustive_time.append(result[0])
        precision_time.append(result[1])
        rebuild_time.append(result[2])
        remove_time.append(result[3])
    return x_index, exhaustive_time, precision_time, rebuild_time, remove_time

def log_draw_for_data(name, time_data):
    x_index = time_data[0]
    exhaustive = time_data[1]
    precision = time_data[2]
    rebuild = time_data[3]
    remove = time_data[4]
    logging.debug(name + ":")
    logging.debug('exhaustive: ' + " ".join(map(str, exhaustive)))
    logging.debug('precision: ' + " ".join(map(str, precision)))
    logging.debug('rebuild_quadTree: ' + " ".join(map(str, rebuild)))
    logging.debug('remove_quadTree: ' + " ".join(map(str, remove)))
    plt.cla()
    plt.xlabel(name)
    plt.ylabel('time')
    plt.title('time - ' + name +' diagram')
    plt.plot(x_index, exhaustive, 'r--', label = 'exhaustive')
    plt.plot(x_index, precision, 'g--', label = 'precision')
    plt.plot(x_index, rebuild, 'b--', label = "rebuild_quadTree")
    plt.plot(x_index, remove, 'y--', label = "remove_quadTree")
    plt.legend()
    plt.savefig(name +'.png')

if __name__ == '__main__':
    # log_draw_for_data('changed_num_3000', get_speed_by_change_num(total_num=3000))
    # log_draw_for_data('changed_num_10000', get_speed_by_change_num(total_num=10000))
    # log_draw_for_data('changed_num_30000', get_speed_by_change_num(total_num=30000))
    # log_draw_for_data('query_num_3000', get_speed_by_query_num(total_num=3000))
    # log_draw_for_data('query_num_10000', get_speed_by_query_num(total_num=10000))
    log_draw_for_data('iters_num_3000', get_speed_by_iter(total_num=3000))
    # log_draw_for_data('iters_num_10000', get_speed_by_iter(total_num=10000))
