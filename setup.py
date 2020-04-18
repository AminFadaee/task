import pathlib

from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='cli-task',
    version='0.1',
    description='A simple cli to-do list.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/aminFadaee/task',
    author='Amin Fadaee',
    py_modules=['tasks'],
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("tests",)) + ['assets'],
    include_package_data=True,
    package_data={'assets': ['assets/fonts/onuava__.ttf']},
    install_requires=[
        'click==7.1.1',
        'fpdf==1.7.2',
    ],
    entry_points='''
        [console_scripts]
        task=cli_client.client:task
    ''',
)
