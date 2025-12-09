# app/ui/quest_list_panel.py
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QLabel,
)


class QuestListPanel(QWidget):
    """
    Left sidebar containing:
    - Search field
    - Quest list (IDs + names)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Search box
        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText(
            "Search quests (ID or name)"
        )


        # Quest list
        self.list_widget = QListWidget(self)

        # Placeholder label to show until we wire up XML loading
        placeholder_label = QLabel(
            "Quest list will be populated from QuestInfo.img.xml"
        )
        placeholder_label.setWordWrap(True)

        layout.addWidget(self.search_edit)
        layout.addWidget(self.list_widget)
        layout.addWidget(placeholder_label)
