"""pydocstruct/loaders/json_loader.py"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydocstruct.core.document import Document
from pydocstruct.core.loader import BaseLoader


class JsonLoader(BaseLoader):
    """JSONファイルを読み込むローダー"""

    def load(self) -> list[Document]:
        """JSONファイルを読み込む
        
        JSONがリストの場合は複数のDocumentを生成し、
        辞書の場合は単一のDocumentを生成します。
        コンテンツとして使用するキーを指定することも可能です（未実装）。
        現在はJSON全体を文字列化してcontentとします。
        """
        with open(self.file_path, "r", encoding=self.encoding) as file:
            data = json.load(file)

        documents = []
        base_metadata = self._create_base_metadata()

        if isinstance(data, list):
            for i, item in enumerate(data):
                # 文字列以外の場合はJSON文字列に変換
                content = item if isinstance(item, str) else json.dumps(item, ensure_ascii=False)
                
                metadata = base_metadata.copy()
                metadata["index"] = i
                
                documents.append(
                    Document(
                        content=content,
                        metadata=metadata,
                        source=str(self.file_path),
                    )
                )
        else:
            # 単一のオブジェクト
            content = json.dumps(data, ensure_ascii=False, indent=2)
            documents.append(
                Document(
                    content=content,
                    metadata=base_metadata,
                    source=str(self.file_path),
                )
            )

        return documents

