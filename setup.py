# setup.py
from setuptools import setup, find_packages

setup(
    name='rexia_ai',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'rexia_ai': ['thought_buffer/buffer/*']},
    install_requires=[
        "langchain_community==0.2.4",
        "langchain_google_community==1.0.5",
        "langchain_openai==0.1.8",
        "openai==1.33.0",
        "pydantic==2.7.3",
        "qdrant_client==1.9.1",
        "Requests==2.32.3",
        "setuptools==69.5.1"
    ],
)