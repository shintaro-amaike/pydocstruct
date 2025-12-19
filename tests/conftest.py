"""tests/conftest.py"""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def sample_files_dir(tmp_path: Path) -> Path:
    """テスト用サンプルファイルディレクトリを作成
    
    Args:
        tmp_path (Path): pytestの一時ディレクトリ
        
    Returns:
        Path: サンプルファイルディレクトリのパス
    """
    # サンプルディレクトリを作成
    samples_dir = tmp_path / "samples"
    samples_dir.mkdir()
    
    return samples_dir


@pytest.fixture
def sample_text_file(sample_files_dir: Path) -> Path:
    """テスト用テキストファイルを作成
    
    Args:
        sample_files_dir (Path): サンプルファイルディレクトリ
        
    Returns:
        Path: テキストファイルのパス
    """
    # テキストファイルを作成
    text_file = sample_files_dir / "sample.txt"
    text_file.write_text("これはテストファイルです。\n複数行のテキストを含みます。", encoding="utf-8")
    
    return text_file


@pytest.fixture
def sample_markdown_file(sample_files_dir: Path) -> Path:
    """テスト用Markdownファイルを作成
    
    Args:
        sample_files_dir (Path): サンプルファイルディレクトリ
        
    Returns:
        Path: Markdownファイルのパス
    """
    # Markdownコンテンツ
    content = """# メインタイトル

## セクション1
これは最初のセクションです。

## セクション2
これは2番目のセクションです。

### サブセクション2.1
詳細な内容がここに入ります。
"""
    
    # Markdownファイルを作成
    md_file = sample_files_dir / "sample.md"
    md_file.write_text(content, encoding="utf-8")
    
    return md_file