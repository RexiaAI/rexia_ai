"""This module is used to install the package using the command "pip install -e ."""

from setuptools import setup, find_packages

setup(
    name="rexia_ai",
    version="0.0.1",
    packages=find_packages(include=["agencies", "agents", "handlers", "tasks"]),
)
