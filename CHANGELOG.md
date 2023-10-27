# Changelog

## Version 0.1.0
- Refactor for publication based on `RFC: ModelInterfaceV4`.
- added runtime_checkable decorator.
- Update objectmodels with changes from `aqsml-model`.
- Move annotation protocol to separate repository.
- Use static methods instead of properties.
- Remove mlflow and add custom logging class for metric, params, etc.
- Update type hinting to python 3.10 style (was 3.8).
- Changed structure of `InputData`.
- Add `TrainWindowSizePriority` to `DataLabelConfigTemplate`.
- Add basic custom exceptions to `objectmodels`.
- Remove train and predict logs in output of `train` and `predict`.

## Version 0.0.1
- Initial version of modelinterfaceV4.
