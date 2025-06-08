# LLM-RAG: Retrieval-Augmented Generation Toolkit

This module provides a lightweight RAG (Retrieval-Augmented Generation) pipeline for configuration dependency analysis using LLMs and vector databases.

## Features

- **Document Chunking:** Supports `.md`, `.txt`, `.pdf` files, splits into manageable chunks.
- **Embeddings:** Integrates ZhipuAI, BGE, and HuggingFace embeddings.
- **Vector Database:** Stores and retrieves document vectors for similarity search.
- **RAG Pipeline:** Retrieves relevant context and queries LLMs (e.g., DeepSeek) for dependency extraction.
- **Batch Processing:** Processes configuration lists and outputs results to CSV.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare your API keys** in the code (see `component/llms.py`, `component/embedding.py`).

3. **Build vector database:**
   ```bash
   python quickstart.py
   ```

4. **Run RAG-based dependency extraction:**
   ```bash
   python RAGcompare.py
   ```

## File Structure

- `quickstart.py` – Build vector database from docs.
- `RAGcompare.py` – Main RAG pipeline for batch dependency extraction.
- `component/` – Embedding, vector DB, chunking, and LLM interface modules.

## Notes

- Results are saved in `./Comparative/Result/rag/`.
- Supports multi-software batch processing.
- Make sure your data and API keys are correctly set.
