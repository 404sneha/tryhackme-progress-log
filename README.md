# TryHackMe Progress Log

I'm documenting my journey through TryHackMe as I build my cybersecurity fundamentals and work towards a SOC Analyst role.

## Current Learning Path
**Introduction to Cybersecurity**

- [ ] Room 1: What is Cybersecurity?
- [ ] Room 2: CIA Triad
- [ ] Room 3: Who is the Hacker?
- [ ] Room 4: Attack Vectors
- [ ] Room 5: Skills and Certifications

## Progress Logger

I built a small Python script to record my learning sessions instead of relying on scattered notes.

**What it does**
- Records the room name and URL.
- Saves topics, tools, and learning notes.
- Documents the relevance to SOC / Blue Team work.
- Keeps track of concepts to revise.
- Stores progress locally in JSON and Markdown files.

## Tech Stack
- Python
- JSON
- Markdown
- Git and GitHub

## Run Locally

Make sure Python is installed, then run:

```bash
python add_room.py
```

Follow the prompts to record a room. The script creates a Markdown note and updates `progress.json`.

## Repository Structure

```text
tryhackme-progress-log/
├── add_room.py
├── progress.json
├── README.md
└── rooms/
    └── your-room-notes.md
```

I'm building this project as I learn, so the structure and features will evolve along the way.