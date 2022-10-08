import os
import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import random
import numpy as np
import cv2

from gobigger.balls import BaseBall
from gobigger.utils import format_vector, add_score, save_screen_data_to_img, Border, QuadNode

logging.basicConfig(level=logging.DEBUG)


def test_format_vector():
    v = Vector2(6, 8)
    norm_max = 5
    v_format = format_vector(v, norm_max=norm_max)
    assert v_format.x == 3
    assert v_format.y == 4


def test_add_score():
    score_old = 10
    score_add = 20
    score_new = add_score(score_old, score_add)
    assert score_new == 30


def test_save_screen_data_to_img():
    screen_data = (np.random.rand(100, 100, 3) * 255).astype(np.uint8)
    img_path = './temp.jpg'
    save_screen_data_to_img(screen_data, img_path=None)
    assert True


@pytest.mark.unittest
class TestBorder:

    def test_init(self):
        border = Border(0, 0, 1000, 1000)
        assert border.minx == 0
        assert border.miny == 0
        assert border.maxx == 1000
        assert border.maxy == 1000
        assert border.width == 1000
        assert border.height == 1000

    def test_contains(self):
        border = Border(0, 0, 1000, 1000)
        assert border.contains(position=Vector2(300, 300))
        assert not border.contains(position=Vector2(1300, 300))

    def test_sample(self):
        border = Border(0, 0, 1000, 1000)
        s = border.sample()
        assert border.contains(s)

    def test_get_joint(self):
        border = Border(0, 0, 1000, 1000)
        border_new = border.get_joint(border=Border(300, 300, 600, 600))
        assert border_new.minx == 300
        assert border_new.maxx == 300
        assert border_new.miny == 600
        assert border_new.maxy == 600


@pytest.mark.unittest
class TestQuadNode:

    def test_init(self):
        border = Border(0, 0, 1000, 1000)
        quad_node = QuadNode(border)
        assert quad_node.max_depth == 32

    def test_get_quad(self):
        border = Border(0, 0, 1000, 1000)
        quad_node = QuadNode(border)
        node = BaseBall('0', position=border.sample(), border=border, score=1)
        assert isinstance(quad_node.get_quad(node=node), int)

    def test_insert(self):
        border = Border(0, 0, 1000, 1000)
        quad_node = QuadNode(border)
        node = BaseBall('0', position=border.sample(), border=border, score=1)
        quad_node.insert(node=node)

    def test_find(self):
        border = Border(0, 0, 1000, 1000)
        quad_node = QuadNode(border)
        node = BaseBall('0', position=border.sample(), border=border, score=1)
        quad_node.find(border)

    def test_clear(self):
        border = Border(0, 0, 1000, 1000)
        quad_node = QuadNode(border)
        node = BaseBall('0', position=border.sample(), border=border, score=1)
        quad_node.clear()

    def test_remove(self):
        border = Border(0, 0, 1000, 1000)
        quad_node = QuadNode(border)
        node = BaseBall('0', position=border.sample(), border=border, score=1)
        quad_node.remove(node=node)
