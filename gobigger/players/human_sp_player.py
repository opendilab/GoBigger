from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall
from .human_player import HumanPlayer


class HumanSPPlayer(HumanPlayer):

    def __init__(self, cfg, team_id, player_id, border, spore_settings, sequence_generator=None):
        super(HumanSPPlayer, self).__init__(cfg, team_id, player_id, border, spore_settings)
        assert sequence_generator is not None
        self.sequence_generator = sequence_generator

    def move(self, ball_id=None, direction=None, duration=0.05):
        if ball_id is None:
            for ball_id, ball in self.balls.items():
                ball.move(given_acc=direction, duration=duration)
                ball.score_decay()
        else:
            if ball_id in self.balls:
                self.balls[ball_id].move(given_acc=direction, duration=duration)
                self.balls[ball_id].score_decay()

    def eject(self, ball_id=None, direction=None):
        ret = []
        if ball_id and ball_id in self.balls:
            ret.append(self.balls[ball_id].eject(direction=direction))
        return ret

    def split(self, ball_id=None, direction=None):
        if ball_id and ball_id in self.balls:
            ret = self.balls[ball_id].split(self.get_clone_num(), direction=direction)
            if ret and isinstance(ret, CloneBall):
                self.add_balls(ret)
        return True

    def respawn(self, position):
        ball = CloneBall(ball_id=self.sequence_generator.get(), position=position, border=self.border, 
                         score=self.ball_settings.score_init, team_id=self.team_id, 
                         player_id=self.player_id, spore_settings=self.spore_settings, 
                         sequence_generator=self.sequence_generator, **self.ball_settings)
        self.balls = {}
        self.balls[ball.ball_id] = ball   
        return True 
