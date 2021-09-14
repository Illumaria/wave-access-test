import os

import pandas as pd
import pytest

from dataframe_summarizer.dataframe_summarizer import DataframeSummarizer
from dataframe_summarizer.utils import load_iris_dataset


IRIS_DATASET_PATH = 'data/iris_data'
OUTPUT_PATH = 'data/output'


def test_can_load_iris_dataset():
    df = load_iris_dataset()
    expected_df_shape = (150, 5)
    assert df is not None
    assert pd.DataFrame == type(df)
    assert expected_df_shape == df.shape


@pytest.fixture()
def iris_dataset():
    df = load_iris_dataset()
    return df


def test_can_load_dataframe_summarizer_from_dataframe(iris_dataset):
    summarizer = DataframeSummarizer(iris_dataset)
    assert summarizer is not None
    assert summarizer.data is not None
    assert summarizer.data.shape == iris_dataset.shape


def test_can_load_dataframe_summarizer_from_file():
    summarizer = DataframeSummarizer.load_from_csv(IRIS_DATASET_PATH)
    expected_df_shape = (150, 5)
    assert summarizer is not None
    assert summarizer.data is not None
    assert expected_df_shape == summarizer.data.shape


@pytest.fixture()
def summarizer(iris_dataset):
    summarizer = DataframeSummarizer(iris_dataset)
    return summarizer


def test_can_get_statistics(summarizer):
    summarizer.get_statistics()
    statistics = summarizer.statistics
    expected_shape = (5, 12)
    assert statistics is not None
    assert pd.DataFrame == type(statistics)
    assert expected_shape == statistics.shape


@pytest.mark.parametrize(
    'output_type',
    [
        pytest.param('csv', id='csv'),
        pytest.param('markdown', id='markdown'),
        pytest.param('html', id='html'),
        pytest.param('xlsx', id='xlsx'),
    ],
)
def test_can_save_file(summarizer, output_type):
    save_path = OUTPUT_PATH + '.' + output_type
    summarizer.get_statistics(save_path, output_type)
    assert os.path.exists(save_path)


def test_save_throws_exception_on_wrong_format(summarizer):
    summarizer.get_statistics()
    output_type = 'abc'
    save_path = OUTPUT_PATH + '.' + output_type
    with pytest.raises(NotImplementedError):
        summarizer.save(save_path, output_type)
    assert not os.path.exists(save_path)
