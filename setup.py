from setuptools import setup, find_packages

setup(
    name='rexia_ai',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "langchain_community==0.2.5",
        "langchain_google_community==1.0.5",
        "langchain_openai==0.1.9",
        "llmware==0.3.0",
        "moviepy==1.0.3",
        "openai==1.35.3",
        "opencv_python==4.10.0.82",
        "opencv_python_headless==4.10.0.82",
        "pydantic==2.7.4",
        "pytube==15.0.0",
        "Requests==2.32.3",
        "setuptools==69.5.1",
        "transformers==4.41.2"
    ],
)