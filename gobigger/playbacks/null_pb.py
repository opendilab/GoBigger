from .base_pb import BasePB


class NullPB(BasePB):

    def need_save(self, *args, **kwargs):
        return False

    def save_step(self, *args, **kwargs):
        return

    def save_final(self, *args, **kwargs):
        return
