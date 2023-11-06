from datetime import datetime, timezone
from dataclasses import dataclass

from typing import Any


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
    params: dict[str, Any]
    artifacts: list[dict[str, str | None]]

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

    def log_params(self, params: dict):
        """Log multiple parameters. If parameter was logged in same run before, it is overwritten.

        Args:
            params (dict): Each dictionary entry denotes one parameter description: value pair.
        """
        self.params |= params

    def log_artifact(self, artifact_path: str, label: str | None = None):
        """Log an artifact / file.

        Args:
            artifact_path (str): Path to file to log
            label(str | None): Label of how to group this artifact with others. Defaults to None.
        """
        self.artifacts.append({artifact_path: label})

    def log_artifacts(self, artifacts: list[dict[str, str | None]]):
        """Log multiple artifacts / files.

        Args:
            artifacts (list[dict[str, str | None]]): List of dictionaries with paths of
                artifacts / files to log as keys and grouping labels as values (can be None)
        """
        self.artifacts.extend(artifacts)

    def reset_cache(self):
        """Clear all stored items in logger cache."""
        self.created_on = datetime.now(timezone.utc)
        self.metrics = []
        self.params = {}
        self.artifacts = []
