from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QTextEdit


class QuestInfoForm(QWidget):
    """
    Form for QuestInfo fields.
    Can be used for both:
    - Base Quest (readonly view)
    - New Quest (editable)
    """

    def __init__(self, parent=None, read_only: bool = False, title_suffix: str = ""):
        super().__init__(parent)

        layout = QFormLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.quest_id_edit = QLineEdit(self)
        self.quest_name_edit = QLineEdit(self)
        self.summary_edit = QTextEdit(self)
        self.reward_summary_edit = QTextEdit(self)

        self.quest_id_edit.setPlaceholderText("Quest ID")
        self.quest_name_edit.setPlaceholderText("Quest name")
        self.summary_edit.setPlaceholderText("Quest summary")
        self.reward_summary_edit.setPlaceholderText("Reward summary")

        layout.addRow(f"Quest ID{title_suffix}:", self.quest_id_edit)
        layout.addRow(f"Name{title_suffix}:", self.quest_name_edit)
        layout.addRow("Summary:", self.summary_edit)
        layout.addRow("Reward Summary:", self.reward_summary_edit)

        self.set_read_only(read_only)

    def set_read_only(self, read_only: bool):
        """Toggle read-only state for all fields."""
        for w in (
            self.quest_id_edit,
            self.quest_name_edit,
        ):
            w.setReadOnly(read_only)
        for w in (self.summary_edit, self.reward_summary_edit):
            w.setReadOnly(read_only)

    def set_data(self, data: dict):
        """
        Fill form from a dict like:
        {
          "id": "1000",
          "name": "Quest Name",
          "summary": "...",
          "rewardSummary": "..."
        }
        """
        self.quest_id_edit.setText(str(data.get("id", "")))
        self.quest_name_edit.setText(data.get("name", ""))
        self.summary_edit.setPlainText(data.get("summary", ""))
        self.reward_summary_edit.setPlainText(data.get("rewardSummary", ""))

    def to_data(self) -> dict:
        """Return the form content as a dict."""
        return {
            "id": self.quest_id_edit.text().strip(),
            "name": self.quest_name_edit.text().strip(),
            "summary": self.summary_edit.toPlainText(),
            "rewardSummary": self.reward_summary_edit.toPlainText(),
        }
