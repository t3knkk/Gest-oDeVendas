import logging
from datetime import datetime

def setup_logger():
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        filename='error.log',
        level=logging.ERROR,
        format=log_format,
        filemode='a'
    )

def log_error(exception):
    """
    Registra uma exceção no arquivo de log.
    
    Args:
        exception (Exception): A exceção que foi capturada.
    """

    logging.error(f"An exception occurred: {exception}", exc_info=True)
