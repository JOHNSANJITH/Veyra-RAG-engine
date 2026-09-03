---
title: Veyra Backend
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Veyra

**Hybrid Graph-Augmented Retrieval-Augmented Generation System**

Veyra is an engineering-focused document summarization and question-answering system that combines vector search, graph-based reasoning, and LLM-based generation to provide grounded, citation-aware responses over uploaded documents.

The system extends traditional vector retrieval with concept co-occurrence graphs, enabling contextual expansion for complex queries that require information from multiple sections of a document.

**Demo:** Add the deployed frontend URL here when a public deployment is available.

---

## Features

- **PDF Upload & Ingestion** – Document processing and indexing
- **Hybrid Retrieval Pipeline**
  - Dense vector similarity search
  - BM25 keyword search
  - Concept co-occurrence graph expansion
- **Unified Chat Interface** – Question answering and document summarization
- **Citation-Aware Responses** – Grounded answers with source attribution
- **Conversation Memory** – Short-term context retention across turns
- **Query Rewriting** – Context-aware reformulation using conversation history
- **Token Limit Protection** – Document size validation and context control
- **Evaluation Framework** – Retrieval quality assessment
- **Ablation Studies** – Baseline comparisons and retrieval experiments

---

## System Architecture

```text
PDF Document
     |
     v
Chunking & Parsing
     |
     +----------------------+----------------------+
     |                                             |
     v                                             v
Embeddings Generation                       Concept Extraction
     |                                             |
     v                                             v
Vector Index                                Co-occurrence Graph
     |                                             |
     +----------------------+----------------------+
                            |
                            v
                   Hybrid Graph-RAG Retrieval
                            |
                            v
              Context Assembly & Prompt Construction
                            |
                            v
                       LLM Generation
                            |
                            v
                     Answer + Citations
```

---

## Retrieval Strategy

Veyra employs a three-stage hybrid retrieval pipeline.

### 1. Vector Search

Dense embeddings using sentence-transformer models for semantic similarity.

### 2. Lexical Search

BM25 scoring for keyword-based anchoring and exact term matching.

### 3. Graph Expansion

- **Nodes:** Extracted concepts from document chunks
- **Edges:** Co-occurrence relationships within the corpus
- **Purpose:** Expand retrieval toward conceptually related sections

The graph augments rather than replaces traditional vector retrieval, providing additional structural context for multi-section queries. The graph is maintained incrementally during ingestion and cleaned when documents are removed.

---

## Evaluation

### Evaluation Corpus

The initial evaluation corpus uses:

**"Attention Is All You Need"**

by Vaswani et al.

The corpus provides:

- Dense technical terminology
- Cross-section conceptual dependencies
- Well-defined technical concepts
- Questions requiring multi-section retrieval

### Query Types

#### Localized Queries

Single-concept retrieval.

Example:

> "What is scaled dot-product attention?"

#### Distributed Queries

Multi-section synthesis.

Example:

> "How does self-attention replace recurrence and convolution?"

#### Comparative Queries

Cross-concept analysis.

Example:

> "Compare encoder, decoder, and encoder-decoder architectures."

### Metrics

- **Hit@5** – Percentage of queries with at least one relevant page retrieved
- **Coverage** – Number of unique relevant pages retrieved
- **Diversity** – Fraction of unique pages in the retrieved set

---

## Results

### Baseline Comparison: Vector Search vs. Hybrid Graph-RAG

The current evaluation compares vector-only retrieval against hybrid retrieval with graph expansion.

**Observed findings:**

- Hit@5 reached 1.00 across the evaluated query set
- Vector-only and hybrid retrieval produced comparable retrieval quality
- Graph expansion occasionally surfaced conceptually adjacent sections
- No degradation was observed in the current evaluation corpus

These results are corpus-specific and should be interpreted as an initial evaluation rather than a universal benchmark.

### Ablation Study

The graph component is evaluated using two configurations:

- **Vector Only**
- **Vector + Graph Expansion**

The ablation study measures whether graph augmentation changes recall, coverage, and diversity.

---

## Conversation Memory & Query Rewriting

- **Short-term memory** maintains recent conversation turns
- **Context-aware rewriting** reformulates follow-up queries using chat history
- Enables conversational interaction without directly polluting the retrieval query

---

## Tech Stack

### Backend

- Python
- FastAPI
- LangChain
- Qdrant / Vector Store
- NetworkX
- BM25
- Sentence Transformers
- Groq / OpenAI-compatible LLM APIs

### Frontend

- Next.js
- React
- Modern chat-style interface
- PDF upload interface
- Glassmorphism design system

### Development & Deployment

- Ruff
- Pre-commit hooks
- Docker
- GitHub Actions
- Hugging Face Spaces
- Vercel

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Clone Repository

```bash
git clone https://github.com/JOHNSANJITH/veyra-rag-engine.git
cd veyra-rag-engine
```

### Backend Setup

```bash
cd backend
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

### Frontend Setup

Open a second terminal:

```bash
cd frontend
npm install
```

Create the local environment file:

```bash
copy .env.example .env.local
```

On Linux/macOS:

```bash
cp .env.example .env.local
```

Run the frontend:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```

---

## Code Quality

Veyra uses automated code-quality tooling.

### Install Pre-commit Hooks

```bash
pre-commit install
```

### Format & Lint

```bash
ruff check .
ruff format .
```

---

## Docker

Build the image:

```bash
docker build -t veyra .
```

Run the container:

```bash
docker run -p 8000:8000 veyra
```

---

## Project Structure

```text
veyra-rag-engine/
|
+-- backend/
|   +-- app/
|       +-- api/
|       +-- core/
|       +-- evaluation/
|       +-- ingestion/
|       +-- memory/
|       +-- models/
|       +-- retrieval/
|
+-- frontend/
|
+-- .github/
|   +-- workflows/
|
+-- Dockerfile
+-- pyproject.toml
+-- requirements.txt
+-- .gitignore
+-- LICENSE
+-- README.md
```

---

## Deployment

The application is designed to support separate frontend and backend deployments.

### Frontend

The Next.js frontend can be deployed using Vercel.

### Backend

The FastAPI backend can be deployed using Hugging Face Spaces or another container-compatible platform.

Production URLs should be added here after the Veyra deployments are created.

Binary document files are excluded from version control and handled at runtime.

---

## Roadmap

- [ ] Improve hybrid retrieval weighting
- [ ] Add advanced reranking
- [ ] Improve graph construction
- [ ] Expand retrieval evaluation
- [ ] Add answer-quality evaluation
- [ ] Add hallucination detection
- [ ] Add retrieval latency monitoring
- [ ] Add token and cost tracking
- [ ] Add streaming responses
- [ ] Improve document parsing
- [ ] Support multiple knowledge bases
- [ ] Add authentication and user management
- [ ] Add production monitoring
- [ ] Expand automated CI/CD deployment

---

## Project Goals

Veyra explores modern retrieval-augmented generation systems from an engineering perspective.

The project focuses on combining information retrieval, graph reasoning, natural language processing, and large language models into a grounded document intelligence system.

The main areas of focus are:

```text
Information Retrieval
        +
Natural Language Processing
        +
Graph Reasoning
        +
Large Language Models
        +
Backend Engineering
        +
Evaluation
        +
Deployment
```

---

## Author

**JOHN SANJITH**

GitHub: [@JOHNSANJITH](https://github.com/JOHNSANJITH)

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome.

Please feel free to submit a pull request or open an issue for improvements and suggestions.

---

## Contact

For questions, feedback, or collaboration opportunities, please open an issue on the GitHub repository.
