class TestModelInterface:
    """
    Base class for testing if models follow the model interface
    Example:
    ```
    class TestProductModel(TestModelInterface, unittest.TestCase):
        testmodel = TestModelInterface(YourProductModel, INTERFACE, BASE_MODEL)

        def test_model_follows_interface(self):
            self.testmodel.model_isinstance_interface_test()
            self.testmodel.model_inherits_base_model_test()
            self.testmodel.model_accepts_kwargs_test()
    """

    def __init__(self, model, interface) -> None:
        self.model = model
        self.interface = interface

    def test_model_isinstance_interface(self):
        if not isinstance(self.model, self.interface):
            raise TypeError("model is not an instance of interface")

    def test_model_inherits_base_model(self, base_model):
        if not issubclass(self.model, base_model):
            raise ValueError("model is not a subclass of base_model")
