from setuptools import setup

setup(
    name='statbank',
    version='0.1',
    description='Statbank API client library',
    url='http://github.com/gisgroup/statbank-python',
    author='Gis Group ApS',
    author_email='valentin@gisgroup.dk, zacharias@gisgroup.dk',
    license='MIT',
    packages=['statbank'],
    install_requires=[
        'python-dateutil',
    ],
    test_suite='tests',
)
