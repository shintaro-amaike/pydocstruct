"""pydocstruct/processors/text_cleaner.py"""
from __future__ import annotations

import re


class TextCleaner:
    """テキストクリーニングを行うクラス"""

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """空白文字を正規化（連続する空白を1つに、前後の空白を削除）"""
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def remove_urls(text: str, replacement: str = "") -> str:
        """URLを削除または置換"""
        return re.sub(r"https?://\S+|www\.\S+", replacement, text)

    @staticmethod
    def remove_emails(text: str, replacement: str = "") -> str:
        """メールアドレスを削除または置換"""
        return re.sub(r"\S+@\S+\.\S+", replacement, text)

    @staticmethod
    def clean(
        text: str,
        normalize_whitespace: bool = True,
        remove_urls: bool = False,
        remove_emails: bool = False,
    ) -> str:
        """テキストを一括クリーニング"""
        if normalize_whitespace:
            text = TextCleaner.normalize_whitespace(text)
        if remove_urls:
            text = TextCleaner.remove_urls(text)
        if remove_emails:
            text = TextCleaner.remove_emails(text)
        return text

