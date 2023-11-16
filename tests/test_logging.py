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

    def test_log_artifact(self):
        with tempfile.TemporaryFile() as tmpfile:
            self.md_logger.log_artifact(tmpfile)
            assert self.md_logger.artifacts[-1] == tmpfile, "log_artifact failed"

    def test_log_artifacts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile1 = str(Path(tmpdir) / "tmpfile1")
            tmpfile2 = str(Path(tmpdir) / "tmpfile2")
            with open(tmpfile1, "wb") as f:
                f.write(self.test_image)
            with open(tmpfile2, "wb") as f:
                f.write(self.test_image2)
            self.md_logger.log_artifacts([tmpfile1, tmpfile2])
            assert self.md_logger.artifacts == [
                tmpfile1,
                tmpfile2,
            ], "log_artifacts failed"

    def test_reset_cache(self):
        self.md_logger.metrics = {"m1": 0}
        self.md_logger.params = {"p1": 1}
        self.md_logger.artifacts = ["my_folder/"]
        self.md_logger.reset_cache()
        assert self.md_logger.metrics == []
        assert self.md_logger.params == {}
        assert self.md_logger.artifacts == []
