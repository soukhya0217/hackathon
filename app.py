import html
from pathlib import Path

import streamlit as st

import memory
from rag_backend import (
    UPLOAD_DIR,
    answer_question,
    build_knowledge_base,
    delete_uploaded_file,
    get_indexed_chunk_count,
    get_upload_manifest,
    save_uploaded_files,
    vectorstore_exists,
    vectorstore_index_mtime,
)
from rag_backend import load_vectorstore as _load_vectorstore

st.set_page_config(
    page_title="RAG Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "accent": "#6366f1",
    "accent_hover": "#4f46e5",
    "accent_light": "#eef2ff",
    "bg": "#ffffff",
    "sidebar": "#f7f7f8",
    "text": "#0d0d0d",
    "muted": "#6e6e80",
    "border": "#e5e5e5",
    "user_bubble": "#f4f4f4",
}


@st.cache_resource
def get_cached_vectorstore(index_mtime: float):
    if index_mtime <= 0:
        return None
    return _load_vectorstore()


def get_vectorstore():
    return get_cached_vectorstore(vectorstore_index_mtime())


def invalidate_vectorstore_cache():
    get_cached_vectorstore.clear()


def init_state():
    memory.init_db()

    defaults = {
        "messages": [],
        "documents": [],
        "show_welcome": True,
        "chunk_count": 0,
        "kb_indexed": False,
        "is_generating": False,
        "session_id": memory.new_session_id(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if not st.session_state.messages:
        st.session_state.messages = memory.get_messages(st.session_state.session_id)
        if st.session_state.messages:
            st.session_state.show_welcome = False

    if vectorstore_exists():
        st.session_state.kb_indexed = True
        st.session_state.chunk_count = get_indexed_chunk_count()

    sync_documents_from_disk()


def sync_documents_from_disk():
    if not UPLOAD_DIR.exists():
        st.session_state.documents = []
        return

    st.session_state.documents = [
        {"name": f.name, "size": f.stat().st_size}
        for f in sorted(UPLOAD_DIR.iterdir())
        if f.is_file() and not f.name.startswith(".")
    ]


def doc_count() -> int:
    return len(st.session_state.documents)


def kb_active() -> bool:
    return st.session_state.kb_indexed and vectorstore_exists()


def inject_styles():
    c = COLORS
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

            html, body, [class*="css"] {{
                font-family: 'Inter', sans-serif !important;
            }}

            #MainMenu, footer, header[data-testid="stHeader"] {{
                visibility: hidden !important;
                height: 0 !important;
            }}

            .stDeployButton, [data-testid="stToolbar"], [data-testid="stStatusWidget"] {{
                display: none !important;
            }}

            .block-container {{
                padding-top: 1rem !important;
                padding-bottom: 6rem !important;
                max-width: 48rem !important;
                margin: 0 auto !important;
            }}

            [data-testid="stAppViewContainer"] > .main {{
                background: {c["bg"]};
            }}

            [data-testid="stSidebar"] {{
                background: {c["sidebar"]} !important;
                border-right: 1px solid {c["border"]};
            }}

            [data-testid="stSidebar"] > div:first-child {{
                padding: 1.25rem 1rem;
            }}

            [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
                background: {c["accent"]} !important;
                border: none !important;
                border-radius: 8px !important;
                font-weight: 500 !important;
            }}

            [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{
                background: {c["accent_hover"]} !important;
            }}

            [data-testid="stSidebar"] .stButton > button[kind="secondary"] {{
                background: transparent !important;
                border: 1px solid {c["border"]} !important;
                border-radius: 8px !important;
                color: {c["text"]} !important;
            }}

            .welcome-box {{
                text-align: center;
                padding: 4rem 1rem 2rem;
                color: {c["text"]};
            }}

            .welcome-box h1 {{
                font-size: 1.75rem;
                font-weight: 600;
                margin: 0 0 0.5rem 0;
            }}

            .welcome-box p {{
                font-size: 1rem;
                color: {c["muted"]};
                margin: 0;
            }}

            [data-testid="stChatMessage"] {{
                background: transparent !important;
                padding: 0.75rem 0 !important;
            }}

            [data-testid="stChatMessageAvatarUser"] {{
                background: {c["accent"]} !important;
            }}

            [data-testid="stChatMessageAvatarAssistant"] {{
                background: {c["user_bubble"]} !important;
                color: {c["accent"]} !important;
            }}

            .grounded-note {{
                font-size: 0.75rem;
                color: {c["muted"]};
                margin-top: 0.25rem;
                font-style: italic;
            }}

            .source-card {{
                background: {c["accent_light"]};
                border: 1px solid {c["border"]};
                border-left: 3px solid {c["accent"]};
                border-radius: 8px;
                padding: 0.75rem 1rem;
                margin-bottom: 0.5rem;
            }}

            .source-card-title {{
                font-size: 0.85rem;
                font-weight: 600;
                color: {c["text"]};
                margin: 0 0 0.35rem 0;
            }}

            .source-card-excerpt {{
                font-size: 0.8rem;
                color: {c["muted"]};
                margin: 0;
                line-height: 1.45;
            }}

            [data-testid="stChatInput"] {{
                border-top: 1px solid {c["border"]};
                background: {c["bg"]};
            }}

            [data-testid="stChatInput"] textarea {{
                border: 1px solid {c["border"]} !important;
                border-radius: 1.5rem !important;
                padding: 0.75rem 1rem !important;
            }}

            [data-testid="stChatInput"] button {{
                background: {c["accent"]} !important;
                border-radius: 50% !important;
            }}

            [data-testid="stFileUploader"] {{
                font-size: 0.875rem;
            }}

            .sidebar-doc {{
                font-size: 0.8rem;
                color: {c["muted"]};
                padding: 0.25rem 0;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_source_citations(sources: list[dict]):
    if not sources:
        return

    with st.expander(
        f"📎 {len(sources)} source passage{'s' if len(sources) != 1 else ''} from your documents",
        expanded=False,
    ):
        for i, source in enumerate(sources, start=1):
            filename = html.escape(Path(source.get("source", "unknown")).name)
            page = source.get("page")
            page_label = f" · Page {page + 1}" if page is not None else ""
            excerpt = html.escape(source.get("excerpt", ""))
            st.markdown(
                f"""
                <div class="source-card">
                    <p class="source-card-title">[{i}] {filename}{page_label}</p>
                    <p class="source-card-excerpt">"{excerpt}"</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_messages():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("grounded") and msg.get("sources"):
                st.markdown(
                    '<p class="grounded-note">Synthesized from retrieved document passages — expand sources to see exact excerpts.</p>',
                    unsafe_allow_html=True,
                )
                render_source_citations(msg["sources"])


def generate_pending_answer():
    query = st.session_state.messages[-1]["content"]
    result = {"content": "", "sources": [], "grounded": False}

    with st.chat_message("assistant"):
        with st.status("Processing your question…", expanded=True) as status:
            if not kb_active():
                result = {
                    "content": (
                        "Upload documents in the sidebar, then click **Build Knowledge Base** "
                        "before asking questions."
                    ),
                    "sources": [],
                    "grounded": False,
                }
                status.update(label="Knowledge base not ready", state="error")
            else:
                try:
                    status.write("🔍 Searching knowledge base and generating answer…")
                    vectorstore = get_vectorstore()
                    chat_history = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages[:-1]
                    ]
                    if chat_history:
                        status.write(f"🧠 Using {len(chat_history)} prior message(s) for context")
                    rag_result = answer_question(
                        query,
                        vectorstore=vectorstore,
                        chat_history=chat_history,
                    )

                    if rag_result.get("no_index"):
                        result = {
                            "content": rag_result["answer"],
                            "sources": [],
                            "grounded": False,
                        }
                        status.update(label="Knowledge base not ready", state="error")
                    elif not rag_result["context_chunks"]:
                        result = {
                            "content": rag_result["answer"],
                            "sources": [],
                            "grounded": False,
                        }
                        status.update(label="No matching passages", state="complete")
                    elif not rag_result["grounded"]:
                        result = {
                            "content": rag_result["answer"],
                            "sources": [],
                            "grounded": False,
                        }
                        status.update(label="No relevant information found", state="complete")
                    else:
                        status.write(f"📄 Used {len(rag_result['context_chunks'])} matching passage(s)")
                        result = {
                            "content": rag_result["answer"],
                            "sources": rag_result["sources"],
                            "grounded": True,
                        }
                        status.update(label="Answer ready", state="complete")
                except ValueError as exc:
                    result = {"content": str(exc), "sources": [], "grounded": False}
                    status.update(label="Configuration error", state="error")
                except Exception as exc:
                    result = {
                        "content": f"Failed to generate answer: {exc}",
                        "sources": [],
                        "grounded": False,
                    }
                    status.update(label="Error", state="error")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["content"],
            "sources": result.get("sources", []),
            "grounded": result.get("grounded", False),
        }
    )
    memory.add_message(st.session_state.session_id, "assistant", result["content"])
    st.session_state.is_generating = False


def run_build_knowledge_base():
    with st.status("Building knowledge base…", expanded=True) as status:
        status.write("📂 Loading uploaded files…")
        result = build_knowledge_base()

        for warning in result.get("warnings", []):
            status.write(f"⚠️ {warning}")

        if not result["ok"]:
            st.session_state.build_kb_message = ("error", result.get("error", "Indexing failed."))
            status.update(label="Indexing failed", state="error")
            return

        if result.get("skipped_rebuild"):
            status.write("✅ Index is already up to date — skipped rebuild.")
        elif result.get("incremental"):
            status.write(f"➕ Added new file(s) to existing index ({result['chunk_count']} chunks total).")
        else:
            status.write(f"✂️ Indexed {result['document_count']} file(s) into {result['chunk_count']} chunks.")
            status.write("🧠 Embeddings complete.")

        status.update(label="Knowledge base ready", state="complete")

    invalidate_vectorstore_cache()
    st.session_state.chunk_count = result["chunk_count"]
    st.session_state.kb_indexed = True

    if result.get("skipped_rebuild"):
        msg = f"Index up to date · {result['chunk_count']} chunks."
    elif result.get("incremental"):
        msg = f"Added new file(s) · {result['chunk_count']} chunks total."
    else:
        msg = f"Indexed {doc_count()} file(s) · {result['chunk_count']} chunks."

    st.session_state.build_kb_message = ("success", msg)


def _uploads_changed(uploaded_files) -> bool:
    on_disk = get_upload_manifest()
    uploaded_meta = {f.name: {"size": f.size, "mtime_ns": 0} for f in uploaded_files}
    on_disk_sizes = {name: meta["size"] for name, meta in on_disk.items()}

    if set(uploaded_meta) != set(on_disk_sizes):
        return True
    return any(uploaded_meta[name]["size"] != on_disk_sizes[name] for name in uploaded_meta)


def process_uploads(uploaded_files):
    if uploaded_files:
        if _uploads_changed(uploaded_files):
            save_uploaded_files(uploaded_files)
            invalidate_vectorstore_cache()
            st.session_state.kb_indexed = False
            st.session_state.chunk_count = 0
            st.session_state.upload_notice = "New files saved — click **Build Knowledge Base** to index them."
        else:
            save_uploaded_files(uploaded_files)

    sync_documents_from_disk()
    st.session_state.show_welcome = len(st.session_state.messages) == 0


def remove_document(filename: str):
    if delete_uploaded_file(filename):
        invalidate_vectorstore_cache()
        st.session_state.kb_indexed = False
        st.session_state.chunk_count = 0
        sync_documents_from_disk()
        st.session_state.upload_notice = f"Removed **{filename}** — rebuild the knowledge base to update search."


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
init_state()
inject_styles()

with st.sidebar:
    st.markdown("### RAG Assistant")

    uploaded = st.file_uploader(
        "Upload PDF, DOCX, or TXT",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    process_uploads(uploaded)

    if st.session_state.get("upload_notice"):
        st.info(st.session_state.upload_notice)
        del st.session_state.upload_notice

    status_label = "Ready" if kb_active() else "Not indexed"
    st.caption(f"{doc_count()} documents · {st.session_state.chunk_count} chunks · {status_label}")
    st.caption("🧠 Memory enabled · SQLite session history")

    if st.button("Build Knowledge Base", key="build_kb", use_container_width=True, type="primary"):
        run_build_knowledge_base()
        st.rerun()

    if "build_kb_message" in st.session_state:
        level, text = st.session_state.build_kb_message
        if level == "success":
            st.success(text)
        else:
            st.error(text)
        del st.session_state.build_kb_message

    if st.session_state.documents:
        st.markdown("**Files**")
        for doc in st.session_state.documents:
            col_name, col_btn = st.columns([4, 1])
            with col_name:
                st.markdown(
                    f'<div class="sidebar-doc">📄 {html.escape(doc["name"])}</div>',
                    unsafe_allow_html=True,
                )
            with col_btn:
                if st.button("✕", key=f"del_{doc['name']}", help=f"Remove {doc['name']}"):
                    remove_document(doc["name"])
                    st.rerun()

    st.divider()

    if st.button("Clear chat", use_container_width=True):
        memory.clear_session(st.session_state.session_id)
        st.session_state.messages = []
        st.session_state.show_welcome = True
        st.session_state.is_generating = False
        st.rerun()

if st.session_state.messages:
    render_messages()
elif st.session_state.show_welcome:
    st.markdown(
        """
        <div class="welcome-box">
            <h1>How can I help you today?</h1>
            <p>Upload your documents, build the knowledge base, then ask anything.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if st.session_state.is_generating:
    generate_pending_answer()
    st.rerun()

if prompt := st.chat_input("Ask anything about your documents…", disabled=st.session_state.is_generating):
    st.session_state.messages.append({"role": "user", "content": prompt})
    memory.add_message(st.session_state.session_id, "user", prompt)
    st.session_state.show_welcome = False
    st.session_state.is_generating = True
    st.rerun()
