📘 Quest-Cloner v83 — AdventureMS
MapleStory Quest XML Cloner & GUI Tool

A simple Python + GUI utility for duplicating MapleStory quest entries across exported Classic XML files (Act.img.xml, Check.img.xml, QuestInfo.img.xml, etc.).
This fully removes the need to manually copy/paste blocks inside HaRepacker.

You can use either the command-line script (quest_helper.py) or the GUI EXE (quest_helper_gui.exe).

✨ Features

🔁 Clone an existing quest ID to a new quest ID

📝 Automatically updates QuestInfo text fields:

name

summary

rewardSummary

📂 Works across all major quest XMLs:

Act.img.xml

Check.img.xml

Exclusive.img.xml

PQuest.img.xml

QuestInfo.img.xml

Say.img.xml

💾 Automatically creates safe .bak backups

🧩 GUI version (EXE) — no Python required

🔍 Optional debug mode to show all operations

🧑‍💻 Interactive prompts — no arguments needed

📦 Requirements
For Python version:

Python 3.10–3.12

Folder containing the exported Classic XML quest files:

Act.img.xml
Check.img.xml
Exclusive.img.xml
PQuest.img.xml
QuestInfo.img.xml
Say.img.xml
quest_helper.py

For EXE version:

No Python needed

Just place quest_helper_gui.exe directly next to your XML files

Important: These XMLs come from
HaRepacker → File → Export → Export as Classic XML
The tool does NOT read .img or .wz files — only .img.xml.

📥 Setup

Export Quest.wz as Classic XML using HaRepacker.

Put all .img.xml files into one folder.

Either:

Put quest_helper.py in that folder (Python version), or

Put quest_helper_gui.exe in that folder (GUI version).

Optional: Run script for CLI version

Create run_quest_helper.bat:

@echo off
cd /d "%~dp0"
python quest_helper.py
pause

▶️ Running the Tool
💻 Python Version
cd /d "path\to\your\QuestXML"
python quest_helper.py

🖱 GUI / EXE Version

Just double-click:

quest_helper_gui.exe


Must be in the SAME FOLDER as your .xml files.

🧩 Usage Flow

You will be prompted for:

Base Quest ID
The ID to copy from (must exist)

New Quest ID
The ID to create (must not exist yet)

Optional fields:

Enter new text for:

Quest name

Quest summary

Reward summary

Leave blank → keeps original text.

📝 Example
Base quest ID to copy FROM: 20011
New quest ID to create: 9000001

New quest NAME: My Custom Quest
New quest SUMMARY: Talk to the NPC to begin.
New quest REWARD SUMMARY: Adventure begins!

🔧 What the Script Does

For each quest XML:

Finds the <imgdir name="QuestID"> node

Deep-clones it

Renames it to the new quest ID

Updates QuestInfo fields if provided:

name

summary

rewardSummary

Saves changes

Creates .bak backups automatically

🔄 After Editing (Client-Side Workflow)

Open Quest.wz in HaRepacker

Right-click → Import XML

Select the modified XML files

Save Quest.wz

Place updated Quest.wz into your client folder

Your custom quest now appears in-game.

⚠️ Important — Step 4 (SERVER-SIDE QUEST DATA)

If the server does not contain the same quest ID block, the quest will:

Accept correctly

Complete visually

BUT NOT TRACK KILLS / REWARDS

Your server must contain cloned quest data for:

✔ Act (rewards)
✔ Check (kill requirements)
✔ Info (QuestInfo fields)

If you're cloning quest 1037 → 3000:

Client must have Quest 3000

Server must also have Quest 3000

Otherwise:

❌ Mob kills do not update
❌ Rewards do not apply
❌ Quest never completes properly

🧰 Troubleshooting Guide
❌ “Act.img.xml not found in this folder”

You're running the tool in the wrong folder.
Put the EXE or script next to the XMLs.

❌ “QuestInfo.img.xml not found in script folder”

You ran the EXE in a folder with .img files, not .img.xml files.

❌ Quest appears in-game but does not award items/EXP

Your server does NOT contain the cloned quest data — see Step 4.

❌ New quest not created

Your base quest ID doesn't exist.
Search for:

<imgdir name="1037">

📄 License

MIT License
Free to use, modify, redistribute, and include in private servers.
