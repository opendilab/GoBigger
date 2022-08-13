import os
import cv2
import numpy as np
import logging
import uuid
import copy
import pickle
import lz4.frame

from .base_pb import BasePB


class FramePB(BasePB):

    def __init__(self, playback_settings, **kwargs):
        self.playback_settings = playback_settings
        self.save_frame = self.playback_settings.save_frame
        self.save_all = self.playback_settings.save_all
        self.save_partial = self.playback_settings.save_partial
        self.save_dir = self.playback_settings.save_dir
        self.save_name_prefix = self.playback_settings.save_name_prefix
        if self.save_frame:
            if not os.path.isdir(self.save_dir):
                try:
                    os.makedirs(self.save_dir)
                except:
                    pass
                logging.warning('save_dir={} must be an existed directory!'.format(self.save_dir))
            if not self.save_name_prefix:
                self.save_name_prefix = str(uuid.uuid1())
        self.playback_data = {}

    def need_save(self, *args, **kwargs):
        return self.save_frame

    def save_step(self, diff_balls_remove, diff_balls_modify, leaderboard, last_frame_count, *args, **kwargs):
        self.playback_data[last_frame_count] = [diff_balls_modify, diff_balls_remove, leaderboard]

    def save_final(self, cfg, *args, **kwargs):
        self.playback_data['cfg'] = cfg
        self.playback_path = os.path.join(self.save_dir, self.save_name_prefix + '.pb')
        compressed_data = lz4.frame.compress(pickle.dumps(self.playback_data))
        with open(self.playback_path, 'wb') as f:
            pickle.dump(compressed_data, f)
        logging.info('save pb at {}'.format(self.playback_path))

