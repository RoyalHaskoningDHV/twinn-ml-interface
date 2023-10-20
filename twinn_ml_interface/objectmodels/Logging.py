from datetime import datetime


class MetaDataLogger():
    """A logging object with specific methods to keep track of metrics, parameters,
    artifacts/files and images one might want to log to mlflow later on. The information is
    stored in the object until `self.reset_cache()` is called. For larger objects it is
    also possible to log them to file temporarily.

    Examples
    --------
    >>> # Log metrics
    >>> md_logger = MetaDataLogger()
    >>> metrics = {'r2_score': 0.7, 'num_sensors': 200}
    >>> md_logger.log_metrics(metrics)
    >>> print(md_logger.metrics)
    ...
    >>> # Log image
    >>> from PIL import Image
    ...
    >>> my_image = Image.new("RGB", (400, 400), (255, 255, 255))
    >>> md_logger.log_image(my_image.tobytes(), image_path="images")
    >>> print(md_logger.images)
    ...
    >>> # Log image to temporary file to save RAM
    >>> md_logger.log_image_to_hd(my_image.tobytes(), image_path="images")
    >>> print(md_logger.images_hd)
    ...
    >>> # Reset cache
    >>> md_logger.reset_cache()
    >>> print(md_logger.metrics)
    """
    def __init__(self):
        self.reset_cache()

    def log_metrics(self, metrics: dict):
        """Log multiple metrics. If metric was logged in the same run before, it is overwritten.

        Parameters
        ----------
        metrics: dict
            Each dictionary entry denotes one metric description: value pair.
        """
        self.metrics = self.metrics | metrics

    def log_params(self, params: dict):
        """Log multiple parameters. If parameter was logged in same run before, it is overwritten.

        Parameters
        ----------
        params: dict
            Each dictionary entry denotes one parameter description: value pair.
        """
        self.params = self.params | params

    def log_artifact(self, artifact_path: str, label: str = None):
        """Log an artifact / file.

        Parameters
        ----------
        artifact_path: str
            Path to file to log
        label: str (default=None)
            Label of how to group this artifact with others
        """
        self.artifacts.append({artifact_path, label})

    def log_artifacts(self, artifacts: list[dict[str, str | None]]):
        """Log multiple artifacts / files.

        Parameters
        ----------
        artifacts: list[dict[str, str | None]]
            List of dictionaries with paths of artifacts / files to log as keys and
            grouping labels as values (can be None)
        """
        self.artifacts.extend(artifacts)

    def log_image(self, image: bytes, image_path: str):
        """Log an image.

        Parameters
        ----------
        image: bytes
            image data to log
        image_path: str
            path where to save the image as binary later on if using mlflow.
        """
        self.images.append({image: image_path})

    def log_images(self, images: list[dict[bytes, str]]):
        """Log multiple images.

        Parameters
        ----------
        images: list[dict[bytes, str]]
            List of dictionaries, where each entry is a pair of bytes and strings denoting
            the images to save and the paths where to save them later on if using mlflow.
        """
        self.images.extend(images)

    def log_image_to_hd(self, image: bytes, image_path: str):
        """Save an image to hard-drive, log the path.

        Parameters
        ----------
        image: bytes
            image data to log
        image_path: str
            path where to save the image
        """
        with open(image_path, 'wb') as f:
            f.write(image)
        self.images_hd.append(image_path)

    def reset_cache(self):
        """Clear all stored items in logger cache."""
        self.created_on = datetime.now()
        self.metrics = {}
        self.params = {}
        self.artifacts = []
        self.images = []
        self.images_hd = []
