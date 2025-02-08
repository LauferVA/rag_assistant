import os
import logging
from sentence_transformers import SentenceTransformer
import numpy as np

logger = logging.getLogger(__name__)

class FileIndexer:
    def __init__(self, data_dir):
        """
        Initialize the indexer with a directory path and the e5-large-v2 embedding model.
        """
        self.data_dir = data_dir
        self.index = {}  # Mapping from file path to a dict with content and embedding
        # Initialize the embedding model
        self.embedder = SentenceTransformer("intfloat/e5-large-v2")

    def update_index(self):
        """Scan the directory (and subdirectories) for text files and update the index."""
        self.index = {}
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith(('.txt', '.md', '.py', '.json', '.log')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                        # Compute embedding for the file content
                        embedding = self.embedder.encode(content, convert_to_numpy=True)
                        self.index[filepath] = {"content": content, "embedding": embedding}
                        logger.debug("Indexed file: %s", filepath)
                    except Exception as e:
                        logger.error("Error reading file %s: %s", filepath, e)
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
        Search for relevant files using cosine similarity between query and file embeddings.
        
        :param query: The search query string.
        :param top_n: The maximum number of files to return.
        :return: A list of tuples (filepath, similarity score, content) sorted by relevance.
        """
        query_embedding = self.embedder.encode(query, convert_to_numpy=True)
        results = []
        for filepath, data in self.index.items():
            content = data["content"]
            file_embedding = data["embedding"]
            score = self.cosine_similarity(query_embedding, file_embedding)
            if score > 0:
                results.append((filepath, score, content))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]
