# app/xml/questinfo_helpers.py
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, List, Tuple
from .xml_loader import ensure_imgdir


def get_imgdir(root: Optional[ET.Element], quest_id: int) -> Optional[ET.Element]:
    """Return <imgdir name='quest_id'> node."""
    if root is None:
        return None
    return root.find(f"./imgdir[@name='{quest_id}']")


def extract_questinfo(root: Optional[ET.Element], quest_id: int) -> Dict[str, Any]:
    """
    Extract QuestInfo fields for a single quest.
    """
    data = {
        "name": "",
        "summary": "",
        "rewardSummary": "",
        "demandSummary": "",
        "log0": "",
        "log1": "",
        "log2": "",
        "type": "",
        "parent": "",
        "area": None,
        "order": None,
        "autoStart": None,
        "autoComplete": None,
    }

    if root is None:
        return data

    node = get_imgdir(root, quest_id)
    if node is None:
        return data

    for child in node:
        tag = child.tag
        name = child.get("name")
        val = child.get("value", "")

        if tag == "string":
            if name == "name":
                data["name"] = val
            elif name == "summary":
                data["summary"] = val
            elif name == "rewardSummary":
                data["rewardSummary"] = val
            elif name == "demandSummary":
                data["demandSummary"] = val
            elif name == "0":
                data["log0"] = val
            elif name == "1":
                data["log1"] = val
            elif name == "2":
                data["log2"] = val
            elif name == "type":
                data["type"] = val
            elif name == "parent":
                data["parent"] = val

        elif tag == "int":
            try:
                iv = int(val)
            except ValueError:
                continue

            if name == "area":
                data["area"] = iv
            elif name == "order":
                data["order"] = iv
            elif name == "autoStart":
                data["autoStart"] = bool(iv)
            elif name == "autoComplete":
                data["autoComplete"] = bool(iv)

    # Fallback summary: use log0 if summary empty
    if not data["summary"] and data["log0"]:
        data["summary"] = data["log0"]

    return data


def apply_questinfo(root: Optional[ET.Element], qid: int, data: Dict[str, Any]):
    """Write QuestInfo data into QuestInfo.img.xml exactly like your original tool."""
    if root is None:
        return

    node = ensure_imgdir(root, str(qid))

    # Remove everything
    for child in list(node):
        node.remove(child)

    def set_string(name, value):
        if value not in ("", None):
            ET.SubElement(node, "string", {"name": name, "value": str(value)})

    def set_int(name, value):
        if value not in ("", None):
            ET.SubElement(node, "int", {"name": name, "value": str(value)})

    set_string("name", data.get("name"))
    set_string("summary", data.get("summary"))
    set_string("rewardSummary", data.get("rewardSummary"))
    set_string("demandSummary", data.get("demandSummary"))
    set_string("0", data.get("log0"))
    set_string("1", data.get("log1"))
    set_string("2", data.get("log2"))
    set_string("type", data.get("type"))
    set_string("parent", data.get("parent"))

    set_int("area", data.get("area"))
    set_int("order", data.get("order"))
    set_int("autoStart", 1 if data.get("autoStart") else 0)
    set_int("autoComplete", 1 if data.get("autoComplete") else 0)


def get_all_quest_ids(root: Optional[ET.Element]) -> List[Tuple[int, str]]:
    """
    Return a sorted list of (questId, name) using extract_questinfo(),
    so the UI always sees real quest info.
    """
    results: List[Tuple[int, str]] = []

    if root is None:
        return results

    for imgdir in root.findall("./imgdir"):
        qid_str = imgdir.get("name")
        if not (qid_str and qid_str.isdigit()):
            continue

        qid = int(qid_str)
        info = extract_questinfo(root, qid)
        name = info.get("name", "") or ""

        results.append((qid, name))

    return sorted(results, key=lambda x: x[0])
