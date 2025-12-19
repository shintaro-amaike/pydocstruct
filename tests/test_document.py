"""tests/test_document.py"""
from __future__ import annotations

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
    # テストデータ
    data = {
        "content": "テストコンテンツ",
        "metadata": {"key": "value"},
        "doc_id": "doc_002",
    }
    
    # Documentを生成
    doc = Document.from_dict(data)
    
    # 検証
    assert doc.content == "テストコンテンツ"
    assert doc.metadata["key"] == "value"
    assert doc.doc_id == "doc_002"
