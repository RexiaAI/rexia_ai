from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rexia_ai',
    version='0.3.5.2',
    author='Robyn Le Sueur',
    author_email='robyn.lesueur@googlemail.com',
    description='ReXia.AI: An advanced AI framework for agentic processes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RexiaAI/rexia_ai/tree/master',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "docker>=7.1.0",
        "gradio==4.39.0",
        "json5==0.9.25",
        "json_repair==0.25.3",
        "langchain_community>=0.2.9,<0.3.0",
        "langchain_google_community>=1.0.7,<1.1.0",
        "langchain_openai==0.1.17",
        "llmware==0.3.0",
        "moviepy==1.0.3",
        "openai==1.37.0",
        "opencv_python==4.10.0.82",
        "opencv_python_headless==4.10.0.82",
        "pydantic==2.8.2",
        "pytube==15.0.0",
        "Requests==2.32.3",
        "setuptools==69.5.1",
        "tenacity>=8.3.0,<9.0.0",  # Loosened version constraint
        "transformers==4.41.2"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)