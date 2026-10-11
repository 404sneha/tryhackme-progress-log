
import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROOMS_DIR = ROOT / "rooms"
PROGRESS_FILE = ROOT / "progress.json"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "room"


def main():
    print("\n=== TryHackMe Progress Logger ===\n")

    name = input("Room name: ").strip()
    if not name:
        print("Room name cannot be empty.")
        return

    url = input("Room URL: ").strip()
    topics = input("Topics covered: ").strip()
    tools = input("Tools used: ").strip()

    print("\nEnter your learning notes (one line):")
    learned = input("> ").strip()
    soc = input("SOC / Blue Team relevance: ").strip()
    revision = input("Things to revise: ").strip()

    ROOMS_DIR.mkdir(exist_ok=True)
    slug = slugify(name)
    note_path = ROOMS_DIR / f"{slug}.md"

    if note_path.exists():
        print(f"\nA note already exists: {note_path.name}")
        print("Nothing was overwritten.")
        return

    note = f"""# {name}

- **Room URL:** {url or "Not provided"}
- **Date logged:** {date.today().isoformat()}
- **Topics:** {topics or "Not recorded"}
- **Tools:** {tools or "Not recorded"}

## What I learned

{learned or "Add notes later."}

## SOC / Blue Team relevance

{soc or "Add notes later."}

## Things to revise

{revision or "None recorded."}
"""

    note_path.write_text(note, encoding="utf-8")

    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(
                PROGRESS_FILE.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError:
            print("progress.json is invalid JSON. Fix it before continuing.")
            note_path.unlink(missing_ok=True)
            return
    else:
        progress = []

    if not isinstance(progress, list):
        print("progress.json must contain a JSON list.")
        note_path.unlink(missing_ok=True)
        return

    progress.append({
        "room": name,
        "url": url,
        "date_logged": date.today().isoformat(),
        "note": f"rooms/{slug}.md"
    })

    PROGRESS_FILE.write_text(
        json.dumps(progress, indent=2) + "\n",
        encoding="utf-8"
    )

    print(f"\nCreated note: {note_path.relative_to(ROOT)}")
    print("Progress recorded locally.")

    answer = input("Commit and push to GitHub now? (y/n): ").strip().lower()
    if answer == "y":
        try:
            subprocess.run(
                ["git", "add", "rooms", "progress.json"],
                cwd=ROOT, check=True
            )
            subprocess.run(
                ["git", "commit", "-m", f"Log room: {name}"],
                cwd=ROOT, check=True
            )
            subprocess.run(["git", "push"], cwd=ROOT, check=True)
            print("Successfully pushed to GitHub!")
        except subprocess.CalledProcessError:
            print("Git failed. Your notes are still saved locally.")
    else:
        print("Saved locally. Push your changes when ready.")


if __name__ == "__main__":
    main()
