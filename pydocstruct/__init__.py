"""pydocstruct"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from pydocstruct.__version__ import __version__
from pydocstruct.core import (
    BaseChunker,
    BaseLoader,
    Document,
    RecursiveCharacterChunker,
    TextChunker,
    TokenChunker,
)
from pydocstruct.loaders import (
    CsvLoader,
    DocxLoader,
    ExcelLoader,
    HtmlLoader,
    JsonLoader,
    MarkdownLoader,
    PDFLoader,
    TextLoader,
    XmlLoader,
)
from pydocstruct.processors import (
    HtmlNoiseCleaner,
    MetadataExtractor,
    PiiRedactor,
    TextCleaner,
)
from pydocstruct.utils import get_file_extension, get_mime_type, is_supported_format

__all__ = [
    "load",
    "Document",
    "__version__",
    # Core
    "BaseChunker",
    "TextChunker",
    "RecursiveCharacterChunker",
    "TokenChunker",
    "BaseLoader",
    # Loaders
    "CsvLoader",
    "DocxLoader",
    "ExcelLoader",
    "HtmlLoader",
    "JsonLoader",
    "MarkdownLoader",
    "PDFLoader",
    "TextLoader",
    "XmlLoader",
    # Processors
    "TextCleaner",
    "MetadataExtractor",
    "PiiRedactor",
    "HtmlNoiseCleaner",
    # Utils
    "get_file_extension",
    "get_mime_type",
    "is_supported_format",
]


def load(file_path: str | Path, **kwargs: Any) -> list[Document]:
    """Unified function to load file and convert to structured data

    Automatically selects the appropriate loader based on file extension.

    Args:
        file_path (str | Path): Path to the file to load
        **kwargs: Additional options passed to specific loaders

    Returns:
        list[Document]: List of loaded documents

    Raises:
        ValueError: If file format is not supported
        FileNotFoundError: If file does not exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    ext = get_file_extension(path)

    loader_map = {
        "pdf": PDFLoader,
        "docx": DocxLoader,
        "md": MarkdownLoader,
        "markdown": MarkdownLoader,
        "txt": TextLoader,
        "text": TextLoader,
        "json": JsonLoader,
        "csv": CsvLoader,
        "xls": ExcelLoader,
        "xlsx": ExcelLoader,
        "xml": XmlLoader,
        "html": HtmlLoader,
        "htm": HtmlLoader,
    }

    loader_cls = loader_map.get(ext)

    if loader_cls is None:
        raise ValueError(f"Unsupported file format: {ext}")

    loader = loader_cls(path, **kwargs)
    return loader.load()
