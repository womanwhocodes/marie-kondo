import os
from typing import Optional

from config import ORGANIZE_RULES, DOCUMENTS_FOLDER
from logger import setup_logging

try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # Defer import errors until method use

 


class FileClassifier:
    """
    File classifier that uses ORGANIZE_RULES from config.py to classify files.
    """
    def __init__(self, logger=None):
        self.logger = logger or setup_logging()
        self.logger.info("FileClassifier initialized")
        # Initialize OpenAI client lazily when needed
        self._openai_client = None

    def classify(self, file_path):
        """
        Classify the file based on ORGANIZE_RULES from config.py.
        Args:
            file_path (str or Path): Path to the file
        Returns:
            str: Classification label
        """
        from pathlib import Path
        self.logger.debug(f"Starting classification for file: {file_path}")
        
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"File does not exist: {file_path}")
                return 'Misc'
            
            ext = file_path.suffix.lower()
            self.logger.debug(f"File extension detected: {ext}")
            
            for category, extensions in ORGANIZE_RULES.items():
                if ext in extensions:
                    self.logger.info(f"File {file_path.name} classified as {category} (extension: {ext})")
                    return category
            
            self.logger.info(f"File {file_path.name} classified as Misc (no matching extension: {ext})")
            return 'Misc'
            
        except Exception as e:
            self.logger.error(f"Error during classification of {file_path}: {str(e)}")
            return 'Misc'


    def _ensure_openai_client(self):
        """
        Ensure an OpenAI client is available when needed.
        """
        if self._openai_client is None:
            if OpenAI is None:
                raise RuntimeError("OpenAI SDK not installed. Please install 'openai' package.")
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY is not set in the environment.")
            self._openai_client = OpenAI()
        return self._openai_client

    def read_and_classify(self, file_path) -> Optional[str]:
        """
        If the file is a PDF, upload it to OpenAI Files API and request a subcategory
        suitable for organizing the document. The model is instructed to choose one of
        the existing folders in the Downloads directory if it is a good match; only
        if none of them match should it propose a new one-word subcategory.

        Args:
            file_path (str or Path): Path to the PDF file

        Returns:
            Optional[str]: one-word subcategory or None
        """
        from pathlib import Path
        import re
        import json

        try:
            file_path = Path(file_path)
            if not file_path.exists() or file_path.suffix.lower() != ".pdf":
                return None

            client = self._ensure_openai_client()

            # Gather existing folder names in the Downloads/Documents directory
            try:
                existing_folders = [
                    entry.name for entry in os.scandir(DOCUMENTS_FOLDER) if entry.is_dir()
                ]
            except Exception:
                existing_folders = []

            self.logger.info(f"Existing folders: {existing_folders}")
            
            # Upload the PDF to Files API
            with open(file_path, "rb") as f:
                uploaded = client.files.create(file=f, purpose="assistants")

            existing_folders_json = json.dumps(existing_folders)
            prompt = (
                "You are organizing a PDF into a document subcategory. "
                "First, consider the existing folders in the user's Downloads/Documents directory. "
                f"existing_folders = {existing_folders_json}. "
                "If one of these existing folder names is a good fit, return EXACTLY that folder name. "
                "If none of them is appropriate, return a NEW one-word lowercase subcategory such as "
                "'finance', 'tax', 'legal', 'invoice', 'receipt', 'insurance', 'education', 'medical', 'travel'. "
                "Respond with ONLY the chosen subcategory string (no quotes, no punctuation, no explanation)."
            )

            # Ask the model to classify using the uploaded file
            response = client.responses.create(
                model="gpt-4o-mini",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt},
                            {"type": "input_file", "file_id": uploaded.id},
                        ],
                    }
                ],
            )

            # Extract plain text output
            try:
                text = response.output_text  # available in newer SDKs
            except Exception:
                # Fallback extraction for SDKs without output_text helper
                text = ""
                try:
                    outputs = getattr(response, "output", []) or getattr(response, "outputs", [])
                    if outputs:
                        first = outputs[0]
                        content = getattr(first, "content", [])
                        if content and getattr(content[0], "type", "") in ("output_text", "text"):
                            text = getattr(content[0], "text", "")
                except Exception:
                    text = ""

            candidate_raw = (text or "").strip()
            # Build a normalizer that matches our sanitization rules for comparison
            def normalize(name: str) -> str:
                name = name.strip().lower()
                name = re.sub(r"[^a-z0-9]+", "-", name)
                name = re.sub(r"-+", "-", name).strip('-')
                return name

            candidate_norm = normalize(candidate_raw)
            if not candidate_norm:
                return None

            # Prefer an exact match to an existing folder (case-insensitive / normalized)
            normalized_map = {normalize(x): x for x in existing_folders}
            if candidate_norm in normalized_map:
                return normalized_map[candidate_norm]

            # Otherwise, treat as a new (sanitized) one-word/phrase (hyphenated) subcategory
            return candidate_norm or None

        except Exception as e:
            # Likely password-protected or unreadable, or API error
            self.logger.warning(f"PDF classify failed for {file_path}: {type(e).__name__}: {str(e)}")
            return None
