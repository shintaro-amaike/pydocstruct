"""pydocstruct/loaders/text_loader.py"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from pydocstruct.core.document import Document
from pydocstruct.core.loader import BaseLoader


class TextLoader(BaseLoader):
    """テキストファイルを読み込むローダー"""

    def load(self) -> list[Document]:
        """テキストファイルを読み込む"""
        with open(self.file_path, "r", encoding=self.encoding) as file:
            content = file.read()

        metadata = self._create_base_metadata()

        return [
            Document(
                content=content,
                metadata=metadata,
                source=str(self.file_path),
            )
        ]

