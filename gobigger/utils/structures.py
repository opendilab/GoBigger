import math
from pygame.math import Vector2
import logging
import random
import cv2
import numpy as np


def format_vector(v, norm_max):
    '''
    Overview:
        The maximum value of the given vector's modulus
         example:
             1) The maximum speed limit is 5, given that the current speed is (6,8), it will return (3,4)
             2) Limit the maximum acceleration and return to the acceleration after the limit
    '''
    if v.length() == 0:
        return v
    elif v.length() < norm_max:
        # logging.debug('v={}, v.length()={}, norm_max={}'.format(v, v.length(), norm_max))
        return v
    else:
        return v.normalize() * norm_max


def add_size(size_old, size_add):
    '''
    Overview:
        Calculate the size of the big ball after eating the small ball
    '''
    return size_old + size_add


def save_screen_data_to_img(screen_data, img_path=None):
    '''
    Overview:
        Save the numpy screen data as the corresponding picture
    '''
    img = cv2.cvtColor(screen_data, cv2.COLOR_RGB2BGR)
    img = np.fliplr(img)
    img = np.rot90(img)
    if img_path is not None:
        cv2.imwrite(img_path, img)


class Border:
    '''
    Overview:
        used to specify a rectangular range
    '''
    def __init__(self, minx, miny, maxx, maxy, random_generator=None):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.width = self.maxx - self.minx
        self.height =self.maxy - self.miny
        if random_generator is not None:
            self._random = random_generator
        else:
            self._random = random.Random()

    def __repr__(self) -> str:
        return '[' + str(self.minx) + ',' + str(self.miny) + ',' + str(self.maxx) + ',' + str(self.maxy) + ']'

    def contains(self, position: Vector2) -> bool:
        '''
        Overview:
            To judge whether a position in this border.
        Parameters:
            position <Vector2>: the position to be judged.
        Returns:
            bool: True or False, whether the position in this border.
        '''
        return position.x > self.minx and position.x < self.maxx and position.y > self.miny and position.y < self.maxy

    def sample(self) -> Vector2:
        '''
        Overview:
            Randomly sample a position in the border.
        Returns:
            Vector2: the sampled position.
        '''
        x = self._random.uniform(self.minx, self.maxx)
        y = self._random.uniform(self.miny, self.maxy)
        return Vector2(x, y)

    def get_joint(self, border) :
        new_minx = max(self.minx, border.minx)
        new_maxx = min(self.maxx, border.maxx)
        new_miny = max(self.miny, border.miny)
        new_maxy = min(self.maxy, border.maxy)
        if new_minx > new_maxx or new_miny > new_maxy:
            return None
        return Border(new_minx, new_maxx, new_miny, new_maxy, self._random)


class QuadNode:
    def __init__(self, border, max_depth = 32, max_num = 64, parent = None) -> None:
        self.border = border
        self.max_depth = max_depth
        self.midx = (border.minx + border.maxx) / 2
        self.midy = (border.miny + border.maxy) / 2
        self.max_num = max_num
        self.children = None
        self.parent = parent
        self.items = []

    def get_quad(self, node):
        if node.position.x < self.midx:
            if node.position.y < self.midy : return 0
            else: return 1
        else: 
            if node.position.y < self.midy: return 2
            else: return 3

    def insert(self, node):
        if not self.children == None:
            self.children[self.get_quad(node)].insert(node)
        else:
            self.items.append(node)
            node.quad_node = self
            if len(self.items) > self.max_num and self.max_depth >= 1:
                b0 = Border(self.border.minx, self.border.miny, self.midx, self.midy)
                b1 = Border(self.border.minx, self.midy, self.midx, self.border.maxy)
                b2 = Border(self.midx, self.border.miny, self.border.maxx, self.midy)
                b3 = Border(self.midx, self.midy, self.border.maxx,  self.border.maxy)
                self.children = []
                self.children.append(QuadNode(b0, max_depth = self.max_depth - 1, max_num = self.max_num, parent=self))
                self.children.append(QuadNode(b1, max_depth = self.max_depth - 1, max_num = self.max_num, parent=self))
                self.children.append(QuadNode(b2, max_depth = self.max_depth - 1, max_num = self.max_num, parent=self))
                self.children.append(QuadNode(b3, max_depth = self.max_depth - 1, max_num = self.max_num, parent=self))
                for item in self.items:
                    self.children[self.get_quad(item)].insert(item)
                self.items.clear()
    
    def find(self, border):
        ans = self.items
        if not self.children == None:
            for child in self.children:
                tmpBorder = border.get_joint(child.border)
                if not tmpBorder == None:
                    ans = ans + child.find(tmpBorder)
        return ans

    def clear(self):
        if self.children == None: return
        max_num = self.max_num
        for child in self.children:
            if not child.children == None: return
            max_num = max_num - len(child.items)
        if max_num >= 0:
            for child in self.children:
                for item in child.items:
                    item.quad_node = self
                    self.items.append(item)
            self.children = None
            if not self.parent == None:
                self.parent.clear()
            
    def remove(self, node):
        for i, item in enumerate(self.items):
            if item.ball_id == node.ball_id:
                del self.items[i]
                break
        node.quad_node = None
        if not self.parent == None:
            self.parent.clear()
