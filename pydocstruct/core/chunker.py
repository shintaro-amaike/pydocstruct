"""pydocstruct/core/chunker.py"""
from __future__ import annotations

import re
from typing import Any, List

try:
    import tiktoken
except ImportError:
    tiktoken = None

from pydocstruct.core.document import Document


class BaseChunker:
    """Base class for chunkers"""

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """Split a list of Documents into chunks

        Args:
            documents (list[Document]): List of documents to split

        Returns:
            list[Document]: List of chunked documents
        """
        chunked_documents = []
        
        for doc in documents:
            chunks = self.split_text(doc.content)
            
            for idx, chunk in enumerate(chunks):
                chunk_metadata = doc.metadata.copy()
                chunk_metadata["chunk_total"] = len(chunks)
                
                chunked_doc = Document(
                    content=chunk,
                    metadata=chunk_metadata,
                    doc_id=doc.doc_id,
                    source=doc.source,
                    page_number=doc.page_number,
                    chunk_index=idx,
                )
                
                chunked_documents.append(chunked_doc)
        
        return chunked_documents

    def split_text(self, text: str) -> list[str]:
        raise NotImplementedError


class TextChunker(BaseChunker):
    """Simple character-count based chunker"""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separator: str = "\n\n",
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
    
    def split_text(self, text: str) -> list[str]:
        text = re.sub(r'\s+', ' ', text).strip()
        
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start_index = 0
        
        while start_index < len(text):
            end_index = start_index + self.chunk_size
            
            if end_index >= len(text):
                chunks.append(text[start_index:])
                break
            
            chunk_text = text[start_index:end_index]
            last_space = chunk_text.rfind(' ')
            
            if last_space != -1:
                end_index = start_index + last_space
            
            chunks.append(text[start_index:end_index].strip())
            start_index = end_index - self.chunk_overlap
        
        return chunks


class RecursiveCharacterChunker(BaseChunker):
    """Recursive character-based chunker
    
    Attempts to split text by largest separators first to preserve meaningful chunks.
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: list[str] | None = None,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", " ", ""]
        
    def split_text(self, text: str) -> list[str]:
        return self._split_text(text, self.separators)

    def _split_text(self, text: str, separators: list[str]) -> list[str]:
        final_chunks = []
        
        # Determine separator to use
        separator = separators[-1]
        new_separators = []
        
        for i, sep in enumerate(separators):
            if sep == "":
                separator = sep
                break
            if sep in text:
                separator = sep
                new_separators = separators[i + 1:]
                break
                
        # Split by separator
        if separator:
            splits = text.split(separator)
        else:
            splits = list(text) # Character level
            
        # Recombine and verify
        good_splits = []
        _separator = separator if separator else ""
        
        for split in splits:
            if not split:
                continue
            if len(split) < self.chunk_size:
                good_splits.append(split)
            else:
                if new_separators:
                    good_splits.extend(self._split_text(split, new_separators))
                else:
                    good_splits.append(split)
                    
        return self._merge_splits(good_splits, _separator)

    def _merge_splits(self, splits: list[str], separator: str) -> list[str]:
        chunks = []
        current_doc = []
        total_len = 0
        
        for split in splits:
            _len = len(split)
            if total_len + _len + (len(separator) if current_doc else 0) > self.chunk_size:
                if current_doc:
                    doc = separator.join(current_doc)
                    if doc.strip():
                        chunks.append(doc)
                    
                    # Overlap handling (simplified: keep last n items that fit)
                    # For strict overlap, logic needs to be more complex.
                    # Here we just start new doc with current split.
                    # Implementing a robust overlap queue is better.
                    
                    while total_len > self.chunk_overlap and current_doc:
                         total_len -= len(current_doc[0]) + (len(separator) if len(current_doc) > 1 else 0)
                         current_doc.pop(0)
                         
                current_doc = [split]
                total_len = len(split)
            else:
                current_doc.append(split)
                total_len += _len + (len(separator) if len(current_doc) > 1 else 0)
                
        if current_doc:
            doc = separator.join(current_doc)
            if doc.strip():
                chunks.append(doc)
                
        return chunks


class TokenChunker(BaseChunker):
    """Token-count based chunker (uses tiktoken)"""
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        model_name: str = "gpt-3.5-turbo",
        encoding_name: str = "cl100k_base",
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model_name = model_name
        
        if tiktoken is None:
            raise ImportError("tiktoken is not installed. Please install it with `pip install tiktoken`.")
            
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            self.encoding = tiktoken.get_encoding(encoding_name)

    def split_text(self, text: str) -> list[str]:
        tokens = self.encoding.encode(text)
        
        if len(tokens) <= self.chunk_size:
            return [text]
            
        chunks = []
        start_index = 0
        
        while start_index < len(tokens):
            end_index = start_index + self.chunk_size
            
            chunk_tokens = tokens[start_index:end_index]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            if end_index >= len(tokens):
                break
                
            start_index = end_index - self.chunk_overlap
            
        return chunks

