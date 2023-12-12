# Twinn-ml-interface

[![PyPI Latest Release](https://img.shields.io/pypi/v/twinn-ml-interface.svg)](https://pypi.org/project/twinn-ml-interface/)
[![Downloads](https://static.pepy.tech/personalized-badge/twinn-ml-interface?period=month&units=international_system&left_color=black&right_color=orange&left_text=PyPI%20downloads%20per%20month)](https://pepy.tech/project/twinn-ml-interface)
[![License](https://img.shields.io/pypi/l/twinn-ml-interface.svg)](https://github.com/RoyalHaskoningDHV/twinn-ml-interface/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Twinn-ml-interface is a Python package for *data contracts between machine learning code and infrastructure*.

Author: [Royal HaskoningDHV](https://global.royalhaskoningdhv.com/)



### Installation

The easiest way to install is package is using pip:
```
pip install twinn-ml-interface
```

## Model Interface

### Properties
#### **model_type_name**
An unique name for each model class.

#### **model_category**
Whether the model outputs anomalies, predictions or actuals. This determines the format in which the results are expected.

#### **performance_value**
The model is expected to calculate some metric value after training to indicate the model performance.

#### **train_data_config**
N/A for most cases.

#### **target_tag**
For most cases, return a UnitTagLiteral containing the unit code and tagname of the target of the model.

#### **data_config**
For most cases, return a list of UnitTagLiterals containing all the data that is used for training the model. The training window can be passed at runtime.

#### **result_tag**
For most cases, return a UnitTagLiteral of the result unit and tag of the model.

#### **unit_properties_template**
N/A for most cases.

#### **unit_hierarchy_template**
N/A for most cases.

#### **train_window_finder_config_template**
N/A for most cases.

### Training
For training, the functions of the model interface are called in the following order:

1. initialize
2. preprocess
3. validate_input_data
4. train
5. dump

### Prediction
For prediction, the functions of the model interface are called in the following order:
1. load
2. predict