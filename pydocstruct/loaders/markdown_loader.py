"""pydocstruct/loaders/markdown_loader.py"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from pydocstruct.core.document import Document
from pydocstruct.core.loader import BaseLoader


class MarkdownLoader(BaseLoader):
    """Markdownファイルを読み込むローダー
    
    Markdownファイルをテキストとして読み込み、
    見出しレベルでの分割オプションを提供します。
    
    Attributes:
        split_by_headers (bool): 見出しで分割するか
    """
    
    def __init__(
        self,
        file_path: str | Path,
        encoding: str = "utf-8",
        split_by_headers: bool = False,
        **kwargs: Any,
    ) -> None:
        """MarkdownLoaderの初期化
        
        Args:
            file_path (str | Path): Markdownファイルのパス
            encoding (str, optional): エンコーディング. Defaults to "utf-8".
            split_by_headers (bool, optional): 見出しで分割. Defaults to False.
            **kwargs: 追加のメタデータ
        """
        super().__init__(file_path, encoding, **kwargs)
        self.split_by_headers = split_by_headers
    
    def load(self) -> list[Document]:
        """Markdownファイルを読み込む
        
        Returns:
            list[Document]: Documentリスト
        """
        # ファイルを読み込む
        with open(self.file_path, "r", encoding=self.encoding) as file:
            content = file.read()
        
        # 基本メタデータを作成
        metadata = self._create_base_metadata()
        
        # 見出しで分割する場合
        if self.split_by_headers:
            return self._split_by_headers(content, metadata)
        
        # 分割しない場合は単一のDocumentを返す
        document = Document(
            content=content,
            metadata=metadata,
            source=str(self.file_path),
        )
        
        return [document]
    
    def _split_by_headers(
        self,
        content: str,
        base_metadata: dict[str, Any],
    ) -> list[Document]:
        """見出しでMarkdownを分割
        
        Args:
            content (str): Markdownコンテンツ
            base_metadata (dict[str, Any]): 基本メタデータ
            
        Returns:
            list[Document]: 分割されたDocumentリスト
        """
        import re
        
        # 見出しパターン（# で始まる行）
        header_pattern = r'^(#{1,6})\s+(.+)$'
        
        # 結果格納用リスト
        documents = []
        current_section = []
        current_header = None
        current_level = 0
        
        # 行ごとに処理
        for line in content.split('\n'):
            # 見出し行かチェック
            match = re.match(header_pattern, line)
            
            if match:
                # 前のセクションを保存
                if current_section:
                    section_content = '\n'.join(current_section).strip()
                    if section_content:
                        # メタデータを作成
                        section_metadata = base_metadata.copy()
                        section_metadata["header"] = current_header
                        section_metadata["header_level"] = current_level
                        
                        # Documentを作成
                        doc = Document(
                            content=section_content,
                            metadata=section_metadata,
                            source=str(self.file_path),
                        )
                        documents.append(doc)
                
                # 新しいセクションを開始
                current_level = len(match.group(1))
                current_header = match.group(2)
                current_section = [line]
            else:
                # 現在のセクションに行を追加
                current_section.append(line)
        
        # 最後のセクションを処理
        if current_section:
            section_content = '\n'.join(current_section).strip()
            if section_content:
                section_metadata = base_metadata.copy()
                section_metadata["header"] = current_header
                section_metadata["header_level"] = current_level
                
                doc = Document(
                    content=section_content,
                    metadata=section_metadata,
                    source=str(self.file_path),
                )
                documents.append(doc)
        
        return documents
