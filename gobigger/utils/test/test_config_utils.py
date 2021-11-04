import os
import logging
import pytest
from easydict import EasyDict

from gobigger.utils import deep_merge_dicts

logging.basicConfig(level=logging.DEBUG)


def test_deep_merge_dicts():
    a = EasyDict(dict(
        name='aaa',
        content=dict(
            team_num=4,
            map_width=1000
        )
    ))
    b = EasyDict(dict(
        name='bbb',
        content=dict(
            map_width=2000
        )
    ))
    c = deep_merge_dicts(a, b)
    assert c.name == 'bbb'
    assert c.content.map_width == 2000
    assert c.content.team_num == 4
