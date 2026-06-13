"""tests/test_document.py"""
from pydocstruct.core.document import Document


def test_document_creation():
    """Documentの基本的な作成テスト"""
    # Documentを作成
    doc = Document(
        content="テストコンテンツ",
        metadata={"author": "Test Author"},
        source="test.txt",
    )
    
    # 検証
    assert doc.content == "テストコンテンツ"
    assert doc.metadata["author"] == "Test Author"
    assert doc.source == "test.txt"
    assert "created_at" in doc.metadata


def test_document_to_dict():
    """Documentの辞書変換テスト"""
    # Documentを作成
    doc = Document(
        content="テストコンテンツ",
        doc_id="doc_001",
    )
    
    # 辞書に変換
    doc_dict = doc.to_dict()
    
    # 検証
    assert isinstance(doc_dict, dict)
    assert doc_dict["content"] == "テストコンテンツ"
    assert doc_dict["doc_id"] == "doc_001"


def test_document_from_dict():
    """辞書からのDocument生成テスト"""
    data = {
        "content": "テストコンテンツ",
        "metadata": {"key": "value"},
        "doc_id": "doc_002",
    }
    doc = Document.from_dict(data)
    assert doc.content == "テストコンテンツ"
    assert doc.metadata["key"] == "value"
    assert doc.doc_id == "doc_002"


def test_document_roundtrip():
    """to_dict → from_dict が元のDocumentと等価であること"""
    original = Document(
        content="テストコンテンツ",
        metadata={"author": "taro"},
        doc_id="doc_003",
        source="file.txt",
        page_number=2,
        chunk_index=1,
    )
    restored = Document.from_dict(original.to_dict())
    assert restored.content == original.content
    assert restored.doc_id == original.doc_id
    assert restored.source == original.source
    assert restored.page_number == original.page_number
    assert restored.chunk_index == original.chunk_index
    assert restored.metadata["author"] == original.metadata["author"]


def test_document_to_dict_contains_all_fields():
    """to_dict がすべてのフィールドを含むこと"""
    doc = Document(
        content="内容",
        doc_id="doc_004",
        source="path/to/file.txt",
        page_number=3,
        chunk_index=0,
    )
    d = doc.to_dict()
    assert d["content"] == "内容"
    assert d["doc_id"] == "doc_004"
    assert d["source"] == "path/to/file.txt"
    assert d["page_number"] == 3
    assert d["chunk_index"] == 0
    assert "metadata" in d


def test_document_optional_fields_default_to_none():
    """オプションフィールドのデフォルト値がNoneであること"""
    doc = Document(content="content only")
    assert doc.doc_id is None
    assert doc.source is None
    assert doc.page_number is None
    assert doc.chunk_index is None
