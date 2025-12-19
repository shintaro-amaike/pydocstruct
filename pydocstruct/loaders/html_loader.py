"""pydocstruct/loaders/html_loader.py"""
from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

from pydocstruct.core.document import Document
from pydocstruct.core.loader import BaseLoader


class HtmlLoader(BaseLoader):
    """HTMLファイルを読み込むローダー"""

    def __init__(
        self,
        file_path: str | Path,
        encoding: str = "utf-8",
        preserve_structure: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(file_path, encoding, **kwargs)
        self.preserve_structure = preserve_structure
        
        if BeautifulSoup is None:
            raise ImportError(
                "beautifulsoup4がインストールされていません。"
                "pip install beautifulsoup4 でインストールしてください。"
            )

    def load(self) -> list[Document]:
        """HTMLファイルを読み込む
        
        script, styleタグを除去してテキストを抽出します。
        titleタグをメタデータとして取得します。
        preserve_structure=Trueの場合、markdownifyを使用して構造を保持したMarkdownとして抽出します。
        """
        with open(self.file_path, "r", encoding=self.encoding) as file:
            soup = BeautifulSoup(file, "html.parser")

        # script, styleタグを削除
        for script in soup(["script", "style"]):
            script.decompose()

        metadata = self._create_base_metadata()
        
        # タイトルがあればメタデータに追加
        if soup.title:
            metadata["title"] = soup.title.string

        if self.preserve_structure:
            try:
                import markdownify
                text = markdownify.markdownify(str(soup), heading_style="ATX", strip=["script", "style"])
                # 連続する空行を削減
                import re
                text = re.sub(r'\n{3,}', '\n\n', text).strip()
            except ImportError:
                 # fallback if markdownify is not present (though we will advise user to install it)
                 # For robustness, we could raise error or warn. Let's warn/error.
                 raise ImportError("markdownify is required for preserve_structure=True. pip install markdownify")
        else:
            # テキストを抽出
            text = soup.get_text(separator="\n", strip=True)

        return [
            Document(
                content=text,
                metadata=metadata,
                source=str(self.file_path),
            )
        ]

