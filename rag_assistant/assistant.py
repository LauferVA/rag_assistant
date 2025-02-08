import os
import logging
from .file_indexer import FileIndexer
from .llm_helper import generate_completion
from .instructions import load_instructions, save_instructions

logger = logging.getLogger(__name__)

class RagAssistant:
    def __init__(self, data_dir, instructions_file=None):
        """
        Initialize the RAG Assistant with a directory to scan.
        
        :param data_dir: Path to the directory containing text files.
        :param instructions_file: (Optional) File path for custom instructions.
        """
        self.data_dir = data_dir
        self.indexer = FileIndexer(data_dir)
        self.instructions_file = instructions_file or os.path.join(data_dir, "instructions.txt")
        self.instructions = load_instructions(self.instructions_file)
        # Build initial index
        self.indexer.update_index()
        logger.info("RagAssistant initialized with data directory: %s", data_dir)

    def update_index(self):
        """Update the file index by scanning the data directory."""
        self.indexer.update_index()
        logger.info("File index updated.")

    def query(self, question, top_n=3):
        """
        Query the assistant with a question.
        It retrieves context from relevant files and uses the LLM to generate an answer.
        
        :param question: The question string.
        :param top_n: Number of top matching files to include in the context.
        :return: The generated answer.
        """
        self.update_index()  # Ensure index is fresh
        logger.info("Received query: %s", question)
        results = self.indexer.search(query=question, top_n=top_n)
        context_texts = []
        for filepath, score, content in results:
            logger.debug("File: %s, Score: %s", filepath, score)
            context_texts.append(f"File: {filepath}\nContent:\n{content}")
        context = "\n\n".join(context_texts)
        prompt = (
            f"Instructions: {self.instructions}\n\n"
            f"Context: {context}\n\n"
            f"Question: {question}\nAnswer:"
        )
        logger.debug("Generated prompt for LLM: %s", prompt)
        answer = generate_completion(prompt)
        logger.info("Generated answer: %s", answer)
        return answer

    def add_completion(self, completion_text, filename="completions.txt"):
        """
        Save the provided completion text to a file in the data directory and update the index.
        This lets the assistant “learn” from particularly helpful answers.
        
        :param completion_text: The completion text provided by the LLM.
        :param filename: The file name where completions are stored (default: completions.txt).
        """
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(completion_text + "\n")
            logger.info("Added completion to %s", filepath)
        except Exception as e:
            logger.error("Error writing completion to %s: %s", filepath, e)
        # Rebuild the index so that the new completion is searchable
        self.indexer.update_index()

    def set_instructions(self, instruction_text):
        """
        Set custom instructions for the assistant.
        
        :param instruction_text: A string with your desired instructions.
        """
        self.instructions = instruction_text
        save_instructions(self.instructions_file, instruction_text)
        logger.info("Custom instructions updated.")
