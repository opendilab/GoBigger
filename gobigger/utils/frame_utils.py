import os
import sys
import pickle


def save_frame_info(self, save_frame_full_path, food_balls, thorns_balls, spore_balls, clone_balls):
    if save_frame_full_path != '':
        frame_info = {'food': [], 'thorns': [], 'spore': [], 'clone': []}
        # food
        for ball in food_balls:
            frame_info['food'].append([ball.position.x, ball.position.y, ball.radius])
        # thorns
        for ball in thorns_balls:
            frame_info['thorns'].append([ball.position.x, ball.position.y, ball.radius, ball.vel.x, ball.vel.y,
                                       ball.acc.x, ball.acc.y, ball.move_time, ball.moving])
        # spore
        for ball in spore_balls:
            frame_info['spore'].append([ball.position.x, ball.position.y, ball.radius, ball.direction.x, 
                                       ball.direction.y, ball.vel.x, ball.vel.y,
                                       ball.acc.x, ball.acc.y, ball.move_time, ball.moving])
        # clone
        for ball in clone_balls:
            frame_info['clone'].append([ball.position.x, ball.position.y, ball.radius, ball.owner, 
                                       ball.team_name, ball.vel.x, ball.vel.y, ball.acc.x, ball.acc.y, 
                                       ball.vel_last.x, ball.vel_last.y, ball.acc_last.x, ball.acc_last.y, 
                                       ball.direction.x, ball.direction.y, ball.last_given_acc.x, 
                                       ball.last_given_acc.y, ball.age, ball.cooling_last, ball.stop_flag,
                                       ball.stop_time, ball.acc_stop.x, ball.acc_stop.y])
        with open(save_frame_full_path, 'wb') as f:
            pickle.dump(frame_info, f)

def load_frame_info():
    custom_init_food = []
    custom_init_thorns = []
    custom_init_spore = []
    custom_init_clone = []
    if frame_path:
        with open(frame_path, 'rb') as f:
            data = pickle.load(f)
        custom_init_food = data['food']
        custom_init_thorns = data['thorns']
        custom_init_spore = data['spore']
        custom_init_clone = data['clone']
    return custom_init_food, custom_init_thorns, custom_init_spore, custom_init_clone