MapleStory Quest Editor (PySide6)

A modern, fully-featured editor for MapleStory v83 Quest XML files, built with PySide6 and designed for rapid quest cloning, editing, and mass production of new quests.

This tool replaces manual XML editing and eliminates the need for HaRepacker when creating or modifying quests.

It supports every major quest XML file used in v83:

QuestInfo.img.xml

Check.img.xml

Act.img.xml

It includes:

A base quest viewer

A new quest builder

Side-by-side editing

Automated cloning with safe backups

Search, filtering, delete, and form copy tools

Collapsible UI sections

A fully modernized dark UI

Windows users: A standalone EXE is available under the Releases section — no Python required.

✨ Features
🔍 Powerful Quest Search

Type anything — ID, name keywords, etc.
The list updates instantly and keeps your scroll + selection stable even after cloning or filtering.

📑 Base → New Quest Editing

Select a quest on the left to load its full data:

QuestInfo (name, summary, reward summary, IDs…)

Requirements (NPCs, min level, items, mobs, prereqs)

Rewards (EXP, item rewards)

The right-side “New Quest” column lets you build a modified version side-by-side.

📦 Clone / Save (Multi-ID Support)

You can clone:

One new quest

Many at once (e.g. 3000 3001 3002)

Or overwrite an existing quest ID intentionally

The tool:

Applies QuestInfo, Requirements, Rewards

Writes into all XML trees

Creates .bak backups automatically

Preserves your UI state (forms stay filled, selection remains)

Prevents losing your place during mass edits

🔁 Copy Base → New

Instantly copy the base quest’s entire structure into the New Quest column.

🧹 Clear New

Clears only the New Quest column — the base form stays untouched.

❌ Delete Quest

Removes a quest from:

QuestInfo

Check

Act

Backups are always created before deletion.

📘 Collapsible Sections

All forms (QuestInfo, Requirements, Rewards) can be expanded/collapsed for fast navigation and reduced scrolling.

🗂 XML Logic (Fully Automated)
QuestInfo

Builds/updates <imgdir name="id">

Handles fields:

name

summary

rewardSummary

autoStart

autoComplete

startNPC / endNPC

Check (Requirements)

Stage 0: startNPC, lvmin, items, mob kill requirements, prereqs

Stage 1: endNPC

All user text (itemid qty, mobid qty, etc.) is safely parsed and rebuilt.

Act (Rewards)

Stage 1 only — reward output block

Handles EXP + item gains and losses

Accepts itemid qty and itemid xqty formats

🏁 Installation
Option A — Use the EXE (recommended)

Download from Releases and run:

MapleStory Quest Editor.exe


No setup required.

Option B — Run from Source
Requirements

Python 3.10+

PySide6

Install dependencies
pip install -r requirements.txt

Run
python main.py

📂 Folder Structure
quest_editor_pyside/
│
├── app/
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── quest_editor_panel.py
│   │   ├── quest_list_panel.py
│   │   ├── middle_actions_panel.py
│   │   ├── collapsible_section.py
│   │   ├── quest_info_form.py
│   │   ├── requirements_form.py
│   │   └── rewards_form.py
│   │
│   ├── xml/
│   │   ├── xml_loader.py
│   │   ├── questinfo_helpers.py
│   │   ├── check_helpers.py
│   │   └── act_helpers.py
│   │
│   └── core/
│       └── settings.py
│
├── theme.qss
├── main.py
└── README.md

🛠 How to Use
1) Load QuestInfo, Check, Act XMLs

Point the Settings menu to your extracted Classic XMLs.

2) Select a quest

Its data loads into the Base Quest column.

3) Copy Base → New (optional)

Good starting point for modifications.

4) Change the New Quest ID

Enter one or multiple IDs.

5) Hit Clone / Save

Your XMLs update instantly with backups.

6) Repeat

The editor preserves your Base + New forms for fast production.

🧪 Safety

Fully non-destructive

Every XML write creates a matching .bak file

The editor never modifies WZ files — only XML you load

Does not corrupt stage 0/1 structures

Prevents unintended reward placement in stage 0

Ensures missing <imgdir name="id"> blocks are created cleanly

🤝 Related Tools

This editor fits into a full MapleStory modding toolkit:

WZ Image Flattener

PNG + JSON generator for displaying item / mob / npc icons.
https://github.com/Souliolii/WZ-Image-Flattener

WZ Icon Viewer

GUI tool for browsing flattened icon assets.
https://github.com/Souliolii/WZ-Image-Viewer

💬 Support

If this project helps you, consider supporting the developer:
Ko-fi: https://ko-fi.com/soulioli

📜 License

MIT — free to modify and redistribute.