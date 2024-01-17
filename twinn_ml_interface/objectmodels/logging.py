from dataclasses import dataclass
from datetime import datetime, timezone
from os import PathLike, listdir
from os.path import isdir, isfile
from typing import Hashable


@dataclass
class Metric:
    key: str
    value: float
    timestamp: int = 0
    step: int = 0


class MetaDataLogger:
    """A logging object with specific methods to keep track of metrics, parameters,
    artifacts/files and images one might want to log to mlflow later on. The information is
    stored in the object until `self.reset_cache()` is called. For larger objects it is
    also possible to log them to file temporarily.

    **Disclaimer**: Notice that `metrics`, `params`, `artifacts` and `db_logs` will only be
    logged during training. `prediction_log` will be logged only during prediction.

    Examples
    --------
    >>> # Log metrics
    >>> md_logger = MetaDataLogger()
    >>> metrics = [Metric('r2_score', 0.7 ), Metric('num_sensors', 200)]
    >>> md_logger.log_metrics(metrics)
    >>> print(md_logger.metrics)
    ...
    >>> # Reset cache
    >>> md_logger.reset_cache()
    >>> print(md_logger.metrics)
    """

    metrics: list[Metric]
    params: dict[str, str]
    artifacts: dict[str | PathLike, str | None]
    db_logs: dict[str, Hashable]
    prediction_log: list[str]

    def __init__(self):
        self.reset_cache()

    def log_metric(self, metric: Metric):
        """Log a Metric.

        Metrics with the same Metric.key but different attributes can be used to create graphs.

        Args:
            metric (Metric): Any Metric
        """
        self.metrics.append(metric)

    def log_metrics(self, metrics: list[Metric]):
        """Log multiple metrics

        Args:
            metrics (list[Metric]) : Each element is a metric
        """
        self.metrics += metrics

    def log_params(self, params: dict[str, str]):
        """Log multiple parameters. If parameter was logged in same run before, it is overwritten.

        Args:
            params (dict[str, str]): Each dictionary entry denotes one parameter
                as key value pair.
        """
        self.params |= params

    def log_db_logs(self, db_log: dict[str, Hashable]):
        """Log special elements that will be stored in a DB (access by API). If the element was
        logged in the same run before, it is overwritten.

        Args:
            params (dict[str, Hashable]): Each dictionary entry denotes one lo as key value pair.
        """
        self.db_logs |= db_log

    def log_artifacts_in_dir(self, local_dir: PathLike, label: str | None = None):
        """Log an artifact / file.

        Args:
            local_dir (PathLike): Path to file or folder to log
            label(str | None): Label of how to group this artifact with others. Defaults to None.
        """
        self.artifacts[local_dir] = label

    def log_artifacts_in_multiple_dirs(self, artifacts: dict[PathLike, str | None]):
        """Log multiple artifacts / files.

        Args:
            artifacts (dict[str, str | None]): List of dictionaries with paths of
                artifacts / files to log as keys and grouping labels as values (can be None)
        """
        self.artifacts |= artifacts

    def is_metric_in_metrics(self, metric_name: str, metric_value: float | None = None) -> bool:
        """Check is a certain metric is inside the logger

        Args:
            metric_name (str): the metric to check
            metric_value (float | None, optional): The value of the metric, will be checked only
                if provided. Defaults to None.

        Returns:
            bool: wether if the metric is inside the logger with a certain value (optional)
        """
        for element in self.metrics:
            if metric_name == element.key and (
                metric_value is None or metric_value == element.value
            ):
                return True
        return False

    def get_metric_value(self, metric_name: str) -> float | None:
        """Get the metric value from the logger if it exists, else None

        Args:
            metric_name (str): the metric to check

        Returns:
            float | None: MEtrics value if exists, else None
        """
        for element in self.metrics:
            if metric_name == element.key:
                return element.value
        return None

    def get_artifact_names(self) -> set[str]:
        """Get get all artifact names that have been stored in the logger

        Returns:
            set[str]: a set with the names of all the artifacts stored
        """
        artifact_names = set()
        for path in self.artifacts:
            if isfile(path):
                artifact_names.add(path.split("/")[-1].split(".")[0])
            elif isdir(path):
                for image_filename in listdir(path):
                    artifact_names.add(image_filename.split(".")[0])
        return artifact_names

    def log_prediction_string(self, prediction_log: str):
        """You cannot log metrics, parameters or artifacts during predictions,
        but you can pass a string that will be logged for a given prediction run.

        Args:
            prediction_log (str): Some information to log for a prediction run.
        """
        self.prediction_log.append(prediction_log)

    def reset_cache(self):
        """Clear all stored items in logger cache."""
        self.created_on = datetime.now(timezone.utc)
        self.metrics = []
        self.params = {}
        self.artifacts = {}
        self.db_logs = {}
        self.prediction_log = []
