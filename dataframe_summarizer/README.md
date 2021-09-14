# DataframeSummarizer

## Prerequisites

* Python >= 3.8
* pip >= 21.0.1

## Installation

```bash
git clone https://github.com/Illumaria/wave-access-test.git
cd wave-access-test/dataframe_summarizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

For example, to save statistics for some dataframe `df` into `output.md` do:

```python
from dataframe_summarizer import DataframeSummarizer

summarizer = DataframeSummarizer(df)
summarizer.get_statistics(save_path='output.md', output_type='markdown')
```

### Run tests

```bash
pip install -r requirements_dev.txt
pytest . -v --cov=dataframe_summarizer
```

### Run linter

```bash
flake8 dataframe_summarizer --count --max-line-length=120 --statistics
```
