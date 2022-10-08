class BasePB:

    def __init__(self, playback_settings):
        self.playback_settings = playback_settings

    def need_save(self, last_frame_count, *args, **kwargs):
        raise NotImplementedError

    def save_step(self, *args, **kwargs):
        raise NotImplementedError

    def save_final(self, *args, **kwargs):
        raise NotImplementedError
