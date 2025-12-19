"""pydocstruct/loaders/__init__.py"""
from pydocstruct.loaders.csv_loader import CsvLoader
from pydocstruct.loaders.docx_loader import DocxLoader
from pydocstruct.loaders.excel_loader import ExcelLoader
from pydocstruct.loaders.html_loader import HtmlLoader
from pydocstruct.loaders.json_loader import JsonLoader
from pydocstruct.loaders.markdown_loader import MarkdownLoader
from pydocstruct.loaders.pdf_loader import PDFLoader
from pydocstruct.loaders.text_loader import TextLoader
from pydocstruct.loaders.xml_loader import XmlLoader

__all__ = [
    "CsvLoader",
    "DocxLoader",
    "ExcelLoader",
    "HtmlLoader",
    "JsonLoader",
    "MarkdownLoader",
    "PDFLoader",
    "TextLoader",
    "XmlLoader",
]

