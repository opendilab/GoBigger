import os
import cv2
import numpy as np
import logging

from gobigger.render import EnvRender


class PlaybackUtil:

    def __init__(self, playback_settings, game_fps, map_width, map_height):
        self.playback_settings = playback_settings
        self.game_fps = game_fps
        self.map_width = map_width
        self.map_height = map_height
        self.save_video = self.playback_settings.save_video
        self.save_fps = self.playback_settings.save_fps
        self.save_resolution = self.playback_settings.save_resolution
        self.save_all = self.playback_settings.save_all
        self.save_partial = self.playback_settings.save_partial
        self.save_dir = self.playback_settings.save_dir
        self.save_name_prefix = self.playback_settings.save_name_prefix
        if self.save_video:
            if not os.path.isdir(self.save_dir):
                try:
                    os.makedirs(self.save_dir)
                except:
                    pass
                logging.warning('save_dir={} must be an existed directory!'.format(self.save_path))
            if not self.save_name_prefix:
                self.save_name_prefix = str(uuid.uuid1())
            self.save_fps = int(self.save_fps)
            self.save_resolution = int(self.save_resolution)
            self.save_freq = self.game_fps // self.save_fps
        self.render = EnvRender(game_screen_width=self.save_resolution, game_screen_height=self.save_resolution, 
                                map_width=self.map_width, map_height=self.map_width)
        self.screens_all = []
        self.screens_partial = []

    def get_clip_screen(self, screen_data, rectangle):
        rectangle_tmp = copy.deepcopy(rectangle)
        left_top_x, left_top_y, right_bottom_x, right_bottom_y = rectangle_tmp
        left_top_x_fix = max(left_top_x, 0)
        left_top_y_fix = max(left_top_y, 0)
        right_bottom_x_fix = min(right_bottom_x, self.width)
        right_bottom_y_fix = min(right_bottom_y, self.height)

        if len(screen_data.shape) == 3:
            screen_data_clip = screen_data[left_top_x_fix:right_bottom_x_fix, 
                                           left_top_y_fix:right_bottom_y_fix, :]
            screen_data_clip = np.pad(screen_data_clip, 
                                      ((left_top_x_fix-left_top_x,right_bottom_x-right_bottom_x_fix),
                                       (left_top_y_fix-left_top_y,right_bottom_y-right_bottom_y_fix),
                                       (0,0)), 
                                      mode='constant')
        elif len(screen_data.shape) == 2:
            screen_data_clip = screen_data[left_top_x_fix:right_bottom_x_fix, 
                                           left_top_y_fix:right_bottom_y_fix]
            screen_data_clip = np.pad(screen_data_clip, 
                                      ((left_top_x_fix-left_top_x,right_bottom_x-right_bottom_x_fix),
                                       (left_top_y_fix-left_top_y,right_bottom_y-right_bottom_y_fix)), 
                                      mode='constant')
        else:
            raise NotImplementedError
        return screen_data_clip

    def need_save(self, last_frame_count):
        return self.save_video and last_frame_count % self.save_freq == 0

    def save_screen(self, food_balls, thorns_balls, spore_balls, players, player_num_per_team):
        self.screens_all.append(self.render.get_screen(food_balls, thorns_balls, spore_balls, players, player_num_per_team))

    def save_video_func(self):
        if self.save_video:
            if self.save_all:
                video_file_all = os.path.join(self.save_dir, '{}-all.mp4'.format(self.save_name_prefix))
                out = cv2.VideoWriter(video_file_all, cv2.VideoWriter_fourcc(*'mp4v'), self.save_fps, 
                                      (self.screens_all[0].shape[1], self.screens_all[0].shape[0]))
                for index, screen in enumerate(self.screens_all):
                    out.write(screen)
                out.release()
                cv2.destroyAllWindows()
            if self.save_partial:
                for player_id, screens in self.screens_partial.items():
                    video_file_partial = os.path.join(self.save_dir, '{}-{:02d}.mp4'.format(self.save_name_prefix, player_id))
                    out = cv2.VideoWriter(video_file_partial, cv2.VideoWriter_fourcc(*'mp4v'), self.save_fps, 
                                          (screens[0].shape[1], screens[0].shape[0]))
                    for index, screen in enumerate(self.screens):
                        if index % self.save_freq == 0:
                            out.write(screen)
                    out.release()
                    cv2.destroyAllWindows()
