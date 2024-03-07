import unittest

from twinn_ml_interface.mocks import ConfigurationMock
from twinn_ml_interface.objectmodels import Configuration


class TestMetaDataLogger(unittest.TestCase):
    def test_mock_follows_interface(self):
        config = ConfigurationMock("", "", {}, [], [])
        assert isinstance(config, Configuration)
