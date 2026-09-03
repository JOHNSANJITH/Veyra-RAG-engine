<div align="center">

# Veyra

### Hybrid Graph-RAG for Grounded Document Intelligence

Veyra is a multi-document question-answering and research assistant that combines dense retrieval, lexical search, graph expansion, reranking, and LLM generation to produce grounded answers with citations.

<p>
  <a href="https://github.com/JOHNSANJITH/Veyra-RAG-engine"><img src="https://img.shields.io/badge/GitHub-Veyra-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="https://github.com/JOHNSANJITH/Veyra-RAG-engine/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-2ea44f?style=for-the-badge" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Version-2.0-6f42c1?style=for-the-badge" alt="Version 2.0">
  <img src="https://img.shields.io/badge/Status-Active-1f883d?style=for-the-badge" alt="Active">
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Next.js-14-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=111111" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=flat-square&logo=javascript&logoColor=111111" alt="JavaScript">
  <img src="https://img.shields.io/badge/CSS-3-663399?style=flat-square&logo=css3&logoColor=white" alt="CSS">
  <img src="https://img.shields.io/badge/Qdrant-Vector_DB-DC244C?style=flat-square" alt="Qdrant">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
</p>

<p>
  <a href="#architecture">Architecture</a> ·
  <a href="#retrieval-pipeline">Retrieval</a> ·
  <a href="#evaluation">Evaluation</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#roadmap">Roadmap</a>
</p>

</div>

---

## Why Veyra?

Traditional vector RAG is strong at semantic similarity, but complex questions often depend on exact terminology, relationships between concepts, and information distributed across multiple sections.

Veyra explores a hybrid approach that combines three retrieval signals:

- **Dense retrieval** for semantic similarity
- **BM25** for exact and lexical matching
- **Concept graphs** for contextual expansion across related sections

A reranking stage then refines the candidate set before context is assembled for the LLM.

The goal is simple:

> **Retrieve better evidence before asking the model to generate an answer.**

---

##  Features

| Capability | What Veyra does |
| --- | --- |
|  Document ingestion | Upload and process PDF documents into a searchable corpus |
|  Dense retrieval | Sentence-transformer embeddings with vector search |
|  Lexical retrieval | BM25 keyword matching for exact terminology |
|  Graph retrieval | Concept co-occurrence expansion across related chunks |
|  Reranking | Cross-encoder reranking of retrieved candidates |
|  Conversational QA | Short-term memory for multi-turn interactions |
|  Query rewriting | Reformulates follow-up questions using conversation context |
|  Citations | Returns grounded source references with generated answers |
|  Evaluation | Retrieval metrics and baseline/ablation experiments |
|  Deployment | Docker-ready backend with separate Next.js frontend |

---

##  Architecture

```text
                         ┌───────────────────┐
                         │    PDF Documents  │
                         └─────────┬─────────┘
                                   │
                                   ▼
                     ┌─────────────────────────┐
                     │  Parsing / Cleaning     │
                     │  Chunking / Metadata    │
                     └────────────┬────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
        ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐
        │  Embeddings  │  │    BM25      │  │ Concept Graph   │
        │  + Qdrant    │  │    Index     │  │ + Expansion     │
        └──────┬───────┘  └──────┬───────┘  └────────┬────────┘
               │                 │                   │
               └─────────────────┼───────────────────┘
                                 ▼
                      ┌───────────────────────┐
                      │ Hybrid Retrieval      │
                      │ + Candidate Merging   │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │ Cross-Encoder         │
                      │ Reranking             │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │ Context Assembly      │
                      │ + Prompt Construction │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │ LLM Generation        │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │ Answer + Citations    │
                      └───────────────────────┘
