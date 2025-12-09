# Quest-Cloner v83 — AdventureMS
### MapleStory Quest XML Cloner & Professional GUI Editor

A modern, fully graphical tool for cloning, editing, and managing MapleStory quests using Classic XML exports  
(Act.img.xml, Check.img.xml, QuestInfo.img.xml, etc.).

This project replaces manual XML editing and HaRepacker copy-paste with a clean, automated workflow.

---

# 🚀 Recommended: Use the EXE Release
Most users **do NOT need Python**.

Download the latest **EXE release**, place it next to your `.img.xml` files, and launch it.  
The tool automatically detects its working directory and safely reads/writes your XML files.

Python scripts are included for developers or contributors.

---

# ✨ Features

## 🔍 Quest Browser + Smart Search
Search quests instantly with:
- **ID or name**
- **Advanced filters:**
  - `npc:<id>` → quests starting/ending at that NPC  
  - `mob:<id>` → quests requiring that mob  
  - `item:<id>` → quests requiring *or* rewarding that item  
  - `rx:<pattern>` → regex search on `id: name`

Click any quest to preview all its data:
- Text & logs
- QuestInfo fields
- Requirements
- Rewards

---

## 📚 Quest Cloning
- Clone any quest to **one or multiple new IDs**
  - Single: `3000`
  - Batch: `3000 3001 3002` or `3000,3001,3002`
- Editable before saving
- Automatically updates QuestInfo fields:
  - `name`
  - `summary`
  - `rewardSummary`
- Copies all logs, requirements, and rewards
- **Overwrite protection**:
  - Warns if an ID already exists  
  - Requires confirmation before replacing
- Automatic `.bak` backups

---

## 📝 Quest Editing (GUI)

### Edit QuestInfo:
- Name  
- Type  
- Area  
- Parent  
- Order  
- Auto Start / Auto Complete  
- Logs 0–2  
- Summary  
- Reward Summary  
- Demand Summary  

### Edit Requirements (Check.img):
- Start NPC  
- End NPC  
- Min Level  
- Required Items  
- Required Mobs  
- Prerequisite Quests  

### Edit Rewards (Act.img):
- EXP  
- Gained items  
- Consumed items  
- **Automatic stage correction**  
  - Puts all rewards in **stage 1**  
  - Ensures stage `0` never contains EXP/items  

### Validation
- Inline red highlighting for malformed lines:
  - Items / mobs must be: `itemId count`
  - Prereq quests: `questId state`
- Must fix errors before saving

### Quality of Life
- **Copy Base → New** button  
- **Clear New Form** button  
- **Collapsible sections**:
  - QuestInfo  
  - Requirements  
  - Rewards  
  (Massively reduces scrolling)

---

## 🗑 Quest Deletion
Delete a quest across **all XML files** by:
- Selecting it in the list **or**
- Typing its ID manually  

Creates `.bak` backups automatically.

---

# 🎨 GUI Highlights
- Dark theme  
- 3-column layout  
- Fully scrollable  
- Clean section grouping  
- Batch cloning support  
- Error-proof editing  

---

# 📁 Required Files
Export the following from **HaRepacker → File → Export → Classic XML**:

```
Act.img.xml
Check.img.xml
Exclusive.img.xml
PQuest.img.xml
QuestInfo.img.xml
Say.img.xml
```

Place them in the same folder as the EXE or Python script.

---

# ⚙️ Running the Tool

## EXE (Recommended)
Double-click:

```
QuestHelper.exe
```

Must be in the same folder as your `.img.xml` files.

## Python (Developer Mode)
```
python quest_helper.py
```

There is **no separate CLI version** anymore.

---

# 🧠 Usage Overview

1. Select a base quest  
2. Enter one or more **New IDs**  
3. (Optional) edit the quest  
4. Click **Clone / Save**  
5. XML files update + backups created  

Delete quests: select or type an ID → **Delete Quest**

---

# 🔄 How It Works Internally

For each XML:
1. Finds `<imgdir name="BaseID">`
2. Deep-clones to `<imgdir name="NewID">`
3. Applies new QuestInfo / Requirements / Rewards
4. Forces Act.img rewards to stage `1`
5. Writes updated XML
6. Creates `.bak` backup

---

# 🔧 Reimporting Into MapleStory Client

1. Open **Quest.wz** in HaRepacker  
2. Import modified Classic XML files  
3. Save Quest.wz  
4. Replace client’s Quest.wz  

Your custom quests will appear in-game.

---

# 🖥 Server-Side Requirements

Client-side changes alone are not enough.

Your server **must** define the same quest ID with:
- Act data  
- Check data  
- QuestInfo  

Otherwise:
- Kills won’t track  
- Rewards won’t appear  
- Quests won’t complete  

---

# ❗ Troubleshooting

### “Act.img.xml not found”
Place the EXE/py script in the folder with your `.img.xml` files.

### “Quest does not give rewards”
Server Act data is missing.

### “Kills don’t track”
Server Check data is missing.

### “Quest doesn't appear in game”
Base ID was invalid or not present in QuestInfo.

---

# 📜 License
MIT License
