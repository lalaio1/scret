from setuptools import setup, find_packages

setup(
    name='scret',
    version='0.1.0',
    description='Library for interacting with scret.me API',
    packages=find_packages(),
    install_requires=[
        "requests",
        "aiohttp",
    ],
)
