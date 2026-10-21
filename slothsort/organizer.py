import os, shutil, json
from pathlib import Path
from datetime import datetime
from rich.console import Console

console = Console()
UNDO_LOG_PATH = Path("undo_log.json")

def get_unique_path(target_path: Path) -> Path:
    if not target_path.exists(): return target_path
    stem, ext, counter = target_path.stem, target_path.suffix, 1
    while True:
        candidate = target_path.parent / f"{stem}_{counter}{ext}"
        if not candidate.exists(): return candidate
        counter += 1

def log_movement(orig: Path, new_p: Path):
    data = []
    if UNDO_LOG_PATH.exists():
        try:
            with open(UNDO_LOG_PATH, "r", encoding="utf-8") as f: data = json.load(f)
        except Exception: data = []
    data.append({"timestamp": datetime.now().isoformat(), "from": str(orig.resolve()), "to": str(new_p.resolve())})
    with open(UNDO_LOG_PATH, "w", encoding="utf-8") as f: json.dump(data, f, indent=2)

def move_file(source: Path, target_dir: Path, new_filename: str, dry_run: bool = False) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    dest = get_unique_path(target_dir / new_filename)
    if dry_run:
        console.print(f"[yellow][DRY RUN][/yellow] {source.name} -> {dest}")
        return dest
    shutil.move(str(source), str(dest))
    log_movement(source, dest)
    console.print(f"[green]Moved:[/green] {source.name} -> [bold]{dest}[/bold]")
    return dest

def undo_last_run():
    if not UNDO_LOG_PATH.exists():
        console.print("[red]No undo log found.[/red]"); return
    with open(UNDO_LOG_PATH, "r", encoding="utf-8") as f: data = json.load(f)
    for entry in reversed(data):
        curr, orig = Path(entry["to"]), Path(entry["from"])
        if curr.exists():
            orig.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(curr), str(orig))
            console.print(f"[cyan]Restored:[/cyan] {curr.name} -> {orig}")
    UNDO_LOG_PATH.unlink()
    console.print("[bold green]Undo completed.[/bold green]")
