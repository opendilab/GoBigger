import numpy as np
import logging

from .structures import Border, QuadNode


class BaseCollisionDetection:

    def __init__(self, border: Border) -> None:
        self.border = border

    def solve(self, query_list: list, gallery_list: list):
        raise NotImplementedError


class ExhaustiveCollisionDetection(BaseCollisionDetection):
    '''
    Overview:
        Exhaustive Algorithm
    '''
    def __init__(self, border: Border) -> None:
        super(ExhaustiveCollisionDetection, self).__init__(border=border)

    def solve(self, query_list: list, gallery_list: list):
        '''
        Overview:
            For the balls in the query, enumerate each ball in the gallery to determine whether there is a collision
        Parameters:
            query_list <List[BaseBall]>: List of balls that need to be queried for collision
            gallery_list <List[BaseBall]>: List of all balls
        Returns:
            results <Dict[int: List[BaseBall]> return value
                int value denotes:
                    the subscript in query_list
                string value denotes:
                    List of balls that collided with the query corresponding to the subscript
        '''
        results = {}
        for i, q in enumerate(query_list):
            results[i] = []
            for j, g in enumerate(gallery_list):
                if q.judge_cover(g): 
                    results[i].append(g)
        return results


class PrecisionCollisionDetection(BaseCollisionDetection) :
    '''
    Overview:
        Precision Approximation Algorithm
        Divide the map into several rows according to the accuracy that has been set, dynamically maintain the row information in each frame, and search by row
    '''
    def __init__(self, border: Border, precision : int = 1000) -> None:
        '''
        Parameter:
            precision <int>: the precision of dividing rows
        '''
        super(PrecisionCollisionDetection, self).__init__(border = border)
        self.precision = precision
        self.row_vector = [[] for j in range(self.precision)]

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

    def solve(self, query_list: list, gallery_list: list):
        '''
        Overview:
            First, you need to sort the balls in each row according to the ordinate. For the balls in query_list, first abstract the boundary of the ball into a rectangle, then traverse each row in the rectangle, and find the first ball covered by the query through dichotomy in each row, and then Enumerate the balls in sequence until the ordinate exceeds the boundary of the query rectangle
        Parameters:
            query_list <List[BaseBall]>: List of balls that need to be queried for collision
            gallery_list <List[BaseBall]>: List of all balls
        Returns:
            results <Dict[int: List[BaseBall]> return value
                int value denotes:
                    the subscript in query_list
                string value denotes:
                    List of balls that collided with the query corresponding to the subscript
        '''

        for i in range(self.precision): 
            self.row_vector[i].clear()
        for node in gallery_list: 
            self.row_vector[self.get_row(node.position.x)].append(node)
        for i in range(self.precision):
            self.row_vector[i].sort(key = lambda base_ball: base_ball.position.y)
        results = {}
        for id, query in enumerate(query_list):
            results[id] = []
            left = query.position.y - query.radius
            right = query.position.y + query.radius
            top = self.get_row(query.position.x - query.radius)
            bottom = self.get_row(query.position.x + query.radius)
            for i in range(top, bottom + 1):
                start_pos = self.dichotomous_jump(left, i)
                if start_pos >= 0:
                    for j in range(start_pos, len(self.row_vector[i])):
                        if self.row_vector[i][j].position.y > right: break
                        is_covered = query.judge_cover(self.row_vector[i][j])
                        if is_covered: 
                            results[id].append(self.row_vector[i][j])
        return results


class RebuildQuadTreeCollisionDetection(BaseCollisionDetection) :
    '''
        Overview:
            Build a quadtree on a two-dimensional plane in every frame, and query collisions in the quadtree

    '''
    def __init__(self, border: Border, node_capacity = 64, tree_depth = 32) -> None:
        '''
        Parameter:
            node_capacity <int>: The capacity of each point in the quadtree
            tree_depth <int>: The max depth of the quadtree
        '''
        super(RebuildQuadTreeCollisionDetection, self).__init__(border = border)
        self.node_capacity = node_capacity
        self.tree_depth = tree_depth
        self.border = border
    
    def solve(self, query_list: list, gallery_list: list):
        '''
        Overview:
           Construct a quadtree from scratch based on gallery_list and complete the query
        Parameters:
            query_list <List[BaseBall]>: List of balls that need to be queried for collision
            gallery_list <List[BaseBall]>: List of all balls
        Returns:
            results <Dict[int: List[BaseBall]> return value
                int value denotes:
                    the subscript in query_list
                string value denotes:
                    List of balls that collided with the query corresponding to the subscript
        '''
        quadTree = QuadNode(border=self.border, max_depth = self.tree_depth, max_num = self.node_capacity)
        for node in gallery_list:
            quadTree.insert(node)
        results = {}
        for i, query in enumerate(query_list):
            results[i] = []
            quadTree_results = quadTree.find(Border(max(query.position.x - query.radius, self.border.minx), 
                                                    max(query.position.y - query.radius, self.border.miny), 
                                                    min(query.position.x + query.radius, self.border.maxx),
                                                    min(query.position.y + query.radius, self.border.maxy)))
            for result in quadTree_results:
                if query.judge_cover(result):
                    results[i].append(result)
        return results


class RemoveQuadTreeCollisionDetection(BaseCollisionDetection) :
    '''
        Overview:
            Add delete operations for the quadtree, and dynamically maintain a quadtree

    '''
    def __init__(self, border: Border, node_capacity = 64, tree_depth = 32) -> None:
        '''
        Parameter:
            node_capacity <int>: The capacity of each point in the quadtree
            tree_depth <int>: The max depth of the quadtree
        '''
        super(RemoveQuadTreeCollisionDetection, self).__init__(border = border)
        self.node_capacity = node_capacity
        self.tree_depth = tree_depth
        self.border = border
        self.quadTree = QuadNode(border = border, max_depth = tree_depth, max_num = node_capacity, parent=None)
    
    def solve(self, query_list: list, changed_node_list: list):
        '''
        Overview:
           Update the points in the quadtree according to the changed_node_list and complete the query
        Parameters:
            query_list <List[BaseBall]>: List of balls that need to be queried for collision
            gallery_list <List[BaseBall]>: List of all balls
        Returns:
            results <Dict[int: List[BaseBall]> return value
                int value denotes:
                    the subscript in query_list
                string value denotes:
                    List of balls that collided with the query corresponding to the subscript
        '''
        for node in changed_node_list:
            if not node.quad_node == None : node.quad_node.remove(node)
            if not node.is_remove: self.quadTree.insert(node)
        results = {}
        for i, query in enumerate(query_list):
            results[i] = []
            quadTree_results = self.quadTree.find(Border(max(query.position.x - query.radius, self.border.minx), 
                                                    max(query.position.y - query.radius, self.border.miny), 
                                                    min(query.position.x + query.radius, self.border.maxx),
                                                    min(query.position.y + query.radius, self.border.maxy)))
            for result in quadTree_results:
                if query.judge_cover(result):
                    results[i].append(result)
        return results

def create_collision_detection(cd_type, **cd_kwargs):
    if cd_type == 'exhaustive':
        return ExhaustiveCollisionDetection(**cd_kwargs)
    if cd_type == 'precision':
        return PrecisionCollisionDetection(**cd_kwargs)
    if cd_type == 'rebuild_quadtree':
        return RebuildQuadTreeCollisionDetection(**cd_kwargs)
    if cd_type == 'remove_quadtree':
        return RemoveQuadTreeCollisionDetection(**cd_kwargs)
    else:
        raise NotImplementedError

