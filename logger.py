#!/usr/bin/env python3
"""
Logging configuration for the marie-kondo application.
"""

import logging
import os
from datetime import datetime

def setup_logging():
    """
    Configure logging with both file and console handlers.
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create a unique log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'logs/mk_{timestamp}.log'
    
    # Configure logging format to include file, function and line number
    log_format = '%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s'

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(log_format)

    if not root_logger.handlers:
        file_handler = logging.FileHandler(log_filename)
        stream_handler = logging.StreamHandler()
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(stream_handler)
    else:
        # Ensure existing handlers use the new formatter
        for handler in root_logger.handlers:
            handler.setFormatter(formatter)

    return logging.getLogger(__name__)
