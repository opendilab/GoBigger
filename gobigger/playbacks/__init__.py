import importlib

from .base_pb import BasePB
from .null_pb import NullPB
from .video_pb import VideoPB
from .frame_pb import FramePB
from .action_pb import ActionPB


def create_pb(playback_settings, **kwargs):
    playback_type = playback_settings.playback_type
    if playback_type == 'none':
        return NullPB(None)
    elif playback_type == 'by_video':
        return VideoPB(playback_settings['by_video'], **kwargs)
    elif playback_type == 'by_frame':
        return FramePB(playback_settings['by_frame'], **kwargs)
    elif playback_type == 'by_action':
        return ActionPB(playback_settings['by_action'], **kwargs)
    else:
        raise NotImplementedError
