#!/usr/bin/env python3
"""
File watcher for monitoring a folder.
"""

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logger import setup_logging
from classifier import FileClassifier
from file_mover import FileMover

class FilesWatcher(FileSystemEventHandler):
    """
    File system event handler for monitoring a folder.
    """
    
    def __init__(self, folder_path, logger=None):
        """
        Initialize the watcher with the folder path.
        
        Args:
            folder_path (str): Path to the folder
            logger: Logger instance to use for logging
        """
        self.folder_path = Path(folder_path)
        self.logger = logger or setup_logging()
        self.classifier = FileClassifier()
        self.file_mover = FileMover()
        self.logger.info(f"Initialized Folder watcher for: {self.folder_path}")
    
    def on_created(self, event):
        """
        Called when a file or directory is created.
        """
        self.logger.debug("Created event detected")
        if not event.is_directory:
            file_path = Path(event.src_path)
            self.logger.info(f"New file created: {file_path.name}")
            self.logger.info(f"Full path: {file_path}")
            self.logger.info(f"File size: {file_path.stat().st_size} bytes")
            classification = self.classifier.classify(file_path)
            self.logger.info(f"File classification: {classification}")
            if classification == 'Documents' and file_path.suffix.lower() == '.pdf':
                subcategory = self.classifier.read_and_classify(file_path)
                moved = self.file_mover.move_document_to_subcategory(file_path, subcategory)
                if moved:
                    if subcategory:
                        self.logger.info(f"Moved PDF to Documents/{subcategory}")
                    else:
                        self.logger.info("Moved PDF to Documents (no subcategory)")
                else:
                    self.logger.warning("Move failed for PDF document")
            else:
                if classification:
                    moved = self.file_mover.move_file(file_path, classification)
                    if moved:
                        self.logger.info(f"Moved new file to {classification}")
                    else:
                        self.logger.warning("Move failed for new file")
            

    
    def on_modified(self, event):
        """
        Called when a file or directory is modified.
        """
        self.logger.debug("Modified event detected")
        if not event.is_directory:
            file_path = Path(event.src_path)
            self.logger.info(f"File modified: {file_path.name}")
            

    
    def on_moved(self, event):
        """
        Called when a file or directory is moved or renamed.
        """
        self.logger.debug("Moved event detected")
        if not event.is_directory:
            old_path = Path(event.src_path)
            new_path = Path(event.dest_path)
            self.logger.info(f"File moved/renamed: {old_path.name} -> {new_path.name}")

def start_watching(folder_path, logger=None):
    """
    Start watching the folder for changes.

    Args:
        folder_path (str): Path to the folder
        logger: Logger instance to use for logging
    """
    if logger is None:
        logger = setup_logging()
    
    logger.info(f"Folder path: {folder_path}")
    
    # Create event handler and observer
    event_handler = FilesWatcher(folder_path, logger)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    
    # Start the observer
    observer.start()
    logger.info("File watcher started. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("File watcher stopped.")
    
    observer.join()