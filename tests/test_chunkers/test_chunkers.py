"""tests/test_chunkers/test_chunkers.py"""
from __future__ import annotations

import pytest
from pydocstruct.core.chunker import TextChunker, RecursiveCharacterChunker
from pydocstruct.core.document import Document


class TestTextChunker:
    def test_short_text_returns_single_chunk(self):
        chunker = TextChunker(chunk_size=100)
        assert chunker.split_text("Hello world") == ["Hello world"]

    def test_long_text_is_split_into_multiple_chunks(self):
        chunker = TextChunker(chunk_size=10, chunk_overlap=0)
        chunks = chunker.split_text("a" * 30)
        assert len(chunks) > 1

    def test_all_words_appear_in_at_least_one_chunk(self):
        chunker = TextChunker(chunk_size=20, chunk_overlap=5)
        words = ["alpha", "beta", "gamma", "delta", "epsilon"]
        text = " ".join(words)
        combined = " ".join(chunker.split_text(text))
        for word in words:
            assert word in combined

    def test_no_empty_chunks(self):
        chunker = TextChunker(chunk_size=10, chunk_overlap=2)
        chunks = chunker.split_text("word1 word2 word3 word4 word5 word6")
        assert all(c.strip() for c in chunks)

    def test_no_infinite_loop_when_words_exceed_chunk_size(self):
        """chunk_sizeより長い単語があっても無限ループしないこと"""
        chunker = TextChunker(chunk_size=5, chunk_overlap=2)
        chunks = chunker.split_text("ab cd ef gh ij kl")
        assert len(chunks) >= 1

    def test_overlap_carries_content_into_next_chunk(self):
        chunker = TextChunker(chunk_size=15, chunk_overlap=8)
        text = "aaaaa bbbbb ccccc ddddd eeeee"
        chunks = chunker.split_text(text)
        if len(chunks) >= 2:
            # オーバーラップにより連続するチャンク間で内容が重複すること
            prev_tail = chunks[0][-5:]
            assert any(prev_tail in c for c in chunks[1:])

    def test_split_documents_sets_chunk_index(self):
        chunker = TextChunker(chunk_size=10, chunk_overlap=0)
        doc = Document(content="a" * 35)
        result = chunker.split_documents([doc])
        assert [d.chunk_index for d in result] == list(range(len(result)))

    def test_split_documents_sets_chunk_total(self):
        chunker = TextChunker(chunk_size=10, chunk_overlap=0)
        doc = Document(content="a" * 35)
        result = chunker.split_documents([doc])
        for d in result:
            assert d.metadata["chunk_total"] == len(result)

    def test_split_documents_preserves_source_and_metadata(self):
        chunker = TextChunker(chunk_size=10, chunk_overlap=0)
        doc = Document(content="a" * 30, metadata={"author": "taro"}, source="src.txt")
        result = chunker.split_documents([doc])
        for d in result:
            assert d.metadata["author"] == "taro"
            assert d.source == "src.txt"

    def test_text_equal_to_chunk_size_is_single_chunk(self):
        chunker = TextChunker(chunk_size=10, chunk_overlap=0)
        text = "a" * 10
        assert len(chunker.split_text(text)) == 1

    def test_empty_text_returns_empty_list(self):
        chunker = TextChunker(chunk_size=100)
        chunks = chunker.split_text("")
        assert chunks == [] or chunks == [""]


class TestRecursiveCharacterChunker:
    def test_short_text_returns_single_chunk(self):
        chunker = RecursiveCharacterChunker(chunk_size=200)
        assert chunker.split_text("Hello world") == ["Hello world"]

    def test_splits_by_double_newline_first(self):
        """最初に \\n\\n で段落分割を試みること"""
        chunker = RecursiveCharacterChunker(chunk_size=30, chunk_overlap=0)
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        chunks = chunker.split_text(text)
        assert len(chunks) >= 2
        assert any("First" in c for c in chunks)
        assert any("Second" in c or "Third" in c for c in chunks)

    def test_falls_back_to_single_newline(self):
        """\\n\\n がない場合は \\n で分割すること"""
        chunker = RecursiveCharacterChunker(chunk_size=20, chunk_overlap=0)
        text = "line one\nline two\nline three\nline four\nline five"
        chunks = chunker.split_text(text)
        assert len(chunks) >= 2

    def test_all_content_covered(self):
        chunker = RecursiveCharacterChunker(chunk_size=40, chunk_overlap=0)
        sections = ["Section one text here.", "Section two text here.", "Section three text here."]
        text = "\n\n".join(sections)
        combined = " ".join(chunker.split_text(text))
        for section in sections:
            for word in section.split():
                assert word in combined

    def test_split_documents_sets_chunk_index(self):
        chunker = RecursiveCharacterChunker(chunk_size=30, chunk_overlap=0)
        long_text = "\n\n".join(["section " + str(i) * 5 for i in range(6)])
        doc = Document(content=long_text)
        result = chunker.split_documents([doc])
        assert [d.chunk_index for d in result] == list(range(len(result)))

    def test_single_paragraph_within_chunk_size_is_not_split(self):
        chunker = RecursiveCharacterChunker(chunk_size=100, chunk_overlap=0)
        text = "This is a single short paragraph."
        chunks = chunker.split_text(text)
        assert len(chunks) == 1
        assert chunks[0] == text
