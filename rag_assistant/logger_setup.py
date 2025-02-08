import logging

def setup_logger(log_file=None, level=logging.INFO):
    """
    Configure logging for RAG Assistant.
    
    :param log_file: Optional file path to log messages.
    :param level: Logging level (e.g., logging.INFO).
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console handler.
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File handler, if requested.
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

