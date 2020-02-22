from setuptools import setup

setup(
    name='task',
    version='0.1',
    py_modules=['tasks'],
    install_requires=[
        'Click==7',
        'fpdf==1.7.2',
    ],
    entry_points='''
        [console_scripts]
        task=cli_client.client:task
    ''',
)
