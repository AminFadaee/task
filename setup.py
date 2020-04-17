from setuptools import setup

setup(
    name='task',
    version='0.1',
    description='A simple cli to-do list.',
    url='https://github.com/aminFadaee/task',
    author='Amin Fadaee',
    py_modules=['tasks'],
    license='MIT',
    install_requires=[
        'click==7.1.1',
        'fpdf==1.7.2',
    ],
    entry_points='''
        [console_scripts]
        task=cli_client.client:task
    ''',
)
