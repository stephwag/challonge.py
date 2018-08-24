from setuptools import setup
import os

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setup(
    name='challonge.py',
    version='0.0.1',
    description='Python bindings for the Challonge API',
    author='stephwag',
    author_email='stephwag@stephwag.com',
    packages=['challonge'],
    url='https://github.com/stephwag/challonge.py',
    license='MIT',
    keywords='challonge api',
    include_package_data=True,
    install_requires=requirements
)
