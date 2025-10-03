#!/usr/bin/env python3
"""
File mover for organizing files into category folders.
"""

import shutil
from pathlib import Path
from config import (
    IMAGES_FOLDER, DOCUMENTS_FOLDER, INSTALLERS_FOLDER, 
    ARCHIVES_FOLDER, MEDIA_FOLDER, MISC_FOLDER
)
from logger import setup_logging

class FileMover:
    """
    Handles moving files to their appropriate category folders.
    """
    
    def __init__(self, logger=None):
        """
        Initialize the file mover.
        
        Args:
            logger: Logger instance to use for logging
        """
        self.logger = logger or setup_logging()
        self.category_folders = {
            "Images": IMAGES_FOLDER,
            "Documents": DOCUMENTS_FOLDER,
            "Installers": INSTALLERS_FOLDER,
            "Archives": ARCHIVES_FOLDER,
            "Media": MEDIA_FOLDER,
            "Misc": MISC_FOLDER
        }
        self._ensure_folders_exist()
    
    def _ensure_folders_exist(self):
        """
        Create category folders if they don't exist.
        """
        for folder_path in self.category_folders.values():
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Ensured folder exists: {folder_path}")
    
    def move_file(self, file_path, classification):
        """
        Move a file to its appropriate category folder.
        
        Args:
            file_path (str or Path): Path to the file to move
            classification (str): Classification category of the file
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        self.logger.info(f"Moving file: {file_path} to {classification}")
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                self.logger.error(f"File does not exist: {file_path}")
                return False
            
            # Get destination folder
            dest_folder = self.category_folders.get(classification)
            if not dest_folder:
                self.logger.error(f"Unknown classification: {classification}")
                return False
            
            dest_path = Path(dest_folder) / file_path.name
            
            # Handle filename conflicts
            dest_path = self._get_unique_filename(dest_path)
            
            # Move the file
            shutil.move(str(file_path), str(dest_path))
            
            self.logger.info(f"Moved {file_path.name} to {dest_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error moving file {file_path}: {str(e)}")
            return False

    def move_document_to_subcategory(self, file_path, subcategory: str | None) -> bool:
        """
        Move a document to a subcategory under DOCUMENTS_FOLDER when provided.
        If subcategory is None, move directly into DOCUMENTS_FOLDER.

        Args:
            file_path (str or Path): Path to the file
            subcategory (str | None): one-word subcategory

        Returns:
            bool: True if move succeeded
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"File does not exist: {file_path}")
                return False

            if subcategory:
                dest_folder = Path(DOCUMENTS_FOLDER) / subcategory.lower()
            else:
                dest_folder = Path(DOCUMENTS_FOLDER)

            dest_folder.mkdir(parents=True, exist_ok=True)
            dest_path = dest_folder / file_path.name
            dest_path = self._get_unique_filename(dest_path)
            shutil.move(str(file_path), str(dest_path))
            self.logger.info(f"Moved {file_path.name} to {dest_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error moving document {file_path}: {str(e)}")
            return False
    
    def _get_unique_filename(self, dest_path):
        """
        Generate a unique filename if the destination already exists.
        
        Args:
            dest_path (Path): Original destination path
            
        Returns:
            Path: Unique destination path
        """
        if not dest_path.exists():
            return dest_path
        
        counter = 1
        while True:
            stem = dest_path.stem
            suffix = dest_path.suffix
            new_name = f"{stem}_{counter}{suffix}"
            new_path = dest_path.parent / new_name
            
            if not new_path.exists():
                return new_path
            
            counter += 1 