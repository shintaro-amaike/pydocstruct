# pydocstruct

[![PyPI version](https://badge.fury.io/py/pydocstruct.svg)](https://badge.fury.io/py/pydocstruct)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**pydocstruct** は、様々なファイルフォーマット（PDF, DOCX, Excel, Markdown, CSV, JSON等）を読み込み、RAG（Retrieval-Augmented Generation）システムやベクトルデータベースで扱いやすい構造化データに変換するためのPythonライブラリです。

RAG向けに最適化された機能（トークンベースのチャンク分割、Markdownテーブル変換、PII削除など）を提供します。

## 特徴

- 🌟 **統一インターフェース**: `pydocstruct.load()` 関数ひとつで全フォーマットに対応
- 📄 **多様なフォーマット**: PDF, Excel (XLSX), Word (DOCX), Markdown, Text, HTML, XML, JSON, CSV
- 🤖 **RAG最適化**:
    - **高度なチャンク分割**: 文字数ベースに加え、再帰的分割(`RecursiveCharacterChunker`)やトークン数ベース(`TokenChunker`)をサポート
    - **表現力**: CSV/ExcelをMarkdownテーブルとして抽出、HTMLの構造保持
    - **PDF高度化**: レイアウト解析、OCRによるスキャンPDF対応
- 🛡️ **データクリーニング**: 
    - **PII削除**: メールアドレス、電話番号などの個人情報を自動マスキング
    - **ノイズ除去**: HTMLのヘッダー/フッター/広告を除去

## インストール

```bash
pip install pydocstruct
```

### 依存関係のインストール

全機能（OCR、Excel、テーブル変換など）を利用するには、以下のコマンドで追加の依存パッケージをインストールすることをお勧めします。

```bash
pip install pydocstruct[all]
```
*(注意: 手動でインストールする場合: `pandas`, `openpyxl`, `tabulate`, `pypdf`, `python-docx`, `beautifulsoup4`, `markdownify`, `tiktoken`, `pdf2image`, `pytesseract`)*

⚠️ **OCR機能の利用要件**:
OCR機能(`use_ocr=True`)を利用するには、別途システムに以下のツールをインストールし、PATHを通す必要があります：
- **Tesseract-OCR**
- **Poppler** (for `pdf2image`)

## クイックスタート

### 基本的な読み込み

```python
from pydocstruct import load

# PDFファイルを読み込む
documents = load("paper.pdf")

for doc in documents:
    print(f"File: {doc.source}")
    print(f"Page: {doc.page_number}")
    print(f"Content: {doc.content[:100]}...")
```

`load` 関数は `list[Document]` を返します。

## 対応フォーマットと詳細

| フォーマット | 拡張子 | 説明 | 主なオプション |
|------------|-------|------|----------------|
| **PDF** | `.pdf` | ページごとにDocument化。OCR/レイアウト解析対応。 | `use_ocr=True`, `use_layout=True` |
| **Excel** | `.xlsx` | 行ごと、またはMarkdownテーブルとして読み込み。 | `output_format="markdown"` |
| **CSV** | `.csv` | 行ごと、またはMarkdownテーブルとして読み込み。 | `output_format="markdown"` |
| **Word** | `.docx` | ドキュメント全体を読み込み。 | - |
| **HTML** | `.html` | 本文抽出、または構造保持Markdown変換。 | `preserve_structure=True` |
| **Markdown** | `.md` | 見出し分割に対応。 | `split_by_headers=True` |
| **Text** | `.txt` | UTF-8テキストとして読み込み。 | - |

## 高度な機能

### 1. 構造化データのMarkdownテーブル変換 (CSV/Excel)

RAGにおいて、表データはMarkdownテーブル形式の方がLLMが理解しやすい傾向にあります。

```python
# ExcelをMarkdownテーブルとして読み込む
docs = load("data.xlsx", output_format="markdown")
print(docs[0].content)
# 出力例:
# | Product | Price |
# |:--------|------:|
# | Apple   |   100 |
```

### 2. PDFのOCRとレイアウト解析

スキャンされたPDFや複雑なレイアウトのPDFに対応します。

```python
# レイアウトを保持して抽出（マルチカラムに強い）
docs = load("paper.pdf", use_layout=True)

# テキストがないページに対してOCRを実行（要Tesseract/Poppler）
docs = load("scanned.pdf", use_ocr=True, ocr_lang="jpn")
```

### 3. 高度なチャンク分割 (Chunking)

LLMのコンテキストウィンドウに合わせて、より賢くテキストを分割します。

```python
from pydocstruct.core.chunker import RecursiveCharacterChunker, TokenChunker

# 再帰的分割 (段落 -> 文 -> 単語 の順で分割を試みる)
recursive_chunker = RecursiveCharacterChunker(chunk_size=1000, chunk_overlap=200)
chunked_docs = recursive_chunker.split_documents(documents)

# トークン数ベース分割 (tiktoken使用。GPTモデルに最適)
token_chunker = TokenChunker(chunk_size=500, model_name="gpt-4")
chunked_docs = token_chunker.split_documents(documents)
```

### 4. データクリーニング (Processors)

個人情報の削除やHTMLのノイズ除去が行えます。

```python
from pydocstruct.processors import PiiRedactor, HtmlNoiseCleaner

text = "連絡先: 090-1234-5678, email@example.com"

# PII（個人情報）の削除
cleaned_text = PiiRedactor.redact(text)
print(cleaned_text) 
# -> "連絡先: [REDACTED], [REDACTED]"

# HTMLノイズ除去（ヘッダー/フッター/広告などを削除）
clean_html_text = HtmlNoiseCleaner.clean(html_content)
```

## ライセンス

MIT License
