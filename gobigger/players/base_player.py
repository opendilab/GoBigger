from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall


class BasePlayer:
    '''
    Player's abstract class
    '''
    def __init__(self, name=None):
        self.name = name

    def move(self, direction):
        '''
        Parameters:
            direction <Vector2>: Given any point in a unit circle, the angle represents the direction, and the magnitude represents the acceleration
        '''
        raise NotImplementedError

    def eject(self):
        '''
        Do sporulation
        '''
        raise NotImplementedError

    def eat(self, ball):
        '''
        Eat another ball
        '''
        raise NotImplementedError

    def stop(self):
        '''
        stop moving
        '''
        raise NotImplementedError

    def respawn(self):
        raise NotImplementedError