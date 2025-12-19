"""pydocstruct/core/document.py"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Document:
    """Class representing the basic structure of a document
    
    Provides a unified document representation for storage in RAG systems
    or vector data stores.
    
    Attributes:
        content (str): Document main text content
        metadata (dict[str, Any]): Metadata (author, creation time, filename, etc.)
        doc_id (str | None): Unique identifier for the document
        source (str | None): Document source (file path, URL, etc.)
        page_number (int | None): Page number (if applicable)
        chunk_index (int | None): Chunk index (if split)
    """
    
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    doc_id: str | None = None
    source: str | None = None
    page_number: int | None = None
    chunk_index: int | None = None
    
    def __post_init__(self) -> None:
        """Post-initialization processing
        
        Automatically adds a timestamp to metadata.
        """
        # Automatically add timestamp
        if "created_at" not in self.metadata:
            self.metadata["created_at"] = datetime.now().isoformat()
    
    def to_dict(self) -> dict[str, Any]:
        """Convert document to dictionary format
        
        Returns:
            dict[str, Any]: Dictionary representation of the document
        """
        return {
            "content": self.content,
            "metadata": self.metadata,
            "doc_id": self.doc_id,
            "source": self.source,
            "page_number": self.page_number,
            "chunk_index": self.chunk_index,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Document:
        """Generate Document instance from dictionary
        
        Args:
            data (dict[str, Any]): Dictionary of document data
            
        Returns:
            Document: Generated Document instance
        """
        return cls(**data)
