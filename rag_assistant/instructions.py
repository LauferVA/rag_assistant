import os
import logging

logger = logging.getLogger(__name__)

def save_instructions(filepath, instructions):
    """
    Save custom instructions to a file.
    
    :param filepath: Path to the instructions file.
    :param instructions: The instruction text.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(instructions)
        logger.info("Saved instructions to %s", filepath)
    except Exception as e:
        logger.error("Error saving instructions to %s: %s", filepath, e)

def load_instructions(filepath):
    """
    Load instructions from a file.
    
    :param filepath: Path to the instructions file.
    :return: Instruction text if available; otherwise, default instructions.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                instructions = f.read()
            logger.info("Loaded instructions from %s", filepath)
            return instructions
        except Exception as e:
            logger.error("Error loading instructions from %s: %s", filepath, e)
            return "Provide a helpful answer."
    else:
        logger.info("No instructions file found at %s. Using default instructions.", filepath)
        return "Provide a helpful answer."

