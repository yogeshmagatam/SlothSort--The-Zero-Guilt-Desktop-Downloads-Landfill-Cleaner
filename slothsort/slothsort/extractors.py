import os
from pathlib import Path
from typing import Optional, Tuple
from pypdf import PdfReader
from PIL import Image

def get_file_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp"]:
        return "image"
    if ext == ".pdf":
        return "pdf"
    if ext in [".txt", ".md", ".csv", ".json", ".py", ".sh", ".js", ".html", ".log"]:
        return "text"
    if ext in [".dmg", ".pkg", ".exe", ".msi", ".deb"]:
        return "installer"
    if ext in [".zip", ".tar", ".gz", ".rar", ".7z"]:
        return "archive"
    return "binary"

def extract_content_snippet(path: Path, max_chars: int = 1500) -> Tuple[str, Optional[str]]:
    file_type = get_file_type(path)
    try:
        if file_type == "image":
            with Image.open(path) as img:
                img.verify()
            return "image", str(path)
        elif file_type == "pdf":
            reader = PdfReader(str(path))
            if len(reader.pages) == 0:
                return "empty", ""
            return "pdf_text", (reader.pages[0].extract_text() or "")[:max_chars].strip()
        elif file_type == "text":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return "text", f.read(max_chars).strip()
        elif file_type in ["installer", "archive"]:
            return file_type, path.name
    except Exception as e:
        return "error", str(e)
    return "unknown", path.name
