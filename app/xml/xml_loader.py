import os
import shutil
import xml.etree.ElementTree as ET


def load_xml(path: str):
    """Load XML and return ElementTree or None."""
    if not os.path.exists(path):
        return None
    try:
        return ET.parse(path)
    except Exception:
        return None


def save_xml(tree: ET.ElementTree, path: str):
    """Save XML back to file (UTF-8)."""
    tree.write(path, encoding="utf-8", xml_declaration=True)


def backup(path: str):
    """Create .bak backup next to the target file."""
    if os.path.exists(path):
        shutil.copy2(path, path + ".bak")


def ensure_imgdir(parent: ET.Element, name: str):
    """Return existing <imgdir name='x'> or create it."""
    node = parent.find(f"./imgdir[@name='{name}']")
    if node is None:
        node = ET.SubElement(parent, "imgdir", {"name": name})
    return node
