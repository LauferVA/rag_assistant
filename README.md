Below is a **sample** updated `README.md` reflecting your new file parsing capabilities.  
(Feel free to adapt the language or formatting to suit your style and project needs.)

---

```markdown
# RAG Assistant

**RAG Assistant** is an entirely free, open, and local tool that retrieves and generates intelligent answers from a collection of files on your computer. Instead of a simple keyword search, it uses modern embedding and generation models to understand file content and produce detailed responses.

## Overview

- **Free**: This RAG implementation uses best-in-class free resources: **e5-large-v2** for embeddings and **Mistral-7B Instruct** (4-bit quantized) for generation.
- **Private**: Your data stay private and local—no external API calls.
- **Lightweight**: Designed for low-resource settings, works even with ~4 GB of GPU VRAM (or on CPU, albeit slower).
- **Expanded File Support**: Supports indexing of many file types (TXT, DOCX, PDF, Excel, etc.).  
- **Store Completions**: Use `rag_assistant.add_completion(answer)` to save helpful answers in your local index.
- **Efficient Re-indexing**: Automatically indexes new or updated files on each query.
- **Custom Instructions**: Append your own instructions (e.g. “Explain as if I'm a beginner”).

## How It Works

1. **Scanning Your Files**  
   The assistant automatically scans your specified directory for files (text, DOCX, PDF, Excel, etc.).  
2. **Extracting Text**  
   Specialized parsers attempt to extract textual content from each file. (See [Dependencies](#dependencies) for supported file types.)  
3. **Embedding**  
   Uses **e5-large-v2** (via `sentence-transformers`) to convert file contents into embeddings, enabling semantic similarity searches.  
4. **Retrieval + Generation**  
   When you query, the most relevant file snippets are retrieved using cosine similarity, and **Mistral-7B Instruct** generates an answer that blends the retrieved context with your question.

## Key Features

- **Automatic Updates**  
  Detects and indexes new or modified files every time you query.
- **Expanded File Support**  
  By default, text-based formats (`.txt`, `.md`, `.py`, `.json`...) are indexed. With optional libraries installed, you can also parse `.docx`, `.pdf`, `.xlsx`, `.odt`, `.ipynb`, etc.
- **Learning from Answers**  
  Use `add_completion()` to store especially helpful answers in a local `completions.txt`, making future searches more robust.
- **Local & Private**  
  All embeddings and model inference happens on your machine; nothing is sent to external servers.
- **Logging**  
  Detailed logging can be enabled with `logger_setup.setup_logger(...)`.

## Dependencies

The **core** dependencies are installed by default:

- [transformers](https://github.com/huggingface/transformers)
- [torch](https://pytorch.org/)
- [sentence-transformers](https://github.com/UKPLab/sentence-transformers)
- [numpy](https://numpy.org/)
- [tqdm](https://tqdm.github.io/)
- [bitsandbytes](https://github.com/TimDettmers/bitsandbytes)

### Optional File Parsers

If you want to parse advanced file types like DOCX, PDF, Excel, or ODT, install the corresponding extras (depending on how you configure `setup.py` or your environment):

- **DOCX**: `python-docx`
- **PDF**: Either `PyMuPDF` (`fitz`) or `PyPDF2`
- **Excel**: `openpyxl`
- **ODT**: `odfpy`
- **PPTX**: `python-pptx` (partial support)

You can install them individually, or if you have an `[parsers]` extra, do:
```bash
pip install .[parsers]
```
(Adjust the exact command based on your `setup.py` configuration.)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/rag_assistant.git
   cd rag_assistant
   ```
2. Install with pip:
   ```bash
   pip install .
   ```
3. (Optional) For parsing advanced file types:
   ```bash
   pip install .[parsers]
   ```
   or install each library individually (e.g., `pip install python-docx PyMuPDF openpyxl ...`).

## Example Usage

```python
from rag_assistant import RagAssistant
from rag_assistant.logger_setup import setup_logger
import logging

# Optionally, set up logging (logs to both the console and a file).
setup_logger(log_file="rag_assistant.log", level=logging.DEBUG)

# Initialize the assistant with your files directory.
assistant = RagAssistant(data_dir="/path/to/your/files")

# Optionally, set custom instructions.
assistant.set_instructions("Always provide concise and clear answers.")

# Ask a question. The assistant scans files, retrieves context, and generates an answer.
answer = assistant.query("How do I implement logging in Python?")
print("Answer:", answer)

# Save a particularly helpful completion so it is indexed for future queries.
assistant.add_completion(answer)
```

## Tips

- If you have hundreds of files, indexing can take a while initially. Subsequent queries will only re-index changed or newly added files.
- For best performance on PDF or DOCX documents, install the optional parsing libraries mentioned above.
- Make sure your GPU drivers and PyTorch setup are correct if you plan to use GPU acceleration for Mistral-7B Instruct.

## License

This project is released under the MIT License.  
See [LICENSE](LICENSE) for details.

Enjoy using **RAG Assistant** for offline retrieval-augmented generation! For feedback, open an issue or a pull request.  
Happy hacking!
```

---

### Explanation of Changes
1. **Expanded File Support**  
   The README now highlights you can parse `.docx`, `.pdf`, `.xlsx`, etc., by installing extra dependencies.  
2. **Installation Instructions**  
   We included a mention of the optional `[parsers]` dependency group if you use `extras_require` in `setup.py`.  
3. **Dependencies Section**  
   We added a new section explaining which libraries are needed for advanced file parsing.  
4. **Overall Flow**  
   Everything else—usage examples, disclaimers about local usage, licensing—remains consistent with the original readme approach.

Feel free to merge these edits into your existing README, adjusting style, formatting, or wording as needed.
