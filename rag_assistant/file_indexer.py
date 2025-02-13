# rag_assistant/file_indexer.py

import os
import logging
import numpy as np
from sentence_transformers import SentenceTransformer

from . import file_parsers  # Import our new parser module

logger = logging.getLogger(__name__)

class FileIndexer:
    def __init__(
        self,
        data_dir,
        max_file_size=5 * 1024 * 1024,  # Default: skip files >5MB
        model_name="intfloat/e5-large-v2",
    ):
        """
        A more advanced FileIndexer that can parse multiple file types,
        skipping files that are too large or not supported.
        
        :param data_dir: Directory to index.
        :param max_file_size: Maximum file size (in bytes) to index.
        :param model_name: Hugging Face model for embeddings (default: e5-large-v2).
        """
        self.data_dir = data_dir
        self.max_file_size = max_file_size
        self.index = {}  # { filepath: {"content": str, "embedding": np.array} }
        self.embedder = SentenceTransformer(model_name)

    def update_index(self):
        """
        Walk through the data_dir, parse and embed allowed files, store in self.index.
        """
        self.index = {}

        # Common file extensions to parse. Adjust as needed.
        allowed_extensions = (
            ".txt", ".md", ".py", ".json", ".log", ".csv", ".tsv",
            ".docx", ".doc", ".pdf", ".rtf", ".odt", ".xls", ".xlsx", ".xlsm", ".ods",
            ".ppt", ".pptx", ".odp", ".ipynb", ".xml", ".yaml", ".yml",
            ".html", ".htm", ".css", ".js", ".jsx", ".ts", ".tsx",
            ".sh", ".cmd", ".ps1", ".swift", ".kt", ".go", ".rs", ".lua",
            ".pl", ".r", ".m", ".vb", ".cs", ".asm", ".dart", ".php", ".rb", ".sql"
        )

        for root, dirs, files in os.walk(self.data_dir):
            for file_name in files:
                ext = os.path.splitext(file_name)[1].lower()
                if ext not in allowed_extensions:
                    # Skip unsupported extensions.
                    continue

                filepath = os.path.join(root, file_name)

                # Check file size
                try:
                    size = os.path.getsize(filepath)
                    if size > self.max_file_size:
                        logger.debug("Skipping large file %s (size %d bytes)", filepath, size)
                        continue
                except Exception as e:
                    logger.error("Error checking size of %s: %s", filepath, e)
                    continue

                # Extract text
                content = file_parsers.extract_text_from_file(filepath)
                if not content.strip():
                    # If no text was extracted or empty
                    logger.debug("No text extracted from %s; skipping embedding.", filepath)
                    continue

                # Compute embedding
                try:
                    embedding = self.embedder.encode(content, convert_to_numpy=True)
                    self.index[filepath] = {"content": content, "embedding": embedding}
                    logger.debug("Indexed file: %s", filepath)
                except Exception as e:
                    logger.error("Error embedding file %s: %s", filepath, e)

        logger.info("Indexed %d files.", len(self.index))

    def cosine_similarity(self, vec1, vec2):
        """Compute the cosine similarity between two vectors."""
        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def search(self, query, top_n=3):
        """
        Search for relevant files using cosine similarity between the query embedding and file embeddings.

        :param query: The search query string.
        :param top_n: Number of top matches to return.
        :return: List of tuples: (filepath, similarity_score, content).
        """
        query_embedding = self.embedder.encode(query, convert_to_numpy=True)
        results = []

        for filepath, data in self.index.items():
            file_embedding = data["embedding"]
            score = self.cosine_similarity(query_embedding, file_embedding)
            if score > 0:
                results.append((filepath, score, data["content"]))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]
