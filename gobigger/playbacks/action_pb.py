import os
import cv2
import numpy as np
import logging
import uuid
import copy
import pickle
import lz4.frame

from .base_pb import BasePB


class ActionPB(BasePB):

    def __init__(self, playback_settings, **kwargs):
        self.playback_settings = playback_settings
        self.save_action = self.playback_settings.save_action
        self.save_dir = self.playback_settings.save_dir
        self.save_name_prefix = self.playback_settings.save_name_prefix
        if self.save_action:
            if not os.path.isdir(self.save_dir):
                try:
                    os.makedirs(self.save_dir)
                except:
                    pass
                logging.warning('save_dir={} must be an existed directory!'.format(self.save_dir))
            if not self.save_name_prefix:
                self.save_name_prefix = str(uuid.uuid1())
        self.playback_data = {}
        logging.warning('`by_action` is not available now, please use `by_video` or `by_frame`.')

    def need_save(self, *args, **kwargs):
        return self.save_action

    def save_step(self, actions, last_frame_count):
        self.playback_data[last_frame_count] = actions

    def save_final(self, cfg, seed):
        self.playback_data['cfg'] = cfg
        self.playback_data['seed'] = seed
        self.playback_path = os.path.join(self.save_dir, self.save_name_prefix + '.ac')
        compressed_data = lz4.frame.compress(pickle.dumps(self.playback_data))
        with open(self.playback_path, 'wb') as f:
            pickle.dump(compressed_data, f)
        logging.info('save ac at {}'.format(self.playback_path))
