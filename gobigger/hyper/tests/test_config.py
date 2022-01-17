import logging
import pytest

from gobigger.hyper.configs.config_2f2s import server_default_config as c1
from gobigger.hyper.configs.config_2f2s_v2 import server_default_config as c2
from gobigger.hyper.configs.config_2f2s_v3 import server_default_config as c3
from gobigger.server import Server

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestHyperConfig:

    def test_2f2s(self):
        server = Server(c1)

    def test_2f2s_v2(self):
        server = Server(c2)

    def test_2f2s_v3(self):
        server = Server(c3)





