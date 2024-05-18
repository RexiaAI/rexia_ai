from setuptools import setup, find_packages

setup(
    name='rexia_ai',
    version='0.1.0',
    packages=find_packages(include=['agencies', 'agents', 'handlers', 'llms', 'tasks', 'tools', 'utilities']),
)