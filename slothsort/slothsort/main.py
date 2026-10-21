import time, argparse, schedule
from pathlib import Path
from rich.console import Console
from slothsort.config import load_config
from slothsort.extractors import extract_content_snippet
from slothsort.classifier import classify_and_rename
from slothsort.organizer import move_file, undo_last_run

console = Console()

def run_organizer(config_path=None, dry_run=False):
    config = load_config(config_path)
    is_dry = dry_run or config.get("dry_run", False)
    dirs, dest = [Path(d) for d in config["watch_directories"]], Path(config["destination_base"])
    max_b = config.get("max_file_size_mb", 50) * 1024 * 1024
    console.print(f"[bold magenta]🦥 SlothSort Active[/bold magenta] | Dry run: [bold]{is_dry}[/bold]")
    for d in dirs:
        if not d.exists(): continue
        for item in d.iterdir():
            if item.is_dir() or item.name.startswith(".") or item.stat().st_size > max_b: continue
            f_type, content = extract_content_snippet(item)
            res = classify_and_rename(f_type, content, item.name, item.suffix, config["categories"], config["text_model"], config["vision_model"])
            move_file(item, dest / res["category"], res["suggested_name"], dry_run=is_dry)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--now", action="store_true")
    parser.add_argument("--daemon", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--undo", action="store_true")
    parser.add_argument("--config", type=str, default=None)
    args = parser.parse_args()
    if args.undo: return undo_last_run()
    if args.now or not args.daemon: run_organizer(args.config, args.dry_run)
    if args.daemon:
        console.print("[cyan]Sloth is hibernating. Scheduled at 02:00 daily...[/cyan]")
        schedule.every().day.at("02:00").do(run_organizer, config_path=args.config, dry_run=args.dry_run)
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    main()
