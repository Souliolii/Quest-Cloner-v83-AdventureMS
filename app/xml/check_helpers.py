# app/xml/check_helpers.py
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
from .xml_loader import ensure_imgdir


def extract_requirements(root: Optional[ET.Element], quest_id: int) -> Dict[str, Any]:
    """
    Extract requirements for a quest from Check.img(.xml).
    Matches your original quest_helper_gui logic.
    """
    info: Dict[str, Any] = {
        "startNpc": "",
        "endNpc": "",
        "lvmin": "",
        "items": "",
        "mobs": "",
        "prereq": "",
    }

    if root is None:
        return info

    node = root.find(f"./imgdir[@name='{quest_id}']")
    if node is None:
        return info

    start_npc = None
    end_npc = None
    lvmin = None

    items = []
    mobs = []
    prereq = []

    for stage in node.findall("./imgdir"):
        stage_name = stage.get("name")

        for child in stage:
            # Simple int fields (NPC, lvmin)
            if child.tag == "int":
                name = child.get("name")
                val = child.get("value")
                if not val:
                    continue
                try:
                    val = int(val)
                except:
                    continue

                if name == "npc":
                    if stage_name == "0":
                        start_npc = val
                    elif stage_name == "1":
                        end_npc = val
                elif name == "lvmin":
                    lvmin = val

            # Complex imgdirs
            elif child.tag == "imgdir":
                cname = child.get("name")

                # Items
                if cname == "item":
                    for idx in child.findall("imgdir"):
                        iid = None
                        count = None
                        for i in idx.findall("int"):
                            nm = i.get("name")
                            try:
                                v = int(i.get("value"))
                            except:
                                continue
                            if nm == "id":
                                iid = v
                            elif nm == "count":
                                count = v
                        if iid is not None and count is not None:
                            items.append((iid, count))

                # Mobs
                elif cname == "mob":
                    for idx in child.findall("imgdir"):
                        mid = None
                        cnt = None
                        for i in idx.findall("int"):
                            nm = i.get("name")
                            try:
                                v = int(i.get("value"))
                            except:
                                continue
                            if nm == "id":
                                mid = v
                            elif nm == "count":
                                cnt = v
                        if mid is not None and cnt is not None:
                            mobs.append((mid, cnt))

                # Prereq quests
                elif cname == "quest":
                    for idx in child.findall("imgdir"):
                        qid = None
                        st = None
                        for i in idx.findall("int"):
                            nm = i.get("name")
                            try:
                                v = int(i.get("value"))
                            except:
                                continue
                            if nm == "id":
                                qid = v
                            elif nm == "state":
                                st = v
                        if qid is not None and st is not None:
                            prereq.append((qid, st))

    if start_npc is not None:
        info["startNpc"] = str(start_npc)
    if end_npc is not None:
        info["endNpc"] = str(end_npc)
    if lvmin is not None:
        info["lvmin"] = str(lvmin)

    info["items"] = "\n".join(f"{i} {c}" for i, c in items)
    info["mobs"] = "\n".join(f"{i} {c}" for i, c in mobs)
    info["prereq"] = "\n".join(f"{q} {s}" for q, s in prereq)

    return info


def apply_requirements(root: Optional[ET.Element], qid: int, data: Dict[str, Any]):
    """
    EXACT port of your working apply_requirements (quest_helper_gui.py).
    """
    if root is None:
        return

    node = ensure_imgdir(root, str(qid))

    # Clear everything first
    for child in list(node):
        node.remove(child)

    # Stage 0
    stage0 = ET.SubElement(node, "imgdir", {"name": "0"})

    # Start NPC
    if data.get("startNpc"):
        ET.SubElement(stage0, "int", {"name": "npc", "value": data["startNpc"]})

    # lvmin
    if data.get("lvmin"):
        ET.SubElement(stage0, "int", {"name": "lvmin", "value": data["lvmin"]})

    # Helper parser
    def parse_lines(text):
        results = []
        if not text:
            return results
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            line = line.replace("x", " ").replace("X", " ")
            parts = line.split()
            if len(parts) == 2:
                try:
                    results.append((int(parts[0]), int(parts[1])))
                except:
                    pass
        return results

    items = parse_lines(data.get("items"))
    mobs = parse_lines(data.get("mobs"))
    prereq = parse_lines(data.get("prereq"))

    # Items
    if items:
        block = ET.SubElement(stage0, "imgdir", {"name": "item"})
        for idx, (item_id, count) in enumerate(items):
            row = ET.SubElement(block, "imgdir", {"name": str(idx)})
            ET.SubElement(row, "int", {"name": "id", "value": str(item_id)})
            ET.SubElement(row, "int", {"name": "count", "value": str(count)})

    # Mobs
    if mobs:
        block = ET.SubElement(stage0, "imgdir", {"name": "mob"})
        for idx, (mob_id, count) in enumerate(mobs):
            row = ET.SubElement(block, "imgdir", {"name": str(idx)})
            ET.SubElement(row, "int", {"name": "id", "value": str(mob_id)})
            ET.SubElement(row, "int", {"name": "count", "value": str(count)})

    # Prerequisite quests
    if prereq:
        block = ET.SubElement(stage0, "imgdir", {"name": "quest"})
        for idx, (qid2, state) in enumerate(prereq):
            row = ET.SubElement(block, "imgdir", {"name": str(idx)})
            ET.SubElement(row, "int", {"name": "id", "value": str(qid2)})
            ET.SubElement(row, "int", {"name": "state", "value": str(state)})

    # Stage 1 = end NPC
    stage1 = ET.SubElement(node, "imgdir", {"name": "1"})
    if data.get("endNpc"):
        ET.SubElement(stage1, "int", {"name": "npc", "value": data["endNpc"]})
