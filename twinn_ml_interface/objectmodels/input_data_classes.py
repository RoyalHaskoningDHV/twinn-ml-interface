import logging
from collections.abc import MutableMapping

import pandas as pd


class InputData(dict[str, pd.DataFrame]):
    def __init__(self, mapping: dict[str, pd.DataFrame] | None = None, **kwargs) -> None:
        if mapping:
            if not isinstance(mapping, dict):
                msg = "Input must be a dict"
                raise TypeError(msg)
            self._check_valid_mapping(mapping)
            _mapping = mapping
        else:
            _mapping = {}

        if kwargs:
            self._check_valid_mapping(kwargs)
        super().__init__(_mapping, **kwargs)

    def _validate_element(self, key, value) -> None:
        if not isinstance(key, str):
            msg = "Keys must be of type str"
            raise TypeError(msg)
        if not isinstance(value, pd.DataFrame):
            msg = "Values must be of type pandas.DataFrame"
            raise TypeError(msg)
        if key not in value.columns:
            msg = f"key {key} needs to be a column in the pandas.DataFrame"
            raise ValueError(msg)
        if not isinstance(value.index, pd.DatetimeIndex):
            raise TypeError(f"The index from {key} dataframe is not of type pandas.DatetimeIndex")
        if not isinstance(value.index.name, str) or value.index.name != "TIME":
            raise TypeError(f"The index from {key} dataframe should be named 'TIME'")

    def _check_valid_mapping(self, element: dict) -> None:
        for key, value in element.items():
            self._validate_element(key=key, value=value)

    def __setitem__(self, key, value) -> None:
        self._validate_element(key=key, value=value)
        super().__setitem__(key, value)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, MutableMapping):
            raise TypeError("A dict-like object is needed to compare")
        if set(self.keys()) != set(__value.keys()):
            logging.info("Dict keys are different")
            return False
        for key, df in self.items():
            if not df.equals(__value[key]):
                logging.info(f"DataFrame in {key} is different")
                return False
        return True

    def get_unit_codes(self) -> list[str]:
        """Get a list of all the unit codes in the dictionary.

        Returns:
            list[str]: the unit codes
        """
        return [key.split(":")[0] for key in self]

    def get_ids(self) -> list[str]:
        """Get a list of all the ids (unit code:tag) in the dictionary.

        Returns:
            list[str]: the ids
        """
        return list(self)

    def get_max_time(self) -> pd.Timestamp:
        """Get the max time of all timestamps.

        Returns:
            pd.Timestamp: The biggest timestap
        """
        return max([v.index.max() for _, v in self.items()])

    def get_min_time(self) -> pd.Timestamp:
        """Get the min time of all timestamps.

        Returns:
            pd.Timestamp: The smallest timestap
        """
        return min([v.index.min() for _, v in self.items()])

    def to_long_format(self):
        data = []
        for k, v in self.items():
            id_, type_ = k.split(":")
            long_format = v.rename(columns={k: "VALUE"})
            long_format["ID"] = id_
            long_format["TYPE"] = type_
            long_format.reset_index(names="TIME", inplace=True)
            data.append(long_format)

        return pd.concat(data).reset_index(drop=True)

    @classmethod
    def from_long_df(cls, df: pd.DataFrame) -> "InputData":
        data_chunks = {}
        for name, chunk in df.groupby(["ID", "TYPE"]):
            new_name = ":".join(name)
            chunk.set_index("TIME", inplace=True)
            chunk.drop(columns=["ID", "TYPE"], inplace=True)
            chunk.rename(columns={"VALUE": new_name}, inplace=True)
            data_chunks[new_name] = chunk.sort_index()
        return cls(data_chunks)
