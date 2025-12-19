"""setup.py"""
from __future__ import annotations

from pathlib import Path

from setuptools import find_packages, setup

# README.mdを読み込む
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

# バージョン情報を読み込む
version_file = Path(__file__).parent / "pydocstruct" / "__version__.py"
version_info = {}
exec(version_file.read_text(), version_info)

setup(
    name="pydocstruct",
    version=version_info["__version__"],
    author="Shintaro Amaike",
    author_email="shintaro.amaike@gmail.com",
    description="Document structuring library for RAG and vector databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shintaro-amaike/pydocstruct",
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pypdf>=3.0.0",
        "python-docx>=1.0.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "markdown>=3.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "isort>=5.12.0",
        ],
        "all": [
            "openpyxl>=3.1.0",
            "pandas>=2.0.0",
            "tabulate>=0.9.0",
            "markdownify>=0.11.0",
            "tiktoken>=0.5.0",
            "pdf2image>=1.16.0",
            "pytesseract>=0.3.10",
        ],
    },
)