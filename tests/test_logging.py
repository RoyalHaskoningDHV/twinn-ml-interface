import tempfile
import unittest
from pathlib import Path

from PIL import Image

from twinn_ml_interface.objectmodels import MetaDataLogger, Metric


class TestMetaDataLogger(unittest.TestCase):
    def setUp(self):
        self.md_logger = MetaDataLogger()
        self.test_image = Image.new("RGB", (100, 100), (255, 255, 255)).tobytes()
        self.test_image2 = Image.new("RGB", (100, 100), (0, 0, 0)).tobytes()

    def test_log_metrics(self):
        metrics = [Metric("m1", 0.7), Metric("m2", 200)]
        self.md_logger.log_metrics(metrics)
        assert self.md_logger.metrics == metrics, "log_metrics failed"

    def test_log_params(self):
        params = {"p1": 0.7, "p2": 200}
        self.md_logger.log_params(params)
        assert self.md_logger.params == params, "log_params failed"

    def test_is_metric_in_metrics(self):
        metrics = [Metric("m1", 0.7), Metric("m2", 200)]
        self.md_logger.log_metrics(metrics)
        assert self.md_logger.is_metric_in_metrics("m1")
        assert not self.md_logger.is_metric_in_metrics("m9")
        assert self.md_logger.is_metric_in_metrics("m1", 0.7)
        assert not self.md_logger.is_metric_in_metrics("m1", 0.8)

    def test_get_metric_value(self):
        metrics = [Metric("m1", 0.7), Metric("m2", 200)]
        self.md_logger.log_metrics(metrics)
        assert self.md_logger.get_metric_value("m1") == 0.7

    def test_db_logs(self):
        db_logs = {"scores_custom_metric": [1, 2, 3], "important_parameter": 200}
        self.md_logger.log_db_logs(db_logs)
        assert self.md_logger.db_logs == db_logs, "log_params failed"

    def test_log_artifact(self):
        label = "tmpfile"
        with tempfile.TemporaryFile() as tmpfile:
            self.md_logger.log_artifacts_in_dir(tmpfile, label)
            assert self.md_logger.artifacts == {tmpfile: label}, "log_artifact failed"

    def test_log_artifacts_in_multiple_dirs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile1 = str(Path(tmpdir) / "tmpfile1")
            tmpfile2 = str(Path(tmpdir) / "tmpfile2")
            with open(tmpfile1, "wb") as f:
                f.write(self.test_image)
            with open(tmpfile2, "wb") as f:
                f.write(self.test_image2)
            self.md_logger.log_artifacts_in_multiple_dirs({tmpfile1: None, tmpfile2: None})
            assert self.md_logger.artifacts == {
                tmpfile1: None,
                tmpfile2: None,
            }, "log_artifacts failed"

    def test_get_artifact_names(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = str(Path(tmpdir) / "tmpfile1")
            with open(tmpfile, "wb") as f:
                f.write(self.test_image)
            self.md_logger.log_artifacts_in_dir(tmpfile)

            assert self.md_logger.get_artifact_names() == {"tmpfile1"}

    def test_reset_cache(self):
        self.md_logger.metrics = [Metric("m1", 0)]
        self.md_logger.params = {"p1": 1}
        self.md_logger.db_logs = {"p2": 2}
        self.md_logger.artifacts = {"my_folder/": None}
        self.md_logger.reset_cache()
        assert self.md_logger.metrics == []
        assert self.md_logger.params == {}
        assert self.md_logger.artifacts == {}
        assert self.md_logger.db_logs == {}
