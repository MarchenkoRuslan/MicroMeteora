from setuptools import setup, find_packages

setup(
    name="meteora",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=2.0.0",
        "aiohttp>=3.9.0",
        "httpx>=0.25.2",
    ],
) 