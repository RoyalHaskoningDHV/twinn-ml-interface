# Changelog

## Version 0.5.0
- Removed `Node` class, since the ML models do not interact with it.

## Version 0.4.0
- Removed `transform` function from `DataLabelConfigTemplate` and replaced by `horizon` parameter, that can be used to request future data (useful for `ModelCategory.PREDICTION`)

## Version 0.3.2
- Fix hash from `UnitTag`.

## Version 0.3.1
- Add pipelines for publishing to `pypi`, `testpypi`.
- Remove old pipeline to publish to `SAM` artifacts.

## Version 0.3.0
- Added `mocks/`
- Added description to README.md
- Added `tutorials/`

## Version 0.2.11
- `InputData.max_datetime` and `InputData.min_datetime` now always return a datetime, even if one element is an empty `pd.DataFrame`.

## Version 0.2.10
- `InputData` now is sorted by the index.

## Version 0.2.9
- Simplified `UnitTag`.

## Version 0.2.8
- Add property `Configuration.modelled_unit_code`, that can be used when the target of the model is not the same as the modelled unit.

## Version 0.2.7
- Only allow returning `list[DataLabelConfigTemplate]` in interface method `get_data_config_template`.
- In `DataLabelConfigTemplate` `unit_tag_templates` can be `list[DataLabelConfigTemplate]` or `list[UnitTag]`.
- `DataLabelConfigTemplate.AvailabilityLevel` gets default `All`.

## Version 0.2.6
- Modified `log_prediction_string` so it can be used multiple times.
- Removed legacy `TestModelInterfcae.test_model_accepts_kwargs`.

## Version 0.2.5
- Add `MetaDataLogger` and `Configuration` to `load` method of `ModelInterfaceV4`
- Make `load` method of `ModelInterfaceV4` a staticmethod
- Add `log_prediction_string` method to `MetaDataLogger`, which can be used to log a string later on in the database for a given prediction run.

## Version 0.2.4
- Added `LABEL` to `DataLabel` enum

## Version 0.2.3
- Add Github workflow for building the wheel

## Version 0.2.2
- Bug fix in `UnitTag.get_data_filter`: The whole objects of Unit and Tag were being used in the Filter() instead of just the str version of them.

## Version 0.2.1
- Changed type hint of `Unit.properties` to dict[str, Any]

## Version 0.2.0
- Refactor for publication based on `RFC: ModelInterfaceV4`.
- added runtime_checkable decorator.
- Move annotation protocol to separate repository.
- Use static methods instead of properties.
- Remove mlflow and add custom logging class for metric, params, etc.
- Update type hinting to python 3.10 style (was 3.8).
- Changed structure of `InputData`.
- Add `TrainWindowSizePriority` to `DataLabelConfigTemplate`.
- Add basic custom exceptions to `objectmodels`.
- Remove train and predict logs in output of `train` and `predict`.
- Add performance and a placeholder/dummy as output for `train`.
- Add placeholder/dummy as output for `predict`, together with predictions.

## Version 0.0.1
- Initial version of modelinterfaceV4.
