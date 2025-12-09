import xml.etree.ElementTree as ET
from typing import Tuple, Optional


def clone_node(root: ET.Element, old_id: int, new_id: int) -> Tuple[Optional[ET.Element], str]:
    """
    EXACT clone behavior from your old tool.
    Duplicates <imgdir name="old_id"> and renames it to new_id.
    """
    old = root.find(f"./imgdir[@name='{old_id}']")
    if old is None:
        return None, f"Base quest {old_id} not found."

    # If already exists, delete (old tool overwrote it)
    existing = root.find(f"./imgdir[@name='{new_id}']")
    if existing is not None:
        root.remove(existing)

    # Deep copy
    new = ET.fromstring(ET.tostring(old))
    new.set("name", str(new_id))
    root.append(new)

    return new, "OK"
