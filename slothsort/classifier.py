import json, re, ollama
from typing import Dict, Any, List

SYSTEM_PROMPT = """You are SlothSort, an autonomous local file decluttering agent.
Inspect the provided file details and return ONLY a valid JSON object with two fields:
1. "category": Must be one exact item from the ALLOWED CATEGORIES list.
2. "suggested_name": A clean, concise, snake_case filename with the original extension intact.

Allowed categories:
{categories}

Do not include conversational text or markdown blocks. Raw JSON only."""

def clean_json_response(raw_text: str) -> Dict[str, str]:
    text = re.sub(r"^```(json)?", "", raw_text.strip(), flags=re.MULTILINE)
    text = re.sub(r"```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(text)

def classify_and_rename(file_type, content, filename, extension, categories, text_model, vision_model):
    if file_type == "installer":
        return {"category": "Software_Installers", "suggested_name": filename}
    if file_type == "archive":
        return {"category": "Archives_and_Zips", "suggested_name": filename}
    system = SYSTEM_PROMPT.format(categories=", ".join(categories))
    try:
        if file_type == "image":
            res = ollama.chat(model=vision_model, messages=[{"role": "user", "content": f"{system}\nInspect image for category + name with '{extension}'.", "images": [content]}], options={"temperature": 0.1})
        else:
            prompt = f"Filename: {filename}\nType: {file_type}\nExcerpt:\n{content}"
            res = ollama.chat(model=text_model, messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}], options={"temperature": 0.1})
        parsed = clean_json_response(res["message"]["content"])
        cat = parsed.get("category", "Uncategorized")
        if cat not in categories: cat = "Uncategorized"
        name = parsed.get("suggested_name", filename)
        if not name.endswith(extension): name += extension
        name = re.sub(r"[^\w\.\-]", "_", name)
        return {"category": cat, "suggested_name": name}
    except Exception:
        return {"category": "Uncategorized", "suggested_name": filename}
