#!/usr/bin/env python3
"""
Main entry point for the marie-kondo application.
"""

 
from logger import setup_logging
from config import WATCH_FOLDER
from file_watcher import start_watching

def main():
    """
    Main function that serves as the entry point for the application.
    """
    # Setup logging
    logger = setup_logging()
    
    logger.info("Starting marie-kondo application...")
    print("Application started successfully.")
    print("Marie Kondo is working...")

    start_watching(WATCH_FOLDER, logger)
    
    try:
        # TODO: Add your application logic here
        logger.info("Application logic completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1
    
    logger.info("Application finished successfully")
    return 0

if __name__ == "__main__":
    main()
