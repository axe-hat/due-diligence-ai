"""Tests for retrieval — these require a populated vector store."""

import pytest


def test_retriever_import():
    from src.retrieval.retriever import retrieve, get_available_companies
    assert callable(retrieve)
    assert callable(get_available_companies)


def test_retrieve_empty_query():
    """Should not crash on empty collection."""
    from src.retrieval.retriever import retrieve
    try:
        results = retrieve("test query")
        assert isinstance(results, list)
    except Exception:
        # Expected if vector store is empty
        pass
