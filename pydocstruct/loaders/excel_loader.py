"""pydocstruct/loaders/excel_loader.py"""
from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import pandas as pd
except ImportError:
    pd = None

from pydocstruct.core.document import Document
from pydocstruct.core.loader import BaseLoader


class ExcelLoader(BaseLoader):
    """Excelファイルを読み込むローダー"""

    def __init__(
        self,
        file_path: str | Path,
        output_format: str = "row",  # "row" or "markdown"
        **kwargs: Any,
    ) -> None:
        super().__init__(file_path, **kwargs)
        self.output_format = output_format
        
        if pd is None:
            raise ImportError(
                "pandasがインストールされていません。"
                "pip install pandas openpyxl でインストールしてください。"
            )

    def load(self) -> list[Document]:
        """Excelファイルを読み込む
        
        各シートの各行をDocumentとして読み込みます。
        output_format="markdown"の場合は、各シートを1つのMarkdownテーブルとして読み込みます。
        """
        # 全シートを読み込む
        sheets = pd.read_excel(self.file_path, sheet_name=None)
        
        documents = []
        base_metadata = self._create_base_metadata()
        
        for sheet_name, df in sheets.items():
            if self.output_format == "markdown":
                metadata = base_metadata.copy()
                metadata["sheet_name"] = sheet_name
                documents.append(
                    Document(
                        content=df.to_markdown(index=False),
                        metadata=metadata,
                        source=str(self.file_path),
                    )
                )
                continue

            # 行ごとにDocumentを作成
            for index, row in df.iterrows():
                # 行の内容をテキスト化
                content = "\n".join([f"{col}: {val}" for col, val in row.items()])
                
                metadata = base_metadata.copy()
                metadata["sheet_name"] = sheet_name
                metadata["row_index"] = index
                
                documents.append(
                    Document(
                        content=content,
                        metadata=metadata,
                        source=str(self.file_path),
                    )
                )
            
        return documents

