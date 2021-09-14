"""
Module implementing DataframeSummarizer class.

DataframeSummarizer collects statistics for a given pandas.DataFrame
object and saves it to a file of given extension.
"""
import pandas as pd
from pandas.api.types import is_numeric_dtype


class DataframeSummarizer:
    statistics = ['type', 'min', 'max', 'mean', 'median', 'mode',
                  'nan_count', 'nan_ratio', 'variance', 'std_deviation',
                  'iqr', 'num_distinct']
    output_mapping = {
        'csv': 'to_csv',
        'markdown': 'to_markdown',
        'html': 'to_html',
        'xlsx': 'to_excel',
    }

    def __init__(self, dataframe: pd.DataFrame):
        self.data = dataframe.copy()
        self.statistics = pd.DataFrame(columns=DataframeSummarizer.statistics)
        self.statistics.index.name = 'name'

    @classmethod
    def load_from_csv(cls, filepath: str):
        """Create DataframeSummarizer from file with comma-separated values."""
        dataframe = pd.read_csv(filepath)
        return cls(dataframe)

    def get_general_statistics(self, column: str):
        """Get statistics for data columns of any dtypes."""
        self.statistics.at[column, 'type'] = str(self.data[column].dtype)
        self.statistics.at[column, 'nan_count'] = len(self.data[self.data[column].isna()])
        self.statistics.at[column, 'nan_ratio'] = self.statistics.at[column, 'nan_count'] / len(self.data)
        self.statistics.at[column, 'num_distinct'] = self.data[column].nunique(dropna=False)

    def get_numerical_statistics(self, column: str):
        """Get statistics for data columns of numerical dtypes."""
        self.statistics.at[column, 'min'] = self.data[column].min()
        self.statistics.at[column, 'max'] = self.data[column].max()
        self.statistics.at[column, 'mean'] = self.data[column].mean()
        self.statistics.at[column, 'median'] = self.data[column].median()
        self.statistics.at[column, 'mode'] = self.data[column].mode().values[0]
        self.statistics.at[column, 'variance'] = self.data[column].var()
        self.statistics.at[column, 'std_deviation'] = self.data[column].std()
        self.statistics.at[column, 'iqr'] = self.data[column].quantile(0.75) - self.data[column].quantile(0.25)

    def save(self, save_path: str, output_type: str) -> None:
        """Save statistics table to provided save path with given output type."""
        try:
            save_method = getattr(self.statistics, self.output_mapping.get(output_type))
            save_method(save_path, index=True)
        except TypeError as exc:
            raise NotImplementedError(
                f'Output for type {output_type} is not implemented. '
                f'Please use one of {list(DataframeSummarizer.output_mapping)}.'
            ) from exc

    def get_statistics(self, save_path: str = None, output_type: str = None) -> None:
        """Main method to get all statistics for the data and save them into a file."""
        for column in self.data.columns:
            self.get_general_statistics(column)
            if is_numeric_dtype(self.data[column]):
                self.get_numerical_statistics(column)

        if save_path is not None:
            self.save(save_path, output_type)
