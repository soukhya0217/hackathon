import streamlit as st

st.set_page_config(
    page_title="Enterprise RAG Assistant",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Design tokens (from text.txt)
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#003d9b",
    "primary_container": "#0052cc",
    "on_primary": "#ffffff",
    "primary_fixed": "#dae2ff",
    "on_primary_fixed_variant": "#0040a2",
    "secondary_fixed": "#d9e2ff",
    "on_secondary_fixed_variant": "#00419d",
    "background": "#f8f9fb",
    "surface": "#f8f9fb",
    "surface_container_low": "#f3f4f6",
    "surface_container": "#edeef0",
    "surface_container_high": "#e7e8ea",
    "surface_container_lowest": "#ffffff",
    "on_surface": "#191c1e",
    "on_surface_variant": "#434654",
    "outline_variant": "#c3c6d6",
    "outline": "#737685",
    "error": "#ba1a1a",
    "error_container": "#ffdad6",
}

PROFILE_IMG = (
    "https://lh3.googleusercontent.com/aida-public/AB6AXuB6VyasX9Z2O0z098HbUZs2_"
    "wkmDFTzmd-6qY_p2_q_zRcu7C5Z9zJAtum5FsvMsRGIjtGvayN28HsJLqeYOg226AC3bWkmb"
    "Vx9TCXdduYEid3sKsbV_HpAPs39MYvOvFRRE0Q-mvn7f-bufifnPMCoIt_dNyeqpe9GfxzBk"
    "PbVK1OpL_VFI-tbHxf6JsEGF76Dzj7aCv9aqQb9bZs002h3PGXtKXqsC-v-44SI4gY1-x3wn"
    "VrhapbiWqV_jhlPBeKWhYShvTs46TlF"
)

SUGGESTIONS = [
    {
        "icon": "summarize",
        "title": "Summarize the uploaded document",
        "desc": "Get a concise executive summary of key points and takeaways.",
    },
    {
        "icon": "policy",
        "title": "What policies are mentioned?",
        "desc": "Extract specific compliance, HR, or operational guidelines automatically.",
    },
    {
        "icon": "hail",
        "title": "Explain the onboarding process",
        "desc": "Understand internal workflows and employee lifecycle procedures.",
    },
    {
        "icon": "target",
        "title": "What are the key objectives?",
        "desc": "Identify strategic goals and mission-critical targets in the data.",
    },
]

NAV_TABS = ["Conversations", "Models", "Security"]


def init_state():
    defaults = {
        "messages": [],
        "prompt_area": "",
        "documents": [],
        "active_tab": "Conversations",
        "show_welcome": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def doc_count() -> int:
    return len(st.session_state.documents)


def chunk_count() -> int:
    return sum(max(1, len(doc.get("name", "")) // 8) for doc in st.session_state.documents)


def kb_active() -> bool:
    return doc_count() > 0


def inject_styles():
    c = COLORS
    st.markdown(
        f"""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono&display=swap" rel="stylesheet"/>
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

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
                padding: 0 !important;
                max-width: 100% !important;
            }}

            [data-testid="stAppViewContainer"] > .main {{
                background: {c["background"]};
            }}

            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #f3f4f6 0%, #edeef0 100%) !important;
                border-right: 1px solid {c["outline_variant"]};
                min-width: 260px !important;
                width: 260px !important;
            }}

            [data-testid="stSidebar"] > div:first-child {{
                padding: 1.5rem 1rem 1rem 1rem;
            }}

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
                margin-bottom: 0;
            }}

            .material-symbols-outlined {{
                font-family: 'Material Symbols Outlined' !important;
                font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
                vertical-align: middle;
                line-height: 1;
            }}

            .ms-fill {{
                font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            }}

            .pulse-dot {{
                animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            }}

            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.4; }}
            }}

            .shadow-soft {{
                box-shadow: 0 4px 12px rgba(9, 30, 66, 0.08);
            }}

            /* Sidebar widgets */
            [data-testid="stSidebar"] .stButton > button {{
                width: 100%;
                border-radius: 0.5rem;
                font-weight: 600;
                font-size: 12px;
                letter-spacing: 0.05em;
                border: none;
                transition: all 0.15s ease;
            }}

            .upload-btn button {{
                background: {c["primary"]} !important;
                color: {c["on_primary"]} !important;
                padding: 0.75rem 1.5rem !important;
                box-shadow: 0 4px 12px rgba(9, 30, 66, 0.08);
            }}

            .upload-btn button:hover {{
                background: {c["primary_container"]} !important;
                color: {c["on_primary"]} !important;
            }}

            .clear-btn button {{
                background: transparent !important;
                color: {c["error"]} !important;
                border: none !important;
                text-align: left !important;
                padding: 0.5rem !important;
                font-weight: 400 !important;
                font-size: 14px !important;
                letter-spacing: normal !important;
            }}

            .clear-btn button:hover {{
                background: {c["error_container"]} !important;
            }}

            .settings-btn button {{
                background: transparent !important;
                color: {c["on_surface_variant"]} !important;
                border: none !important;
                text-align: left !important;
                padding: 0.5rem !important;
                font-weight: 400 !important;
                font-size: 14px !important;
                letter-spacing: normal !important;
            }}

            .settings-btn button:hover {{
                background: {c["surface_container_high"]} !important;
            }}

            [data-testid="stFileUploader"] {{
                padding: 0;
                margin-bottom: 1.5rem;
            }}

            [data-testid="stFileUploader"] section {{
                padding: 0;
            }}

            [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {{
                background: {c["primary"]};
                border: none;
                border-radius: 0.5rem;
                padding: 0.75rem 1.5rem;
                min-height: 44px;
                box-shadow: 0 4px 12px rgba(9, 30, 66, 0.08);
            }}

            [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"]::before {{
                content: "Document Upload";
                color: {c["on_primary"]};
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.05em;
                display: block;
                text-align: center;
            }}

            [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] > div {{
                display: none !important;
            }}

            [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"]:hover {{
                background: {c["primary_container"]};
            }}

            [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] span,
            [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] small {{
                color: {c["on_primary"]} !important;
            }}

            [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] svg {{
                fill: {c["on_primary"]} !important;
            }}

            [data-testid="stFileUploader"] button {{
                background: transparent !important;
                color: {c["on_primary"]} !important;
                border: none !important;
                font-weight: 600 !important;
                font-size: 12px !important;
                letter-spacing: 0.05em !important;
            }}

            /* Main area */
            .topbar {{
                height: 64px;
                border-bottom: 1px solid {c["outline_variant"]};
                background: {c["surface"]};
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 1.5rem;
                margin-bottom: 0;
            }}

            .topbar-title {{
                font-size: 24px;
                font-weight: 800;
                color: {c["on_surface"]};
                letter-spacing: -0.01em;
            }}

            .nav-tab {{
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.05em;
                color: {c["on_surface_variant"]};
                text-decoration: none;
                padding-bottom: 4px;
                margin-right: 1.5rem;
                cursor: default;
            }}

            .nav-tab.active {{
                color: {c["primary"]};
                border-bottom: 2px solid {c["primary"]};
            }}

            .status-pill {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 4px 12px;
                border-radius: 999px;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 0.05em;
            }}

            .pill-rag {{
                background: {c["primary_fixed"]};
                color: {c["on_primary_fixed_variant"]};
            }}

            .pill-memory {{
                background: {c["secondary_fixed"]};
                color: {c["on_secondary_fixed_variant"]};
            }}

            .avatar {{
                width: 32px;
                height: 32px;
                border-radius: 50%;
                border: 1px solid {c["outline"]};
                object-fit: cover;
            }}

            .hero-card {{
                background: white;
                border: 1px solid {c["outline_variant"]};
                border-radius: 0.5rem;
                padding: 2rem;
                box-shadow: 0 4px 12px rgba(9, 30, 66, 0.08);
                position: relative;
                overflow: hidden;
                margin-bottom: 1.5rem;
            }}

            .hero-glow {{
                position: absolute;
                right: -48px;
                top: -48px;
                width: 256px;
                height: 256px;
                background: rgba(0, 61, 155, 0.05);
                border-radius: 50%;
                filter: blur(48px);
            }}

            .hero-icon {{
                background: {c["primary_fixed"]};
                color: {c["on_primary_fixed_variant"]};
                width: 48px;
                height: 48px;
                border-radius: 0.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 1.5rem;
            }}

            .hero-title {{
                font-size: 30px;
                font-weight: 700;
                line-height: 38px;
                letter-spacing: -0.02em;
                color: {c["on_surface"]};
                margin: 0 0 1rem 0;
            }}

            .hero-subtitle {{
                font-size: 16px;
                line-height: 24px;
                color: {c["on_surface_variant"]};
                max-width: 36rem;
                margin: 0 0 2rem 0;
            }}

            .action-card {{
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 1rem;
                background: {c["surface_container_low"]};
                border: 1px solid {c["outline_variant"]};
                border-radius: 0.5rem;
                text-align: left;
            }}

            .action-card-icon {{
                background: white;
                padding: 0.75rem;
                border-radius: 0.5rem;
                border: 1px solid {c["outline_variant"]};
                color: {c["on_surface_variant"]};
            }}

            .action-card-title {{
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.05em;
                color: {c["on_surface"]};
                margin: 0;
            }}

            .action-card-desc {{
                font-size: 12px;
                color: {c["on_surface_variant"]};
                margin: 0;
            }}

            .suggestion-card {{
                background: white;
                border: 1px solid {c["outline_variant"]};
                border-radius: 0.5rem;
                padding: 1.5rem;
                height: 100%;
                transition: border-color 0.15s ease, box-shadow 0.15s ease;
            }}

            .suggestion-card:hover {{
                border-color: {c["primary_container"]};
                box-shadow: 0 4px 12px rgba(9, 30, 66, 0.08);
            }}

            .suggestion-title {{
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.05em;
                color: {c["on_surface"]};
                margin: 0.5rem 0 0 0;
            }}

            .suggestion-desc {{
                font-size: 12px;
                color: {c["on_surface_variant"]};
                margin: 0.25rem 0 0 0;
            }}

            .chat-footer-note {{
                text-align: center;
                font-size: 12px;
                color: {c["on_surface_variant"]};
                opacity: 0.6;
                margin-top: 1rem;
            }}

            .chat-input-wrap {{
                background: white;
                border: 2px solid {c["outline_variant"]};
                border-radius: 1rem;
                overflow: hidden;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            }}

            .chat-input-toolbar {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0.75rem 1.5rem;
                border-top: 1px solid {c["outline_variant"]};
                background: rgba(237, 238, 240, 0.5);
            }}

            .toolbar-left {{
                display: flex;
                align-items: center;
                gap: 1rem;
                color: {c["on_surface_variant"]};
                font-family: 'JetBrains Mono', monospace;
                font-size: 13px;
            }}

            .toolbar-icon {{
                color: {c["on_surface_variant"]};
                cursor: default;
            }}

            .toolbar-divider {{
                width: 1px;
                height: 24px;
                background: {c["outline_variant"]};
            }}

            .send-btn button {{
                background: {c["primary"]} !important;
                color: {c["on_primary"]} !important;
                border-radius: 0.5rem !important;
                font-size: 12px !important;
                font-weight: 600 !important;
                letter-spacing: 0.05em !important;
                padding: 0.5rem 1.5rem !important;
                border: none !important;
            }}

            .send-btn button:hover {{
                background: {c["primary_container"]} !important;
            }}

            .suggest-btn button {{
                background: white !important;
                color: {c["on_surface"]} !important;
                border: 1px solid {c["outline_variant"]} !important;
                border-radius: 0.5rem !important;
                padding: 1.5rem !important;
                height: auto !important;
                min-height: 140px !important;
                text-align: left !important;
                font-weight: 400 !important;
                letter-spacing: normal !important;
                white-space: normal !important;
                line-height: 1.4 !important;
                box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
            }}

            .suggest-btn button:hover {{
                border-color: {c["primary_container"]} !important;
                box-shadow: 0 4px 12px rgba(9, 30, 66, 0.08) !important;
            }}

            .suggest-btn button p {{
                margin: 0;
            }}

            .suggest-btn .suggest-title {{
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.05em;
                color: {c["on_surface"]};
                margin-top: 0.5rem;
            }}

            .suggest-btn .suggest-desc {{
                font-size: 12px;
                color: {c["on_surface_variant"]};
                margin-top: 0.25rem;
            }}

            .tab-btn button {{
                background: transparent !important;
                color: {c["on_surface_variant"]} !important;
                border: none !important;
                border-bottom: 2px solid transparent !important;
                border-radius: 0 !important;
                font-size: 12px !important;
                font-weight: 600 !important;
                letter-spacing: 0.05em !important;
                padding: 0 0 4px 0 !important;
                min-height: 0 !important;
            }}

            .tab-btn.active button {{
                color: {c["primary"]} !important;
                border-bottom: 2px solid {c["primary"]} !important;
            }}

            .tab-btn button:hover {{
                color: {c["primary"]} !important;
            }}

            div[data-testid="stTextArea"] textarea {{
                border: none !important;
                box-shadow: none !important;
                background: transparent !important;
                font-size: 14px !important;
                min-height: 100px !important;
                padding: 1.5rem !important;
            }}

            div[data-testid="stTextArea"] {{
                margin-bottom: 0 !important;
            }}

            .msg-user {{
                background: {c["primary_fixed"]};
                color: {c["on_primary_fixed_variant"]};
                padding: 0.75rem 1rem;
                border-radius: 0.5rem;
                margin: 0.5rem 0;
                font-size: 14px;
            }}

            .msg-assistant {{
                background: white;
                border: 1px solid {c["outline_variant"]};
                padding: 0.75rem 1rem;
                border-radius: 0.5rem;
                margin: 0.5rem 0;
                font-size: 14px;
            }}

            .kb-empty {{
                padding: 2rem 1rem;
                border: 2px dashed {c["outline_variant"]};
                border-radius: 0.5rem;
                text-align: center;
                opacity: 0.6;
                margin: 0.5rem 0 1.5rem 0;
            }}

            .kb-doc-item {{
                font-size: 12px;
                color: {c["on_surface_variant"]};
                padding: 0.35rem 0.5rem;
                background: {c["surface_container_lowest"]};
                border: 1px solid {c["outline_variant"]};
                border-radius: 0.25rem;
                margin-bottom: 0.25rem;
            }}

            .status-card {{
                background: {c["surface_container"]};
                border: 1px solid {c["outline_variant"]};
                border-radius: 0.5rem;
                padding: 1rem;
                margin: 1rem 0;
            }}

            .stat-box {{
                text-align: center;
                padding: 0.5rem;
                background: {c["surface_container_lowest"]};
                border: 1px solid {c["outline_variant"]};
                border-radius: 0.5rem;
            }}

            .stat-label {{
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 0.05em;
                color: {c["on_surface_variant"]};
                margin: 0;
            }}

            .stat-value {{
                font-size: 18px;
                font-weight: 600;
                color: {c["primary"]};
                margin: 0;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand():
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:2rem;">
            <div style="background:{COLORS['primary']};padding:8px;border-radius:0.5rem;display:flex;">
                <span class="material-symbols-outlined ms-fill" style="color:{COLORS['on_primary']};font-size:20px;">database</span>
            </div>
            <div>
                <div style="font-size:18px;font-weight:700;color:{COLORS['primary']};line-height:1.2;">Enterprise RAG</div>
                <div style="font-size:12px;color:{COLORS['on_surface_variant']};">Intelligence Control</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_kb():
    count = doc_count()
    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;align-items:center;padding:0 0.5rem;margin-bottom:0.5rem;">
            <span style="font-size:12px;font-weight:600;letter-spacing:0.05em;color:{COLORS['on_surface_variant']};text-transform:uppercase;">Knowledge Base</span>
            <span style="background:{COLORS['surface_container_high']};padding:2px 8px;border-radius:999px;font-family:'JetBrains Mono',monospace;font-size:13px;">{count}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if count == 0:
        st.markdown(
            f"""
            <div class="kb-empty">
                <span class="material-symbols-outlined" style="font-size:28px;color:{COLORS['on_surface_variant']};">folder_open</span>
                <p style="font-size:12px;color:{COLORS['on_surface_variant']};margin:0.5rem 0 0 0;">No documents indexed yet.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for doc in st.session_state.documents:
            st.markdown(
                f'<div class="kb-doc-item">📄 {doc["name"]}</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
        <div style="margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid {COLORS['outline_variant']};">
            <div style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem;color:{COLORS['on_surface_variant']};">
                <span class="material-symbols-outlined" style="font-size:20px;">monitoring</span>
                <span style="font-size:14px;">Analytics</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_status():
    active = kb_active()
    status_color = "#16a34a" if active else COLORS["error"]
    status_label = "Active" if active else "Inactive"
    pulse_class = "" if active else "pulse-dot"

    st.markdown(
        f"""
        <div class="status-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                <span style="font-size:12px;font-weight:600;letter-spacing:0.05em;color:{COLORS['on_surface_variant']};">KB STATUS</span>
                <div style="display:flex;align-items:center;gap:4px;">
                    <div class="{pulse_class}" style="width:8px;height:8px;border-radius:50%;background:{status_color};"></div>
                    <span style="font-size:10px;font-weight:600;color:{status_color};text-transform:uppercase;">{status_label}</span>
                </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                <div class="stat-box">
                    <p class="stat-label">DOCS</p>
                    <p class="stat-value">{doc_count()}</p>
                </div>
                <div class="stat-box">
                    <p class="stat-label">CHUNKS</p>
                    <p class="stat-value">{chunk_count()}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_topbar():
    left, tabs, right = st.columns([2, 2.5, 3])

    with left:
        st.markdown('<div class="topbar-title">RAG Assistant</div>', unsafe_allow_html=True)

    with tabs:
        tab_cols = st.columns(len(NAV_TABS))
        for i, tab in enumerate(NAV_TABS):
            with tab_cols[i]:
                css_class = "tab-btn active" if st.session_state.active_tab == tab else "tab-btn"
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                if st.button(tab, key=f"tab_{tab}"):
                    st.session_state.active_tab = tab
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;justify-content:flex-end;gap:0.75rem;flex-wrap:wrap;">
                <div class="status-pill pill-rag">
                    <span class="material-symbols-outlined ms-fill" style="font-size:14px;">security</span>
                    RAG ENABLED
                </div>
                <div class="status-pill pill-memory">
                    <span class="material-symbols-outlined ms-fill" style="font-size:14px;">memory</span>
                    MEMORY ENABLED
                </div>
                <div style="width:1px;height:32px;background:{COLORS['outline_variant']};"></div>
                <span class="material-symbols-outlined" style="color:{COLORS['on_surface_variant']};font-size:22px;">notifications</span>
                <img class="avatar" src="{PROFILE_IMG}" alt="User profile"/>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_hero():
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-glow"></div>
            <div style="position:relative;z-index:1;">
                <div class="hero-icon">
                    <span class="material-symbols-outlined" style="font-size:32px;">neurology</span>
                </div>
                <h2 class="hero-title">Welcome to your AI <br/><span style="color:{COLORS['primary']};">Knowledge Assistant</span></h2>
                <p class="hero-subtitle">
                    Upload documents to create your enterprise knowledge assistant. Our RAG engine will index your content to provide grounded, traceable, and secure answers.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="action-card">
                <div class="action-card-icon">
                    <span class="material-symbols-outlined">upload</span>
                </div>
                <div>
                    <p class="action-card-title">Start Indexing</p>
                    <p class="action-card-desc">PDF, DOCX, or TXT files</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="action-card">
                <div class="action-card-icon">
                    <span class="material-symbols-outlined">menu_book</span>
                </div>
                <div>
                    <p class="action-card-title">Explore Docs</p>
                    <p class="action-card-desc">View knowledge base</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_suggestions():
    row1 = st.columns(2)
    row2 = st.columns(2)
    cols = [row1[0], row1[1], row2[0], row2[1]]

    for i, suggestion in enumerate(SUGGESTIONS):
        with cols[i]:
            st.markdown('<div class="suggest-btn">', unsafe_allow_html=True)
            label = (
                f"📄 **{suggestion['title']}**\n\n"
                f"{suggestion['desc']}"
            )
            if st.button(label, key=f"suggest_{i}", use_container_width=True):
                st.session_state.prompt_area = suggestion["title"]
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


def render_messages():
    for msg in st.session_state.messages:
        css = "msg-user" if msg["role"] == "user" else "msg-assistant"
        st.markdown(f'<div class="{css}">{msg["content"]}</div>', unsafe_allow_html=True)


def handle_send(prompt: str):
    prompt = prompt.strip()
    if not prompt:
        return
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.show_welcome = False
    if kb_active():
        reply = (
            f"I found relevant context across {doc_count()} document(s). "
            f"Here's a grounded response to: *{prompt}*"
        )
    else:
        reply = (
            "No documents are indexed yet. Upload PDF, DOCX, or TXT files "
            "via **Document Upload** in the sidebar to enable RAG answers."
        )
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.prompt_area = ""


def render_chat_input():
    st.markdown('<div class="chat-input-wrap">', unsafe_allow_html=True)
    prompt = st.text_area(
        "chat",
        placeholder="Ask anything about your enterprise knowledge...",
        label_visibility="collapsed",
        height=100,
        key="prompt_area",
    )

    tool_left, tool_right = st.columns([3, 1])
    with tool_left:
        st.markdown(
            f"""
            <div class="chat-input-toolbar" style="border-top:1px solid {COLORS['outline_variant']};background:rgba(237,238,240,0.5);padding:0.75rem 1.5rem;">
                <div class="toolbar-left">
                    <span class="material-symbols-outlined toolbar-icon">attach_file</span>
                    <span class="material-symbols-outlined toolbar-icon">mic</span>
                    <div class="toolbar-divider"></div>
                    <span>Markdown Supported</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with tool_right:
        st.markdown('<div class="send-btn" style="padding:0.5rem 1rem 0.5rem 0;">', unsafe_allow_html=True)
        if st.button("Send Request ➤", use_container_width=True):
            handle_send(prompt)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<p class="chat-footer-note">AI can make mistakes. Check important info. Secure & Private Enterprise Instance.</p>',
        unsafe_allow_html=True,
    )


def process_uploads(uploaded_files):
    if not uploaded_files:
        return
    existing = {d["name"] for d in st.session_state.documents}
    for f in uploaded_files:
        if f.name not in existing:
            st.session_state.documents.append({"name": f.name, "size": f.size})
    st.session_state.show_welcome = len(st.session_state.messages) == 0


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
init_state()
inject_styles()

with st.sidebar:
    render_sidebar_brand()

    uploaded = st.file_uploader(
        "Document Upload",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Upload PDF, DOCX, or TXT files",
    )
    process_uploads(uploaded)

    render_sidebar_kb()
    render_sidebar_status()

    st.markdown('<div class="settings-btn">', unsafe_allow_html=True)
    st.button("⚙️  Settings", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("🗑️  Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.prompt_area = ""
        st.session_state.show_welcome = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Main content
st.markdown(
    f'<div style="border-bottom:1px solid {COLORS["outline_variant"]};background:{COLORS["surface"]};padding:0 1.5rem;">',
    unsafe_allow_html=True,
)
render_topbar()
st.markdown("</div>", unsafe_allow_html=True)

main_col, _ = st.columns([6, 0.3])
with main_col:
    st.markdown('<div style="max-width:48rem;margin:0 auto;padding:2rem 1.5rem 0;">', unsafe_allow_html=True)

    tab = st.session_state.active_tab

    if tab == "Conversations":
        if st.session_state.messages:
            render_messages()
        elif st.session_state.show_welcome:
            render_hero()
            render_suggestions()
    elif tab == "Models":
        st.markdown(
            f"""
            <div class="hero-card">
                <div class="hero-icon"><span class="material-symbols-outlined" style="font-size:32px;">model_training</span></div>
                <h2 class="hero-title">Model Configuration</h2>
                <p class="hero-subtitle">
                    Select and configure the LLM powering your RAG pipeline. Enterprise models support
                    temperature tuning, token limits, and grounding strength controls.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="hero-card">
                <div class="hero-icon"><span class="material-symbols-outlined" style="font-size:32px;">shield_lock</span></div>
                <h2 class="hero-title">Security & Compliance</h2>
                <p class="hero-subtitle">
                    Manage access controls, audit logs, and data retention policies. All queries are
                    processed within your secure enterprise instance with end-to-end encryption.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if tab == "Conversations":
        st.markdown('<div style="max-width:56rem;margin:0 auto;padding:0 1.5rem 2rem;">', unsafe_allow_html=True)
        render_chat_input()
        st.markdown("</div>", unsafe_allow_html=True)
