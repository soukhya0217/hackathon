from langchain_core.documents import Document

from rag_backend import (
    answer_indicates_no_info,
    format_sources_for_ui,
    get_upload_manifest,
    split_documents,
)


def test_split_documents_preserves_metadata():
    docs = [
        Document(page_content="A" * 400 + "\n\n" + "B" * 400, metadata={"source": "test.pdf", "page": 0})
    ]
    chunks = split_documents(docs, chunk_size=500, chunk_overlap=50)
    assert len(chunks) >= 2
    assert all(c.metadata.get("source") == "test.pdf" for c in chunks)


def test_format_sources_for_ui_truncates_excerpt():
    chunks = [Document(page_content="word " * 100, metadata={"source": "/tmp/doc.pdf"})]
    sources = format_sources_for_ui(chunks, excerpt_len=50)
    assert len(sources) == 1
    assert len(sources[0]["excerpt"]) <= 51


def test_answer_indicates_no_info():
    assert answer_indicates_no_info("I could not find this information in your uploaded documents.")
    assert not answer_indicates_no_info("The HR policy allows 20 days of leave [1].")


def test_get_upload_manifest_empty(tmp_path):
    assert get_upload_manifest(tmp_path) == {}
