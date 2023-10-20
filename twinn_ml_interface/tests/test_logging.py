from pathlib import Path
import tempfile
import unittest

from PIL import Image

from twinn_ml_interface.objectmodels import MetaDataLogger


class TestMetaDataLogger(unittest.TestCase):
    def setUp(self):
        self.md_logger = MetaDataLogger()
        self.test_image = Image.new("RGB", (100, 100), (255, 255, 255)).tobytes()
        self.test_image2 = Image.new("RGB", (100, 100), (0, 0, 0)).tobytes()

    def test_log_metrics(self):
        metrics = {'m1': 0.7, 'm2': 200}
        self.md_logger.log_metrics(metrics)
        assert self.md_logger.metrics == metrics, 'log_metrics failed'

    def test_log_params(self):
        params = {'p1': 0.7, 'p2': 200}
        self.md_logger.log_params(params)
        assert self.md_logger.params == params, 'log_params failed'

    def test_log_artifact(self):
        label = "tmpfile"
        with tempfile.TemporaryFile() as tmpfile:
            self.md_logger.log_artifact(tmpfile, label)
            assert self.md_logger.artifacts[-1] == {tmpfile, label}, 'log_artifact failed'

    def test_log_artifacts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile1 = str(Path(tmpdir) / "tmpfile1")
            tmpfile2 = str(Path(tmpdir) / "tmpfile2")
            with open(tmpfile1, 'wb') as f:
                f.write(self.test_image)
            with open(tmpfile2, 'wb') as f:
                f.write(self.test_image2)
            self.md_logger.log_artifacts([{tmpfile1}, {tmpfile2}])
            assert self.md_logger.artifacts == [{tmpfile1}, {tmpfile2}], 'log_artifacts failed'

    def test_log_image(self):
        self.md_logger.log_image(self.test_image, "image")
        assert self.md_logger.images == [{self.test_image: "image"}], 'log_image failed'

    def test_log_images(self):
        self.md_logger.log_images([{self.test_image: "image1"}, {self.test_image2: "image2"}])
        assert self.md_logger.images[-2] == {self.test_image: "image1"}, 'log_images failed'
        assert self.md_logger.images[-1] == {self.test_image2: "image2"}, 'log_images failed'

    def test_log_image_to_hd(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            image_path = str(Path(tmpdir) / "image")
            self.md_logger.log_image_to_hd(self.test_image, image_path)
            with open(image_path, 'rb') as f:
                assert f.read() == self.test_image, 'log_image_to_hd failed'

    def test_reset_cache(self):
        self.md_logger.metrics = {'m1': 0}
        self.md_logger.params = {'p1': 1}
        self.md_logger.artifacts = [123]
        self.md_logger.images = [456]
        self.md_logger.images_hd = [789]
        self.md_logger.reset_cache()
        assert self.md_logger.metrics == {}
        assert self.md_logger.params == {}
        assert self.md_logger.artifacts == []
        assert self.md_logger.images == []
        assert self.md_logger.images_hd == []
