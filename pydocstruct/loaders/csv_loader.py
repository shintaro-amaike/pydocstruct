"""pydocstruct/loaders/csv_loader.py"""
from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import pandas as pd
except ImportError:
    pd = None

from pydocstruct.core.document import Document
from pydocstruct.core.loader import BaseLoader


class CsvLoader(BaseLoader):
    """Loader for CSV files"""

    def __init__(
        self,
        file_path: str | Path,
        encoding: str = "utf-8",
        output_format: str = "row",  # "row" or "markdown"
        **kwargs: Any,
    ) -> None:
        super().__init__(file_path, encoding, **kwargs)
        self.output_format = output_format
        
        if pd is None:
            raise ImportError(
                "pandasがインストールされていません。"
                "pip install pandas でインストールしてください。"
            )

    def load(self) -> list[Document]:
        """Load CSV file"""
        df = pd.read_csv(self.file_path, encoding=self.encoding)
        base_metadata = self._create_base_metadata()
        
        if self.output_format == "markdown":
            return [
                Document(
                    content=df.to_markdown(index=False),
                    metadata=base_metadata,
                    source=str(self.file_path),
                )
            ]
            
        documents = []
        
        # Create Document for each row
        for index, row in df.iterrows():
            # Convert row content to text (key: value format)
            content = "\n".join([f"{col}: {val}" for col, val in row.items()])
            
            metadata = base_metadata.copy()
            metadata["row_index"] = index
            
            documents.append(
                Document(
                    content=content,
                    metadata=metadata,
                    source=str(self.file_path),
                )
            )
            
        return documents

