# app/xml/act_helpers.py
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
from .xml_loader import ensure_imgdir


def extract_rewards(root: Optional[ET.Element], quest_id: int) -> Dict[str, Any]:
    """
    Extract rewards from Act.img(.xml) EXACTLY like your old program.

    Output:
        {
          "exp": "1000",
          "gainItems": "2000000 10\n2000001 5",
          "loseItems": "4030000 1"
        }
    """
    info = {
        "exp": "",
        "gainItems": "",
        "loseItems": "",
    }

    if root is None:
        return info

    node = root.find(f"./imgdir[@name='{quest_id}']")
    if node is None:
        return info

    gain = []
    lose = []

    # Search stages (0 and 1)
    for stage in node.findall("./imgdir"):
        for child in stage:

            # EXP
            if child.tag == "int" and child.get("name") == "exp":
                try:
                    info["exp"] = str(int(child.get("value")))
                except Exception:
                    pass

            # Items
            if child.tag == "imgdir" and child.get("name") == "item":
                for itemdir in child.findall("./imgdir"):
                    iid = None
                    count = None
                    for i in itemdir.findall("./int"):
                        nm = i.get("name")
                        try:
                            v = int(i.get("value"))
                        except Exception:
                            continue

                        if nm == "id":
                            iid = v
                        elif nm == "count":
                            count = v

                    if iid is not None and count is not None:
                        if count >= 0:
                            gain.append((iid, count))
                        else:
                            lose.append((iid, -count))

    info["gainItems"] = "\n".join(f"{i} {c}" for i, c in gain)
    info["loseItems"] = "\n".join(f"{i} {c}" for i, c in lose)

    return info


def apply_rewards(root: Optional[ET.Element], quest_id: int, data: Dict[str, Any]):
    """
    Apply reward data to Act.img just like your old quest helper.

    Rules:
      - All rewards go into stage "1"
      - Stage "0" must NOT contain rewards
      - Negative count = lose item
    """
    if root is None:
        return

    node = ensure_imgdir(root, str(quest_id))

    # Remove all existing reward data
    for stage in node.findall("./imgdir"):
        if stage.get("name") == "0":
            # stage 0 must not contain exp or items
            for c in list(stage):
                if c.tag == "int" and c.get("name") == "exp":
                    stage.remove(c)
                if c.tag == "imgdir" and c.get("name") == "item":
                    stage.remove(c)

        if stage.get("name") == "1":
            for c in list(stage):
                if c.tag == "int" and c.get("name") == "exp":
                    stage.remove(c)
                if c.tag == "imgdir" and c.get("name") == "item":
                    stage.remove(c)

    # Ensure stage 1
    stage1 = node.find("./imgdir[@name='1']")
    if stage1 is None:
        stage1 = ET.SubElement(node, "imgdir", name="1")

    # EXP
    exp_val = data.get("exp")
    if exp_val and exp_val.isdigit():
        ET.SubElement(stage1, "int", name="exp", value=str(int(exp_val)))

    # Parse item lines
    def parse(text):
        out = []
        if not text:
            return out
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            line = line.replace("x", " ").replace("X", " ")
            parts = line.split()
            if len(parts) != 2:
                continue
            try:
                out.append((int(parts[0]), int(parts[1])))
            except:
                pass
        return out

    gain = parse(data.get("gainItems"))
    lose = parse(data.get("loseItems"))

    if gain or lose:
        item_block = ET.SubElement(stage1, "imgdir", name="item")

        idx = 0
        for iid, count in gain:
            row = ET.SubElement(item_block, "imgdir", name=str(idx))
            idx += 1
            ET.SubElement(row, "int", name="id", value=str(iid))
            ET.SubElement(row, "int", name="count", value=str(count))

        for iid, count in lose:
            row = ET.SubElement(item_block, "imgdir", name=str(idx))
            idx += 1
            ET.SubElement(row, "int", name="id", value=str(iid))
            ET.SubElement(row, "int", name="count", value=str(-count))
