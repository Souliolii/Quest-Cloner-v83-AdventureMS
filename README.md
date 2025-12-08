Quest-Cloner v83 — AdventureMS
MapleStory Quest XML Cloner & GUI Tool

A Python and GUI-based utility for duplicating MapleStory quest entries using exported Classic XML files (Act.img.xml, Check.img.xml, QuestInfo.img.xml, etc.).
This tool replaces the need to manually copy/paste quest blocks inside HaRepacker.

Both a command-line script (quest_helper.py) and a GUI EXE (quest_helper_gui.exe) are included.

Features
--------

- Clone an existing quest ID to a new quest ID.
- Automatically update QuestInfo fields:
  - name
  - summary
  - rewardSummary
- Works across all major quest XMLs:
  - Act.img.xml
  - Check.img.xml
  - Exclusive.img.xml
  - PQuest.img.xml
  - QuestInfo.img.xml
  - Say.img.xml
- Creates automatic .bak backups before modifying files.
- Optional debug mode for detailed output.
- Fully interactive; no command-line arguments required.

Requirements
-----------

Python Version:
- Python 3.10–3.12
- Folder containing Classic XML exports:
  Act.img.xml
  Check.img.xml
  Exclusive.img.xml
  PQuest.img.xml
  QuestInfo.img.xml
  Say.img.xml
  quest_helper.py

These files must come from HaRepacker:
File → Export → Classic XML

GUI / EXE Version:
- No Python required
- The EXE must be placed in the same folder as the exported .img.xml files.

Setup
-----

1. Export Quest.wz from HaRepacker as Classic XML.
2. Place all .img.xml files in a single folder.
3. Place either:
   - quest_helper.py (Python version)
   - quest_helper_gui.exe (GUI version)

(Optional) Windows launcher script:
Create run_quest_helper.bat:

@echo off
cd /d "%~dp0"
python quest_helper.py
pause

Running the Tool
----------------

Python Version:
cd /d "path\to\QuestXML"
python quest_helper.py

GUI / EXE Version:
Double-click:
quest_helper_gui.exe

The EXE must be inside the same folder as the .img.xml files.

Usage
-----

You will be prompted for:

- Base Quest ID (the existing quest to clone)
- New Quest ID (the new quest to create)
- Optional new fields:
  name
  summary
  rewardSummary

Leave fields blank to reuse the original text from the base quest.

Example:
Base quest ID: 20011
New quest ID: 3000
New name: My Custom Quest
New summary: Talk to the NPC to begin.
New reward summary: Adventure begins.

How It Works
------------

For each quest XML file:

1. Finds <imgdir name="QuestID">
2. Creates a deep clone
3. Renames it to the new quest ID
4. Updates QuestInfo fields (if provided)
5. Saves the modified XML
6. Creates an automatic backup:
   filename.xml.bak

Reimporting into the Client
---------------------------

1. Open Quest.wz in HaRepacker
2. Right-click → Import XML
3. Select the modified .img.xml files
4. Save Quest.wz
5. Replace the client’s Quest.wz with the updated version

Your new quest now appears in-game.

Server-Side Requirements
------------------------

Creating a new quest in the client is not enough.
The server must also contain the same quest ID or the quest will fail to function.

The server must contain:
- Act (rewards)
- Check (kill requirements)
- Info (QuestInfo)

If cloning 1037 to 3000:
Client must contain 3000
Server must also contain 3000

Troubleshooting
---------------

“Act.img.xml not found in this folder”:
You are running the tool in the wrong directory.

“QuestInfo.img.xml not found in script folder”:
The EXE is in a folder containing .img files, not .img.xml files.

Quest appears but does not track kills:
Server does not contain the cloned quest.

Quest not created:
The base quest ID does not exist.
Search for:
<imgdir name="1037">

License
-------

MIT License
