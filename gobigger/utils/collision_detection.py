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
    def __init__(self, border: Border, precision : int = 50) -> None:
        '''
        Parameter:
            precision <int>: the precision of dividing rows
        '''
        super(PrecisionCollisionDetection, self).__init__(border = border)
        self.precision = precision

    def get_row(self, x) -> int:
        '''
        Overview:
            Get the row coordinates of the ball
        Parameter:
            node <BaseBall>: The ball need to get its row coordinates
        '''
        return int((x - self.border.minx) / self.border.height * self.precision)


    def solve(self, query_list: list, gallery_list: list):
        '''
        Overview:
            First, you need to sort the balls in each row according to the ordinate. 
            For the balls in query_list, first abstract the boundary of the ball into 
            a rectangle, then traverse each row in the rectangle, and find the first 
            ball covered by the query through dichotomy in each row, and then Enumerate 
            the balls in sequence until the ordinate exceeds the boundary of the query 
            rectangle.
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

        vec = {}
        for id, node in enumerate(gallery_list): 
            row_id = self.get_row(node.position.x)
            if  row_id not in vec:
                vec[row_id] = []
            vec[row_id].append((id, node.position.y))
        for val in vec.values():
            val.sort(key = lambda x: x[1])
        results = {}
        for id, query in enumerate(query_list):
            results[id] = []
            left = query.position.y - query.radius
            right = query.position.y + query.radius
            top = self.get_row(query.position.x - query.radius)
            bottom = self.get_row(query.position.x + query.radius)
            for i in range(top, bottom + 1):
                if i not in vec: continue
                l = len(vec[i])
                start_pos = 0
                for j in range(15, -1, -1):
                    if start_pos+(2**j) < l and vec[i][start_pos+(2**j)][1] < left:
                        start_pos += 2**j
                for j in range(start_pos, l):
                    if vec[i][j][1] > right: break
                    if query.judge_cover(gallery_list[vec[i][j][0]]):
                        results[id].append(gallery_list[vec[i][j][0]])
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

