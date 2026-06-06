# Project Name : Enterprise RAG Assistant

# Problem Statement : Intelligent Conversational AI Agent

# Team No : 31

# College Name : CHRIST (Deemed to be University)

### Problem Statement

Organizations often store critical information across PDFs, policy documents, onboarding guides, project reports, and knowledge repositories. While this information exists, employees frequently struggle to locate the right answer quickly.

Traditional chatbots often fail because they:

* Cannot access organization-specific documents
* Lack conversational context
* Provide answers without references or traceability
* Require users to manually search through lengthy documents

There is a need for an intelligent conversational system that can:

* Retrieve information from enterprise documents
* Answer questions using document context
* Support follow-up questions naturally
* Provide transparent source citations

---

### Proposed Solution

**Enterprise RAG Assistant** is a Retrieval-Augmented Generation (RAG) powered conversational AI system that allows users to upload enterprise documents and interact with them through natural language.

The platform enables:

* Uploading PDF, DOCX, and TXT documents
* Building a semantic knowledge base from uploaded files
* Asking questions in natural language
* Retrieving relevant document sections automatically
* Generating grounded responses using retrieved context
* Supporting follow-up conversations through session memory
* Providing source citations for transparency and trust

The result: users can find information from enterprise documents instantly without manually searching through hundreds of pages.

---

## Innovation & Creativity

Enterprise RAG Assistant goes beyond a traditional chatbot by combining semantic retrieval with conversational memory.

Key innovations include:

* **Semantic Search:** Questions are matched based on meaning rather than exact keywords
* **Memory-Aware Retrieval:** Follow-up questions such as “What are their responsibilities?” are understood using previous conversation context
* **Grounded Responses:** Answers are generated only from retrieved document content, reducing hallucinations
* **Source Citations:** Every answer can be traced back to the document and page where the information originated
* **Incremental Indexing:** New documents can be added without rebuilding the entire knowledge base

This creates a more reliable and enterprise-friendly AI assistant compared to generic chatbots.

---

## Technical Complexity & Stack

Enterprise RAG Assistant combines document processing, semantic search, conversational memory, and large language models into a single workflow.

### Frontend

* Streamlit
* Custom responsive UI
* Real-time chat interface
* Source citation display
* Session-aware conversation history

### Backend

* Python
* LangChain
* SQLite Memory Store
* FAISS Vector Database
* Groq LLM API

### Document Processing

* PyPDFLoader
* Docx2txtLoader
* TextLoader
* RecursiveCharacterTextSplitter

### Embeddings & Retrieval

* BAAI/bge-small-en-v1.5
* FAISS Similarity Search
* Top-K Context Retrieval
* Metadata Preservation

### AI Generation

* Llama 3.1 8B Instant (Groq)
* Retrieval-Augmented Generation
* Grounded Prompting
* Citation-Based Responses

---

## System Architecture

```text
Document Upload
        ↓
Document Parsing
        ↓
Text Chunking
        ↓
Embedding Generation
        ↓
FAISS Vector Database
        ↓
User Question
        ↓
Semantic Retrieval
        ↓
Conversation Memory
        ↓
Llama 3.1 (Groq)
        ↓
Answer + Citations
```

---

## Usability & Impact

Enterprise RAG Assistant is designed to be simple, fast, and trustworthy.

Features include:

* Minimal setup and onboarding
* Natural language document search
* Transparent source citations
* Session-based conversational memory
* Support for multiple enterprise document formats

### Impact Potential

* Reduces time spent searching documents
* Improves knowledge accessibility across teams
* Enables faster onboarding and training
* Reduces dependency on manual documentation lookup
* Provides verifiable and traceable AI-generated responses

The platform transforms static enterprise documents into an interactive knowledge assistant.

---

## Key Features

### Document Management

* Upload PDF, DOCX, and TXT files
* Build searchable knowledge bases
* Incremental indexing support
* Document deletion and rebuild workflows

### Retrieval-Augmented Generation

* Semantic document retrieval
* Context-aware answer generation
* Source-grounded responses
* Hallucination reduction

### Conversational Memory

* Session-based memory
* Follow-up question understanding
* Context retention across conversations
* SQLite-backed persistence

### Source Transparency

* File-level citations
* Page-level references
* Source preview snippets
* Expandable citation cards

---

## Setup Instructions

### Prerequisites

* Python 3.9+
* Groq API Key

---

### Installation

```bash
git clone <repository_url>

cd enterprise-rag-assistant

python -m venv .venv

source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

### Run Application

```bash
streamlit run app.py
```

---

## Project Structure

```text
enterprise-rag-assistant/

├── app.py
├── rag_backend.py
├── memory.py
├── requirements.txt
├── README.md
├── .env.example
│
├── data/
│   ├── uploads/
│   ├── vectorstore/
│   └── chat_memory.db
│
├── docs/
│
└── tests/
```

---

## Future Improvements

* General Chat Mode
* Real-Time Web Search Integration
* LangGraph Tool Routing
* Multi-User Authentication
* OCR Support for Scanned PDFs
* Cloud Deployment
* Role-Based Access Control
* Hybrid Search (Keyword + Semantic)

---

*Built to transform enterprise documents into an intelligent, searchable, and conversational knowledge system.*
