# RAG Assistant

**RAG Assistant** is an entirely free, open, and local tool that retrieves and generates intelligent answers from a collection of text files on your computer. Instead of a simple keyword search, it uses modern 
embedding and generation models to understand file content and produce detailed responses.

## Overview (more detail below):
- Free: This RAG implementation uses best-in-class free resources: e5-large-v2 for embedding and Mistral-7B Instruct for generation.
- Private: Your data stay private and local!
- GPU requirements: It is designed for low resource settings, and will run on as little as 4Gb VRAM.
- Store helpful completions for later retrieval with `rag_assistant.add_completion`
- Efficient re-indexing: Automated, indexing and re-indexing of only files that are altered.
- Supports custom instructions


## How It Works

- **Scanning Your Files:** Automatically scans a specified directory for text files (e.g., `.txt`, `.md`, `.py`, etc.).
- **Understanding the Content:** Uses the **e5-large-v2** embedding model (via SentenceTransformers) to convert file contents into embeddings and to compute query similarity.
- **Generating Answers:** Leverages **Mistral-7B Instruct** (quantized to 4‑bit for optimal performance on systems with ~4 GB VRAM) to generate answers that combine retrieved context 
with your query.

## Key Features

- **Automatic Updates:** Detects and indexes new or modified files every time you query.
- **Learning from Its Own Answers:** Use `rag_assistant.add_completion` to save particularly helpful answers. These completions are added to the file index so that similar future 
queries can benefit.
- **Custom Instructions:** Specify custom instructions (e.g., “explain things like I’m a beginner”) that are prepended to every query.
- **Free and Runs Locally:** Your data stays on your machine.
- **Activity Logs:** Detailed logging is available to help troubleshoot any issues.

## Usage Notes

- **Maximum Directory Size:** This version is optimized for directories containing up to about **1000 files** or roughly **100MB** of text data. Larger directories may result in 
slower performance.
- **Machine Specifications:** Running the default Mistral-7B Instruct model (4‑bit quantized) is recommended on a machine with at least **8GB RAM** and a GPU with at least **4GB 
VRAM** (CPU fallback is supported but will be slower).
- **Dependencies:** Requires Python 3.7 or higher along with `transformers`, `torch`, `sentence-transformers`, `numpy`, `tqdm`, and `bitsandbytes`.

## Installation

Run the following command in the directory containing `setup.py`:

```bash
pip install .
```

## Example Usage

```python
from rag_assistant import RagAssistant
from rag_assistant.logger_setup import setup_logger

# Optionally, set up logging (logs to both the console and a file)
setup_logger(log_file="rag_assistant.log", level=logging.DEBUG)

# Initialize the assistant with your text files directory.
assistant = RagAssistant(data_dir="/path/to/your/text/files")

# Optionally, set custom instructions.
assistant.set_instructions("Always provide concise and clear answers.")

# Ask a question. The assistant scans files, retrieves relevant context, and generates an answer.
answer = assistant.query("How do I implement logging in Python?")
print("Answer:", answer)

# Save a particularly helpful completion so it is indexed for future queries.
assistant.add_completion(answer)
```

Enjoy!
