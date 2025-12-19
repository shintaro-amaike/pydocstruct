# pydocstruct

[![PyPI version](https://badge.fury.io/py/pydocstruct.svg)](https://badge.fury.io/py/pydocstruct)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**pydocstruct** is a Python library designed to convert various file formats (PDF, DOCX, Excel, Markdown, CSV, JSON, etc.) into structured data suitable for RAG (Retrieval-Augmented Generation) systems and vector databases.

It provides features optimized for RAG, such as token-based chunking, Markdown table conversion, and PII redaction.

## Features

- 🌟 **Unified Interface**: Support for all formats via a single `pydocstruct.load()` function.
- 📄 **Diverse Formats**: PDF, Excel (XLSX), Word (DOCX), Markdown, Text, HTML, XML, JSON, CSV.
- 🤖 **RAG Optimization**:
    - **Advanced Chunking**: Supports Recursive Character Splitter and Token-based (`TokenChunker`) splitting.
    - **Enhanced Representation**: Extracts CSV/Excel as Markdown tables; preserves HTML structure.
    - **Advanced PDF Handling**: Layout analysis and OCR support for scanned PDFs.
- 🛡️ **Data Cleaning**: 
    - **PII Redaction**: Automatically masks personal information like emails and phone numbers.
    - **Noise Reduction**: Removes HTML headers, footers, advertisements, etc.

## Installation

```bash
pip install pydocstruct
```

### Installing Dependencies

To use all features (OCR, Excel, table conversion, etc.), we recommend installing the additional dependencies:

```bash
pip install "pydocstruct[all]"
```
*(Note: If installing manually: `pandas`, `openpyxl`, `tabulate`, `pypdf`, `python-docx`, `beautifulsoup4`, `markdownify`, `tiktoken`, `pdf2image`, `pytesseract`)*

⚠️ **Requirements for OCR**:
To use the OCR feature (`use_ocr=True`), you must separately install the following system tools and ensure they are in your PATH:
- **Tesseract-OCR**
- **Poppler** (for `pdf2image`)

## Quick Start

### Basic Usage

```python
from pydocstruct import load

# Load a PDF file
documents = load("paper.pdf")

for doc in documents:
    print(f"File: {doc.source}")
    print(f"Page: {doc.page_number}")
    print(f"Content: {doc.content[:100]}...")
```

The `load` function returns a `list[Document]`.

## Supported Formats & Details

| Format | Extension | Description | Key Options |
|------------|-------|------|----------------|
| **PDF** | `.pdf` | Documents per page. Supports OCR/Layout analysis. | `use_ocr=True`, `use_layout=True` |
| **Excel** | `.xlsx` | Load row-by-row or as Markdown table. | `output_format="markdown"` |
| **CSV** | `.csv` | Load row-by-row or as Markdown table. | `output_format="markdown"` |
| **Word** | `.docx` | Loads entire document. | - |
| **HTML** | `.html` | Extracts text or preserves structure as Markdown. | `preserve_structure=True` |
| **Markdown** | `.md` | Supports splitting by headers. | `split_by_headers=True` |
| **Text** | `.txt` | Loads as UTF-8 text. | - |

## Advanced Usage

### 1. Markdown Table Conversion (CSV/Excel)

For RAG, Markdown tables are often better understood by LLMs than flattened key-value pairs.

```python
# Load Excel as a Markdown table
docs = load("data.xlsx", output_format="markdown")
print(docs[0].content)
# Output Example:
# | Product | Price |
# |:--------|------:|
# | Apple   |   100 |
```

### 2. PDF OCR and Layout Analysis

Handles scanned PDFs or complex multi-column layouts.

```python
# Extract while preserving layout (better for multi-column)
docs = load("paper.pdf", use_layout=True)

# Run OCR on pages with no text (Requires Tesseract/Poppler)
docs = load("scanned.pdf", use_ocr=True, ocr_lang="eng")
```

### 3. Advanced Chunking

Split text intelligently to fit LLM context windows.

```python
from pydocstruct.core.chunker import RecursiveCharacterChunker, TokenChunker

# Recursive splitting (Try Paragraph -> Sentence -> Word)
recursive_chunker = RecursiveCharacterChunker(chunk_size=1000, chunk_overlap=200)
chunked_docs = recursive_chunker.split_documents(documents)

# Token-based splitting (using tiktoken, optimized for GPT models)
token_chunker = TokenChunker(chunk_size=500, model_name="gpt-4")
chunked_docs = token_chunker.split_documents(documents)
```

### 4. Data Cleaning (Processors)

Remove PII or HTML noise.

```python
from pydocstruct.processors import PiiRedactor, HtmlNoiseCleaner

text = "Contact: 090-1234-5678, email@example.com"

# Redact PII
cleaned_text = PiiRedactor.redact(text)
print(cleaned_text) 
# -> "Contact: [REDACTED], [REDACTED]"

# Remove HTML noise (headers, footers, ads)
clean_html_text = HtmlNoiseCleaner.clean(html_content)
```

## License

MIT License