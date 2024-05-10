# Twinn-ml-interface

[![PyPI Latest Release](https://img.shields.io/pypi/v/twinn-ml-interface.svg)](https://pypi.org/project/twinn-ml-interface/)
[![Downloads](https://static.pepy.tech/personalized-badge/twinn-ml-interface?period=month&units=international_system&left_color=black&right_color=orange&left_text=PyPI%20downloads%20per%20month)](https://pepy.tech/project/twinn-ml-interface)
[![License](https://img.shields.io/pypi/l/twinn-ml-interface.svg)](https://github.com/RoyalHaskoningDHV/twinn-ml-interface/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Twinn-ml-interface is a Python package for *data contracts between machine learning code and infrastructure*. This contract ensures smooth onboarding of machine learning models onto the Twinn-ml-platform by Royal HaskoningDHV.

Author: [Royal HaskoningDHV](https://global.royalhaskoningdhv.com/)



### Installation

The easiest way to install this package is using pip:
```
pip install twinn-ml-interface
```

## Model Interface

### Purpose

The Model Interface defines the required methods and attributes that any ML model needs to have in order to run in the Royal HaskoningDHV Twinn-ml infrastructure.

## Testing compliance of your model with the data contract
### Instance of the Model Interface

Once all the attributes and methods from the __Protocol__ `ModelInterfaceV4` are implemented, including the correct type-hints / annotations, we can check if a model is compliant with the interface by doing an `isinstance` check with `ModelInterfaceV4`. You can find a base test in `twinn_ml_interface/interface/model_test.py`. The [Darrow-Poc](https://github.com/RoyalHaskoningDHV/darrow-poc) is an example of a model that follows the ModelInterfaceV4.

### Mock Executors

The `executor` class takes care of running the model either for training or predictions in the Twinn-ml infrastructure. Here, we implemented a mock executor to emulate that behaviour to some extent, which hopefully makes it a little clearer in what context the model class will be used. Any model compliant with the ModelInterface should be able to train and predict using the `ExecutorMock` that can be found in `twinn_ml_interface/mocks/mocks.py`. The [Darrow-Poc](https://github.com/RoyalHaskoningDHV/darrow-poc) is an example of a model that follows `ModelInterfaceV4` and can run using the `ExecutorMock`.

The steps and methods that the infrastructure and the mock executor run during training are:
1. Read config:
    - `get_target_template()`
    - `get_train_window_finder_config_template()`
2. Initialize the model
    - `initialize()`
3. Given the configuration for the train window finder in the previous steps, validate possible windows:
    - `validate_input_data()`
4. Read the data configuration to download all the needed data in a window selected by the previous step:
    - `get_data_config_template()`
5. Transform the input data as needed:
    - `preprocess()`
6. Train:
    - `train()`
7. Store the model:
    - `dump()`

When the training is finished, the model can be used for predicting. The prediction steps are:
1. Retrieve the model from storage and load it:
    - `load()`
2. Fetch the data needed for prediction based on **either**:
    -  `base_features` - if present
    - `get_data_config_template()` - otherwise
3. Predict:
    - `predict()`
4. Load configuration to post predictions:
    - `get_result_template()`

## Example of the Model Interface
### Darrow Poc
The [Darrow-Poc](https://github.com/RoyalHaskoningDHV/darrow-poc) is an example of a model that follows `ModelInterfaceV4`. It contains more detailed explanations of the data model, interface methods and the onboarding process.
