"""pydocstruct/loaders/pdf_loader.py"""
from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import pytesseract
    from pdf2image import convert_from_path
except ImportError:
    pytesseract = None
    convert_from_path = None

from pydocstruct.core.document import Document
from pydocstruct.core.loader import BaseLoader


class PDFLoader(BaseLoader):
    """Loader for PDF files
    
    Extracts text from PDF files using the pypdf library.
    Also supports OCR and layout preservation options.
    
    Attributes:
        extract_images (bool): Flag to extract images
        use_layout (bool): Whether to use layout preservation mode
        use_ocr (bool): Whether to use OCR
        ocr_lang (str): OCR language (e.g., "eng", "jpn")
    """
    
    def __init__(
        self,
        file_path: str | Path,
        extract_images: bool = False,
        use_layout: bool = False,
        use_ocr: bool = False,
        ocr_lang: str = "eng",
        **kwargs: Any,
    ) -> None:
        super().__init__(file_path, **kwargs)
        
        if pypdf is None:
            raise ImportError(
                "pypdfがインストールされていません。"
                "pip install pypdf でインストールしてください。"
            )
            
        if use_ocr and (pytesseract is None or convert_from_path is None):
            raise ImportError(
                "OCRには pytesseract と pdf2image が必要です。"
                "pip install pytesseract pdf2image を実行し、Tesseract-OCRとPopplerをインストールしてください。"
            )
        
        self.extract_images = extract_images
        self.use_layout = use_layout
        self.use_ocr = use_ocr
        self.ocr_lang = ocr_lang
    
    def load(self) -> list[Document]:
        """Load PDF file"""
        documents = []
        
        try:
            with open(self.file_path, "rb") as file:
                pdf_reader = pypdf.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, start=1):
                    # Determine text extraction mode
                    extraction_mode = "layout" if self.use_layout else "plain"
                    try:
                        text = page.extract_text(extraction_mode=extraction_mode)
                    except Exception:
                         # fallback to plain if layout fails (or old pypdf version)
                        text = page.extract_text()
                    
                    # Run OCR if text is empty and OCR is enabled
                    if not text.strip() and self.use_ocr:
                        text = self._perform_ocr(page_num)

                    if not text.strip():
                        continue
                    
                    metadata = self._create_base_metadata()
                    metadata["page_count"] = len(pdf_reader.pages)
                    metadata["page_number"] = page_num
                    
                    if pdf_reader.metadata:
                        metadata["pdf_metadata"] = {
                            "title": pdf_reader.metadata.get("/Title"),
                            "author": pdf_reader.metadata.get("/Author"),
                            "subject": pdf_reader.metadata.get("/Subject"),
                            "creator": pdf_reader.metadata.get("/Creator"),
                        }
                    
                    documents.append(Document(
                        content=text,
                        metadata=metadata,
                        source=str(self.file_path),
                        page_number=page_num,
                    ))
        except Exception as e:
            # OCR only fallback if PDF is unreadable by pypdf (e.g. encrypted or weird format but ok for image tools?)
            # But usually pypdf handles basic read.
            # If use_ocr is strictly requested for ALL pages despite text presence, users should implement logic to ignore extract_text.
            # Current logic: try text -> empty? -> OCR.
            raise e
        
        return documents

    def _perform_ocr(self, page_num: int) -> str:
        """Perform OCR on the specified page"""
        try:
            # Convert page to image (1-based index to list, but convert_from_path handles first_page/last_page)
            # page_num is 1-based.
            images = convert_from_path(
                str(self.file_path),
                first_page=page_num,
                last_page=page_num
            )
            
            if not images:
                return ""
                
            return pytesseract.image_to_string(images[0], lang=self.ocr_lang)
            
        except Exception as e:
            # Log empty string or error on OCR failure, returning empty string here
            return ""
