import logging
import warnings
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

INDEX = ["ID", "TYPE", "TIME"]


def plot_marked_datapoints(
    sensor: pd.Series,
    marked_points: pd.Series,
    title: str = None,
    figsize: tuple[int, int] = (20, 10),
):
    """
    Given a pd.Series with sensor data and a boolean pd.Series marked_points with the
    same lenght, generates a figure with sensor data where sensor[marked_points] appear
    in a different color

    Parameters
    ----------
    sensor : pd.Series
        Raw data to be plotted
    marked_points : pd.Series
        Boolean series with the same length as sensor. Points from sensor data with
        marked_series == True will appear in a different color

    Returns
    -------
    matplotlib.figure.Figure
        Plot with marked points in a different color
    """
    fig = plt.figure(figsize=figsize)
    if title:
        plt.title(title)
    plt.plot(sensor, label="Original data", color="blue")
    plt.plot(sensor[~marked_points], label="Clean data", color="grey")
    plt.plot(sensor[marked_points], "o", label="Marked/Removed points", color="red")
    plt.legend()
    plt.close(fig)
    return fig


@dataclass
class InputData:
    samdata: dict[str, pd.DataFrame]
    labels: dict[str, pd.DataFrame] | None = None

    def get_insights_from_labels(
        self,
        labels_to_plot: list[str],
        target: str | None = None,
        log_all_sensors: bool = False,
    ) -> tuple[dict[str, float], dict[str, plt.Figure]]:
        """
        This method calculates and returns:
        - The percentage of missing values after applying the labels
        - Figures to visualize missing values

        Parameters
        ----------
        labels_to_plot : list[str]
            list of labels to plot
        target: str
            target sensor as "ID:TYPE"
        log_all_sensors: bool
            Wether to get insights from all sensors of only the target. Defaults to False

        Returns
        -------
        tuple[dict[str, float], dict[str, plt.Figure]]
            Two dictionaries, one containing missing values per sensor,
            and the second containing the figures
        """
        data_removed = {label: {} for label in self.formatted_labels}
        figures = {}
        if hasattr(self, "formatted_labels"):
            for label_name, label_set in self.formatted_labels.items():
                for sensor, chunk_samdata in self.samdata.groupby(["ID", "TYPE"], sort=False):
                    sensor_id = ":".join(sensor)
                    if label_name in labels_to_plot and (target is None or target == sensor_id or log_all_sensors):
                        key = f"{label_name}_{sensor_id}"
                        sorted_chunk = chunk_samdata.sort_values("TIME")
                        marked_points = pd.Series(
                            pd.MultiIndex.from_frame(sorted_chunk[INDEX]).isin(label_set),
                            index=sorted_chunk["TIME"],
                        )
                        # Percentage of datapoints removed by label
                        percentage_removed = np.round((marked_points.sum() / len(sorted_chunk)) * 100, 2)
                        data_removed[label_name][sensor_id] = percentage_removed
                        logger.info(f"{key}: {percentage_removed}%")
                        # Images
                        figures[key] = plot_marked_datapoints(
                            sensor=sorted_chunk.set_index("TIME")["VALUE"],
                            marked_points=marked_points,
                            title=key,
                        )
        else:
            warnings.warn("InputData.get_insights_from_labels requires calling apply_labels first")
        return data_removed, figures

    def _format_labels(self, labels_to_apply: list[str]) -> None:
        """
        Internal method to format the labels as a dictionary of sets, for convenience

        Parameters
        ----------
        labels_to_apply : list[str]
            list of label names to reformat
        """
        self.formatted_labels = {}
        for label_name in labels_to_apply:
            label_sorted = self.labels[label_name].reset_index(drop=True).sort_values(INDEX)
            label_merge_indicator = label_sorted.merge(self.samdata[INDEX], how="left", on=INDEX, indicator=True)._merge

            # left_only means that the datapoint is present in the label but not samdata
            if (label_merge_indicator == "left_only").any():
                warnings.warn(
                    f"Label {label_name} contains labels for datapoints that are not in samdata."
                    " Those labels will be ignored."
                )

            self.formatted_labels[label_name] = set(zip(*[label_sorted[col] for col in INDEX]))

    def apply_labels(self, labels_to_apply: list[str] = None) -> pd.DataFrame:
        """
        Apply labels to samdata to get a clean version of samdata

        Parameters
        ----------
        labels_to_apply : list[str]
            list of label names to reformat

        Returns
        -------
        pd.DataFrame
            The clean version of samdata
        """
        if not self.labels:
            warnings.warn("Trying to apply labels but no labels were provided. Returning raw data.")
            return self.samdata.copy()

        labels_to_apply = self.labels if labels_to_apply is None else labels_to_apply

        for label_name in labels_to_apply:
            if label_name not in self.labels:
                warnings.warn(
                    f"Label {label_name} was passed in list of labels_to_apply, but it was not "
                    "provided inside InputData object"
                )

        labels_to_apply = list(set(self.labels).intersection(set(labels_to_apply)))

        self._format_labels(labels_to_apply)

        combined_labels = set().union(*self.formatted_labels.values())
        clean_samdata = self.samdata.copy()
        clean_samdata.loc[pd.MultiIndex.from_frame(self.samdata[INDEX]).isin(combined_labels), "VALUE"] = np.nan
        logging.info(f"Labels {labels_to_apply} applied")
        return clean_samdata
