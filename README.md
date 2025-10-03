## Smart Downloads Organizer

Rule-based file organizer that watches a folder (e.g., your `Downloads`) and moves files into category folders like `Images`, `Documents`, `Installers`, `Archives`, `Media`, and `Misc`. PDFs can optionally be sub-categorized using OpenAI.

### Requirements
- Python 3.8+
- macOS, Linux, or Windows

### 1) Setup (virtual environment recommended)
```bash
cd (your marie-kondo project directory)
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
# Optional: for PDF subcategory classification
pip install openai
```

### 2) Configure
Set the base folder to watch via the `WATCH_FOLDER` environment variable (defaults to `~/Downloads`).
All category folders are derived under this base automatically (`Images`, `Documents`, `Installers`, `Archives`, `Media`, `Misc`).
```bash
export WATCH_FOLDER="$HOME/Downloads"
```

Optional (PDF classification): set your OpenAI API key if you want PDFs to be auto sub-categorized under `Documents/<subcategory>`.
```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 3) Run
```bash
python main.py
```
- The watcher starts and logs to console and `logs/mk_<timestamp>.log`.
- Press `Ctrl+C` to stop.

### How it works
- Files created in `WATCH_FOLDER` are classified by extension using `ORGANIZE_RULES` in `config.py`.
- Non-PDFs are moved directly to their category folder.
- PDFs (when `OPENAI_API_KEY` is set) are uploaded to OpenAI for a one-word subcategory (e.g., `finance`, `tax`, `legal`).
  - If classification succeeds, the file is moved to `Documents/<subcategory>`.
  - If the file is password-protected/unreadable or the API is unavailable, it’s moved to `Documents/` directly.

### Optional: Install as a CLI for local use
This project defines a console script `marie-kondo` in `pyproject.toml`.
```bash
pip install -e .
marie-kondo
```

### Logs
- Logs are written to `logs/` with timestamps and include filename, function, and line number.

### Troubleshooting
- Permission errors: ensure you have read/write access to `WATCH_FOLDER` and destination folders.
- OpenAI errors or unreadable PDFs: files fall back to `Documents/` without subcategory.
- Ensure `watchdog` is installed (provided via `requirements.txt`).

### Uninstall (editable install)
```bash
pip uninstall marie-kondo
```
