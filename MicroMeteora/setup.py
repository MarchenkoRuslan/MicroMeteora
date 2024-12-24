from setuptools import setup, find_packages

setup(
    name="meteora-service",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
        "redis>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "meteora=src.cli:cli",
        ],
    },
) 