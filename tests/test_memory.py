import memory
from rag_backend import build_retrieval_query


def test_build_retrieval_query_enriches_followup():
    history = [{"role": "user", "content": "What is the company leave policy?"}]
    enriched = build_retrieval_query("How many days?", history)
    assert "leave policy" in enriched.lower()
    assert "How many days?" in enriched


def test_build_retrieval_query_keeps_standalone_question():
    history = [{"role": "user", "content": "What is the leave policy?"}]
    query = "Summarize the onboarding process for new engineers in detail"
    assert build_retrieval_query(query, history) == query


def test_memory_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(memory, "MEMORY_DB_PATH", tmp_path / "test_memory.db")
    session = memory.new_session_id()
    memory.add_message(session, "user", "Hello")
    memory.add_message(session, "assistant", "Hi there")
    messages = memory.get_messages(session)
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    memory.clear_session(session)
    assert memory.get_messages(session) == []
