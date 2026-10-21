# The Zero-Guilt Desktop & Downloads Landfill Cleaner


> *"Work slow, conserve energy, let local AI do the decluttering."*

SlothSort is a background agent that periodically cleans your messy `~/Downloads` and `~/Desktop` folders, inspects file contents using local open-weight vision and language models, gives them descriptive names, and organizes them safely.

---
### Why Open-Source AI Matters Here

1. **Absolute Privacy:** Your downloads contain bank statements, tax forms, paystubs, IDs, and personal photos. Sending every file to a cloud API is a major privacy risk. SlothSort runs entirely on your local machine via Ollama.
2. **Zero Incurred Cost:** Sorting 400 messy files using commercial Vision APIs could cost several dollars each run. Local inference costs $0.00.
3. **Works Without Internet:** Organize clutter on an offline laptop while traveling.

---

### Project File Structure
<> Text
slothsort/
├── README.md
├── requirements.txt
├── config.yaml
├── undo_log.json            (generated upon first run)
├── slothsort/
│   ├── __init__.py
│   ├── config.py
│   ├── extractors.py
│   ├── classifier.py
│   ├── organizer.py
│   └── main.py

### Prerequisites

1. Install [Ollama](https://ollama.com/).
2. Pull the required models:
   ```bash
   ollama pull llama3.2-vision
   ollama pull llama3.2:3b

### Quickstart

1. Install dependencies:
    <>Bash
    pip install -r requirements.txt

2. Test run in dry-run mode (does not move anything):
    <>Bash
    python -m slothsort.main --now --dry-run

3. Run an actual clean-up:
    <>Bash
    python -m slothsort.main --now

4. Run as an unbothered sloth daemon (runs daily at 2:00 AM):
    <>Bash
    python -m slothsort.main --daemon

5. Made a mistake? Undo everything back to where it was:
    <>Bash
    python -m slothsort.main --undo
