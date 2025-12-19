"""pydocstruct/core/loader.py"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from pydocstruct.core.document import Document


class BaseLoader(ABC):
    """Base class for file loaders
    
    Loaders for each file format should inherit from this class.
    
    Attributes:
        file_path (Path): Path to the file to load
        encoding (str): File encoding
        metadata (dict[str, Any]): Additional metadata
    """
    
    def __init__(
        self,
        file_path: str | Path,
        encoding: str = "utf-8",
        **kwargs: Any,
    ) -> None:
        """Initialize BaseLoader
        
        Args:
            file_path (str | Path): Path to the file to load
            encoding (str, optional): Encoding. Defaults to "utf-8".
            **kwargs: Additional metadata
        """
        # Convert file path to Path object
        self.file_path = Path(file_path)
        self.encoding = encoding
        self.metadata = kwargs
        
        # Check if file exists
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
    
    @abstractmethod
    def load(self) -> list[Document]:
        """Load file and convert to list of Documents
        
        Abstract method that must be implemented by subclasses.
        
        Returns:
            list[Document]: List of loaded documents
        """
        pass
    
    def _create_base_metadata(self) -> dict[str, Any]:
        """Generate base metadata
        
        Returns:
            dict[str, Any]: Base metadata including file info
        """
        # Get file info
        stat = self.file_path.stat()
        
        return {
            "source": str(self.file_path),
            "filename": self.file_path.name,
            "file_size": stat.st_size,
            "file_type": self.file_path.suffix,
            **self.metadata,
        }
