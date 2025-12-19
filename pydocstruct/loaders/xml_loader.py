"""pydocstruct/loaders/xml_loader.py"""
from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

from pydocstruct.core.document import Document
from pydocstruct.core.loader import BaseLoader


class XmlLoader(BaseLoader):
    """XMLファイルを読み込むローダー"""

    def __init__(
        self,
        file_path: str | Path,
        encoding: str = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().__init__(file_path, encoding, **kwargs)
        
        if BeautifulSoup is None:
            raise ImportError(
                "beautifulsoup4がインストールされていません。"
                "pip install beautifulsoup4 lxml でインストールしてください。"
            )

    def load(self) -> list[Document]:
        """XMLファイルを読み込む
        
        タグを除去してテキストのみを抽出します。
        """
        with open(self.file_path, "r", encoding=self.encoding) as file:
            soup = BeautifulSoup(file, "xml")

        # テキストのみ抽出
        text = soup.get_text(separator="\n", strip=True)

        metadata = self._create_base_metadata()

        return [
            Document(
                content=text,
                metadata=metadata,
                source=str(self.file_path),
            )
        ]

