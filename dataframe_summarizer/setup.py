from setuptools import find_packages, setup

setup(
    name='dataframe_summarizer',
    # packages=find_packages(),
    packages=['dataframe_summarizer'],
    version='0.1.0',
    description='DataframeSummarizer',
    author='Dmitry Astankov',
    install_requires=[
        'openpyxl==3.0.8',
        'pandas==1.3.3',
        'tabulate==0.8.9',
    ],
    license='MIT',
)
