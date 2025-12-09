# app/core/settings.py
import os
from dataclasses import dataclass


@dataclass
class Paths:
    """
    Central place to resolve paths used by the app.
    This will help later with PyInstaller, relative paths, etc.
    """
    base_dir: str

    @property
    def resources_dir(self) -> str:
        return os.path.join(self.base_dir, "resources")

    @property
    def theme_qss(self) -> str:
        return os.path.join(self.resources_dir, "theme.qss")

    @property
    def icons_dir(self) -> str:
        return os.path.join(self.resources_dir, "icons")

    # XML files (can be adjusted/configurable later)
    @property
    def questinfo_xml(self) -> str:
        return os.path.join(self.base_dir, "QuestInfo.img.xml")

    @property
    def check_xml(self) -> str:
        return os.path.join(self.base_dir, "Check.img.xml")

    @property
    def act_xml(self) -> str:
        return os.path.join(self.base_dir, "Act.img.xml")


def get_default_paths() -> Paths:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return Paths(base_dir=base_dir)
