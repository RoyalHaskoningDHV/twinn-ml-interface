# Run TestModelInterface
# Run mocks

import unittest

from ..interface import ModelInterfaceV4, TestModelInterface

INTERFACE = ModelInterfaceV4


class TestModelInterfaceVariations(unittest.TestCase):
    
    def setUp(self):
        self.testmodel = TestModelInterface(SewrFutureMax, INTERFACE, model1)

    def test_model_follows_interface(self):
        self.testmodel.test_model_isinstance_interface()
        self.testmodel.test_model_inherits_base_model()
        self.testmodel.test_model_accepts_kwargs()