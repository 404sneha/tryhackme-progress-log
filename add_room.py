import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROOMS_DIR = ROOT / "rooms"
PROGRESS_FILE = ROOT / "progress.json"


def slugify(text):
    return (
        re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        or "room"
    )


def git_command(*args):
    subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def main():
    print("\n=== TryHackMe Progress Logger ===\n")

    name = input("Room name: ").strip()
    if not name:
        print("Room name cannot be empty.")
        return

    url = input("Room URL: ").strip()
    topics = input("Topics covered: ").strip()
    tools = input("Tools used: ").strip()
    learned = input("What did you learn? ").strip()
    soc = input("SOC / Blue Team relevance: ").strip()
    revision = input("Things to revise: ").strip()

    ROOMS_DIR.mkdir(exist_ok=True)
    slug = slugify(name)
    note_path = ROOMS_DIR / f"{slug}.md"

    if note_path.exists():
        print(f"Note already exists: {note_path.name}")
        print("Nothing was overwritten.")
        return

    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(
                PROGRESS_FILE.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError:
            print("progress.json is invalid. No changes made.")
            return
    else:
        progress = []

    if not isinstance(progress, list):
        print("progress.json must contain a JSON list.")
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

    record = {
        "room": name,
        "url": url,
        "date_logged": date.today().isoformat(),
        "note": f"rooms/{slug}.md",
    }

    note_path.write_text(note, encoding="utf-8")
    progress.append(record)

    try:
        PROGRESS_FILE.write_text(
            json.dumps(progress, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError:
        note_path.unlink(missing_ok=True)
        raise

    print(f"\nCreated: {note_path.relative_to(ROOT)}")
    print("Progress recorded locally.")

    try:
        git_command("add", "--", "rooms", "progress.json")
        git_command("commit", "-m", f"Log room: {name}")
        git_command("push", "origin", "main")
        print("Successfully pushed progress to GitHub!")

    except subprocess.CalledProcessError as error:
        print("\nAutomatic GitHub update failed.")
        print("Your local notes have been saved.")
        if error.stderr:
            print(error.stderr.strip())
        print("We can fix the Git issue without recreating your notes.")


if __name__ == "__main__":
    main()