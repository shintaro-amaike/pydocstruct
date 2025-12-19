"""pydocstruct/processors/metadata_extractor.py"""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any


class MetadataExtractor:
    """ファイルのメタデータを抽出するクラス"""

    @staticmethod
    def extract(file_path: str | Path) -> dict[str, Any]:
        """ファイルから基本メタデータを抽出"""
        path = Path(file_path)
        if not path.exists():
            return {}

        stat = path.stat()
        return {
            "file_name": path.name,
            "file_extension": path.suffix.lower(),
            "file_size": stat.st_size,
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "abs_path": str(path.absolute()),
        }

