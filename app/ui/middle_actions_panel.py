# app/ui/middle_actions_panel.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy


class MiddleActionsPanel(QWidget):
    """
    Middle column with transfer/utility buttons:
    - Copy Base → New
    - Clear New
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(8)

        self.copy_button = QPushButton("Copy Base → New", self)
        self.clear_button = QPushButton("Clear New", self)

        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.copy_button)
        layout.addWidget(self.clear_button)
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
