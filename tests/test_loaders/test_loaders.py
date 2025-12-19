"""tests/test_loaders/test_loaders.py"""
import pytest
import json
import csv
from pathlib import Path
from pydocstruct import load

@pytest.fixture
def sample_json_file(sample_files_dir):
    path = sample_files_dir / "test.json"
    data = {"key": "value", "list": [1, 2, 3]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return path

@pytest.fixture
def sample_csv_file(sample_files_dir):
    path = sample_files_dir / "test.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["col1", "col2"])
        writer.writerow(["val1", "val2"])
    return path

@pytest.fixture
def sample_xml_file(sample_files_dir):
    path = sample_files_dir / "test.xml"
    content = "<root><child>text content</child></root>"
    path.write_text(content, encoding="utf-8")
    return path

@pytest.fixture
def sample_html_file(sample_files_dir):
    path = sample_files_dir / "test.html"
    content = "<html><head><title>Test</title></head><body><p>Hello World</p><script>console.log('skip');</script></body></html>"
    path.write_text(content, encoding="utf-8")
    return path

@pytest.fixture
def sample_docx_file(sample_files_dir):
    try:
        import docx
    except ImportError:
        return None
        
    doc = docx.Document()
    doc.add_paragraph("Hello Docx")
    path = sample_files_dir / "test.docx"
    doc.save(path)
    return path

def test_text_loader(sample_text_file):
    docs = load(sample_text_file)
    assert len(docs) == 1
    assert "テストファイル" in docs[0].content

def test_json_loader(sample_json_file):
    docs = load(sample_json_file)
    assert len(docs) == 1
    assert "value" in docs[0].content

def test_csv_loader(sample_csv_file):
    docs = load(sample_csv_file)
    # 2 rows (1 header, 1 data? or pandas read_csv reads header)
    # CsvLoader implementation creates one doc per row.
    # CSV content:
    # col1,col2
    # val1,val2
    # DataFrame will have 1 row.
    assert len(docs) == 1
    assert "col1: val1" in docs[0].content
    assert "col2: val2" in docs[0].content

def test_xml_loader(sample_xml_file):
    docs = load(sample_xml_file)
    assert len(docs) == 1
    assert "text content" in docs[0].content

def test_html_loader(sample_html_file):
    docs = load(sample_html_file)
    assert len(docs) == 1
    assert "Hello World" in docs[0].content
    assert "console.log" not in docs[0].content
    assert docs[0].metadata.get("title") == "Test"

def test_docx_loader(sample_docx_file):
    if sample_docx_file is None:
        pytest.skip("python-docx not installed")
    
    docs = load(sample_docx_file)
    assert len(docs) == 1
    assert "Hello Docx" in docs[0].content

