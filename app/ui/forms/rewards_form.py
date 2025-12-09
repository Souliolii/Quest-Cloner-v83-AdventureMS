from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QTextEdit


class RewardsForm(QWidget):
    """
    Form for quest rewards.
    Used for both Base and New.
    """

    def __init__(self, parent=None, read_only: bool = False, title_suffix: str = ""):
        super().__init__(parent)

        layout = QFormLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.exp_edit = QLineEdit(self)
        self.gain_items_text = QTextEdit(self)
        self.lose_items_text = QTextEdit(self)

        self.gain_items_text.setPlaceholderText("itemId count per line")
        self.lose_items_text.setPlaceholderText("itemId count per line (lost/consumed)")

        layout.addRow("EXP Reward:", self.exp_edit)
        layout.addRow("Gain Items:", self.gain_items_text)
        layout.addRow("Lose Items:", self.lose_items_text)

        self.set_read_only(read_only)

    def set_read_only(self, read_only: bool):
        self.exp_edit.setReadOnly(read_only)
        self.gain_items_text.setReadOnly(read_only)
        self.lose_items_text.setReadOnly(read_only)

    def set_data(self, data: dict):
        self.exp_edit.setText(str(data.get("exp", "")))
        self.gain_items_text.setPlainText(data.get("gainItems", ""))
        self.lose_items_text.setPlainText(data.get("loseItems", ""))

    def to_data(self) -> dict:
        return {
            "exp": self.exp_edit.text().strip(),
            "gainItems": self.gain_items_text.toPlainText(),
            "loseItems": self.lose_items_text.toPlainText(),
        }
