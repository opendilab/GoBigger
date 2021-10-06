import numpy as np
import logging

from .structures import Border

class precision_algorithm:
    '''
    Overview:
        Precision Approximation Algorithm
        Divide the map into several rows according to the accuracy that has been set, dynamically maintain the row information in each frame, and search by row
    '''
    def __init__(self, border: Border, balls , precision : int = 1000) -> None:
        '''
        Parameter:
            border <Border>: the border of ball's coordinate
            balls <list>: list of balls which need to be searched
            precision <int>: the precision of dividing rows
        '''
        self.border = border
        self.precision = precision
        self.row_vector = [[] for j in range(self.precision)]
        for node in balls: 
            self.row_vector[self.get_row(node.position.x)].append(node)
        for i in range(self.precision):
            self.row_vector[i].sort(key = lambda base_ball: base_ball.position.y)

    def get_row(self, x) -> int:
        '''
        Overview:
            Get the row coordinates of the ball
        Parameter:
            node <BaseBall>: The ball need to get its row coordinates
        '''
        x = max(0, x - self.border.minx)
        x = min(x, self.border.maxx - self.border.minx)
        row_height = self.border.height / self.precision
        row_id = int (x // row_height)
        row_id = max(0, row_id)
        row_id = min(row_id, self.precision - 1)
        return row_id


    def dichotomous_jump(self, value, row_id) -> int:
        '''
        Overview:
            Dichotomous algorithm
        Parameter:
            value <double> : Threshold
            row_id <int> : The id of the row being operated on
        '''
        pos = -1
        l = 0
        r = len(self.row_vector[row_id]) - 1
        while l <= r:
            mid = int((l + r) // 2)
            if value <= self.row_vector[row_id][mid].position.y:
                r = mid - 1
                pos = mid
            else:
                l = mid + 1
        return pos

    def solve(self, left, top, right, bottom):
        '''
        Overview:
            First, you need to sort the balls in each row according to the ordinate. For the balls in query_list, first abstract the boundary of the ball into a rectangle, then traverse each row in the rectangle, and find the first ball covered by the query through dichotomy in each row, and then Enumerate the balls in sequence until the ordinate exceeds the boundary of the query rectangle
        Parameters:
            top <int>: Top border of the query area
            bottom <int>: bottom border of the query area
            left <int>: Left border of the query area
            right <int>: Right border of the query area
        Returns:
            results <generator [BaseBall]> return possible balls (Need further inspection)
        '''

        for i in range(top, bottom + 1):
            start_pos = self.dichotomous_jump(left, i)
            if start_pos >= 0:
                for j in range(start_pos, len(self.row_vector[i])):
                    if self.row_vector[i][j].position.y > right: break
                    yield(self.row_vector[i][j])