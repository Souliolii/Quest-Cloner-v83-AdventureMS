from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QTextEdit


class RequirementsForm(QWidget):
    """
    Form for quest requirements.
    Used for both Base and New.
    """

    def __init__(self, parent=None, read_only: bool = False, title_suffix: str = ""):
        super().__init__(parent)

        layout = QFormLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.start_npc_edit = QLineEdit(self)
        self.end_npc_edit = QLineEdit(self)
        self.level_min_edit = QLineEdit(self)
        self.items_text = QTextEdit(self)
        self.mobs_text = QTextEdit(self)
        self.prereq_text = QTextEdit(self)

        self.items_text.setPlaceholderText("itemId count per line")
        self.mobs_text.setPlaceholderText("mobId count per line")
        self.prereq_text.setPlaceholderText("questId state per line")

        layout.addRow(f"Start NPC{title_suffix}:", self.start_npc_edit)
        layout.addRow(f"End NPC{title_suffix}:", self.end_npc_edit)
        layout.addRow("Min Level:", self.level_min_edit)
        layout.addRow("Required Items:", self.items_text)
        layout.addRow("Required Mobs:", self.mobs_text)
        layout.addRow("Prereq Quests:", self.prereq_text)

        self.set_read_only(read_only)

    def set_read_only(self, read_only: bool):
        for w in (
            self.start_npc_edit,
            self.end_npc_edit,
            self.level_min_edit,
        ):
            w.setReadOnly(read_only)
        for w in (self.items_text, self.mobs_text, self.prereq_text):
            w.setReadOnly(read_only)

    def set_data(self, data: dict):
        self.start_npc_edit.setText(str(data.get("startNpc", "")))
        self.end_npc_edit.setText(str(data.get("endNpc", "")))
        self.level_min_edit.setText(str(data.get("lvmin", "")))
        self.items_text.setPlainText(data.get("items", ""))
        self.mobs_text.setPlainText(data.get("mobs", ""))
        self.prereq_text.setPlainText(data.get("prereq", ""))

    def to_data(self) -> dict:
        return {
            "startNpc": self.start_npc_edit.text().strip(),
            "endNpc": self.end_npc_edit.text().strip(),
            "lvmin": self.level_min_edit.text().strip(),
            "items": self.items_text.toPlainText(),
            "mobs": self.mobs_text.toPlainText(),
            "prereq": self.prereq_text.toPlainText(),
        }
