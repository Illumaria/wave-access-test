import urllib.request
from pathlib import Path

import pandas as pd


def load_iris_dataset() -> pd.DataFrame:
    """Load Iris dataset from URL and open it with Pandas."""
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

    filepath = Path('data/iris_data')
    filepath.parent.mkdir(exist_ok=True)

    # Download data file and load it with Pandas:
    urllib.request.urlretrieve(url, str(filepath))
    df = pd.read_csv(str(filepath), names=column_names)

    # Replace downloaded file with file containing column names:
    filepath.unlink()
    df.to_csv(filepath, index=False)

    return df
