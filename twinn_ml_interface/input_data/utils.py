from datetime import datetime

import pandas as pd

from .input_data import InputData


def concat(*data_objects: InputData) -> InputData:
    result = InputData()
    for data in data_objects:
        result |= {
            feature: pd.concat([result[feature], data[feature]], sort=True)
            for feature in data.unit_tags.intersection(result.unit_tags)
        }
        result |= {
            feature: data[feature] for feature in data.unit_tags.difference(result.unit_tags)
        }
    return result


def take_slice(data: InputData, start: datetime, end: datetime) -> InputData:
    result = InputData()
    for feature, df in data.items():
        result[feature] = df.loc[
            (df.index >= pd.to_datetime(start, utc=True).to_pydatetime())
            & (df.index <= pd.to_datetime(end, utc=True).to_pydatetime())
        ]
    return result
