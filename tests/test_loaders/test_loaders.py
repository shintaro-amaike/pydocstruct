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
    # JSONが整形されてcontentに含まれること
    assert '"key"' in docs[0].content
    assert '"value"' in docs[0].content
    assert "list" in docs[0].content

def test_csv_loader(sample_csv_file):
    docs = load(sample_csv_file)
    # pandasはヘッダー行をカラム名として読み込むため、データ行は1行 → 1 Document
    assert len(docs) == 1
    assert "col1: val1" in docs[0].content
    assert "col2: val2" in docs[0].content

def test_xml_loader(sample_xml_file):
    docs = load(sample_xml_file)
    assert len(docs) == 1
    # タグが除去されてテキストのみ残ること
    assert "text content" in docs[0].content
    assert "<child>" not in docs[0].content
    assert "<root>" not in docs[0].content

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


def test_markdown_loader_no_split(sample_markdown_file):
    """split_by_headers=False（デフォルト）では1つのDocumentを返すこと"""
    docs = load(sample_markdown_file)
    assert len(docs) == 1
    assert "メインタイトル" in docs[0].content
    assert "セクション1" in docs[0].content
    assert "セクション2" in docs[0].content


def test_markdown_loader_split_by_headers(sample_markdown_file):
    """split_by_headers=True では見出しごとにDocumentが分割されること"""
    from pydocstruct.loaders.markdown_loader import MarkdownLoader
    loader = MarkdownLoader(sample_markdown_file, split_by_headers=True)
    docs = loader.load()
    # サンプルには # が1つ、## が2つ、### が1つの計4見出し
    assert len(docs) >= 3
    headers = [d.metadata.get("header") for d in docs]
    assert "メインタイトル" in headers
    assert "セクション1" in headers
    assert "セクション2" in headers


def test_markdown_loader_split_sets_header_metadata(sample_markdown_file):
    """分割されたDocumentのmetadataにheaderとheader_levelが含まれること"""
    from pydocstruct.loaders.markdown_loader import MarkdownLoader
    loader = MarkdownLoader(sample_markdown_file, split_by_headers=True)
    docs = loader.load()
    for doc in docs:
        assert "header" in doc.metadata
        assert "header_level" in doc.metadata
        assert isinstance(doc.metadata["header_level"], int)


@pytest.fixture
def sample_json_list_file(sample_files_dir):
    """JSONがリスト形式のファイル"""
    path = sample_files_dir / "list.json"
    data = [{"name": "Alice"}, {"name": "Bob"}]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return path


def test_json_loader_list_creates_multiple_docs(sample_json_list_file):
    """JSONがリストの場合、要素ごとにDocumentが生成されること"""
    docs = load(sample_json_list_file)
    assert len(docs) == 2
    assert "Alice" in docs[0].content
    assert "Bob" in docs[1].content

