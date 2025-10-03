import os

def _expand(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))

# Base folder to watch (env var: WATCH_FOLDER)
WATCH_FOLDER = _expand(os.getenv("WATCH_FOLDER", "~/Downloads"))

# Derived folders from WATCH_FOLDER
IMAGES_FOLDER = _expand(os.path.join(WATCH_FOLDER, "Images"))
DOCUMENTS_FOLDER = _expand(os.path.join(WATCH_FOLDER, "Documents"))
INSTALLERS_FOLDER = _expand(os.path.join(WATCH_FOLDER, "Installers"))
ARCHIVES_FOLDER = _expand(os.path.join(WATCH_FOLDER, "Archives"))
MEDIA_FOLDER = _expand(os.path.join(WATCH_FOLDER, "Media"))
MISC_FOLDER = _expand(os.path.join(WATCH_FOLDER, "Misc"))
ORGANIZE_RULES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".ico", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Installers": [".exe", ".dmg", ".pkg", ".deb", ".rpm", ".msi", ".app"],
    "Archives": [".zip", ".tar", ".gz", ".bz2", ".rar", ".7z"],
    "Media": [".mp3",".mp4",".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma", ".aiff", ".m4b", ".m4p", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b", ".m4r", ".m4v", ".m4p", ".m4b"]
}
