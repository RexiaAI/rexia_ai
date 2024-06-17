# setup.py
from setuptools import setup, find_packages

setup(
    name='rexia_ai',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'rexia_ai': ['thought_buffer/buffer/*']},
    install_requires=[
        "langchain_community==0.2.5",
        "langchain_google_community==1.0.5",
        "langchain_openai==0.1.8",
        "llmware==0.3.0",
        "moviepy==1.0.3",
        "openai==1.34.0",
        "opencv_python==4.10.0.82",
        "opencv_python_headless==4.10.0.82",
        "pydantic==2.7.4",
        "pytube==15.0.0",
        "qdrant_client==1.9.1",
        "Requests==2.32.3",
        "setuptools==69.5.1",
        "transformers==4.41.2"
    ],
)