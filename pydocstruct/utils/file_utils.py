"""pydocstruct/utils/file_utils.py"""
from __future__ import annotations

import mimetypes
from pathlib import Path


def get_file_extension(file_path: str | Path) -> str:
    """ファイルの拡張子を取得（小文字、ドットなし）"""
    return Path(file_path).suffix.lower().lstrip(".")


def get_mime_type(file_path: str | Path) -> str | None:
    """ファイルのMIMEタイプを取得"""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def is_supported_format(file_path: str | Path, supported_extensions: list[str]) -> bool:
    """サポートされているフォーマットか確認"""
    ext = get_file_extension(file_path)
    return ext in [e.lower() for e in supported_extensions]

