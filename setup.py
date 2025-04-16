from setuptools import setup, find_packages

setup(
    name="flicka-sports",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "crawl4ai>=0.1.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "python-dotenv>=1.0.0",
        "aiohttp>=3.8.0",
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "pytest-cov>=4.0.0",
        "pytest-mock>=3.10.0",
        "black>=23.0.0",
        "flake8>=6.0.0",
        "pydantic>=2.0.0",
    ],
) 