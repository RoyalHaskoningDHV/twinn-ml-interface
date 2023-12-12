import unittest

import pandas as pd

from twinn_ml_interface.input_data import InputData


class TestInputData(unittest.TestCase):
    def setUp(self):
        sensor1 = pd.DataFrame(
            {
                "TIME": pd.date_range(start="1970-01-01", periods=5, freq="1 H"),
                "ID": "SENSOR1",
                "TYPE": "TAG",
                "VALUE": [1, 2, 3, 4, 5],
            }
        ).astype({"VALUE": "float64"})

        sensor2 = pd.DataFrame(
            {
                "TIME": pd.date_range(start="1970-02-01", periods=3, freq="1 H"),
                "ID": "SENSOR2",
                "TYPE": "TAG",
                "VALUE": [7, 8, 9],
            }
        ).astype({"VALUE": "float64"})

        self.data = pd.concat([sensor1, sensor2]).reset_index(drop=True)

        self.test_df = pd.DataFrame(columns=["test"], index=pd.DatetimeIndex([], name="TIME"))
        self.foo_df = pd.DataFrame(columns=["foo"], index=pd.DatetimeIndex([], name="TIME"))

    def test_allowed_inits(self):
        assert InputData() == {}
        assert InputData({"test": self.test_df}) == {"test": self.test_df}
        assert InputData(test=self.test_df) == {"test": self.test_df}

    def test_not_allowed_inits(self):
        with self.assertRaises(TypeError):
            InputData(test1="test2")

        with self.assertRaises(TypeError):
            InputData({"test1": "test2"})

        with self.assertRaises(ValueError):
            InputData(new=self.test_df)

    def test_set_checks(self):
        input_data = InputData(foo=self.foo_df)
        input_data["new"] = pd.DataFrame(columns=["new"], index=pd.DatetimeIndex([], name="TIME"))

        assert set(input_data.unit_tags) == {"foo", "new"}

    def test_classmethod(self):
        input_data = InputData.from_long_df(self.data)

        assert set(input_data.unit_tags) == {"SENSOR1:TAG", "SENSOR2:TAG"}

    def test_min_time(self):
        input_data = InputData.from_long_df(self.data)
        assert input_data.min_datetime == pd.Timestamp("1970-01-01 00:00:00")

    def test_to_log_format(self):
        input_data = InputData.from_long_df(self.data)
        assert (input_data.to_long_format()[self.data.columns]).equals(self.data)
