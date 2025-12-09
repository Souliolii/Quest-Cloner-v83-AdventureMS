from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QToolButton,
    QFrame,
)
from PySide6.QtCore import Qt


class CollapsibleSection(QWidget):
    """
    Collapsible section widget:
    - Header button
    - Content area that can be expanded/collapsed

    We expose set_expanded(expanded: bool) so other sections can be kept in sync
    without causing signal recursion.
    """

    def __init__(self, title: str, parent=None):
        super().__init__(parent)

        self.toggle_button = QToolButton(self)
        self.toggle_button.setObjectName("CollapsibleHeader")
        self.toggle_button.setText(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.DownArrow)

        self.content_area = QFrame(self)
        self.content_area.setObjectName("CollapsibleContent")
        self.content_area.setFrameShape(QFrame.NoFrame)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.toggle_button)
        layout.addWidget(self.content_area)

        self.toggle_button.toggled.connect(self._on_button_toggled)

    def setContentLayout(self, layout):
        self.content_area.setLayout(layout)

    def _on_button_toggled(self, checked: bool):
        self.set_expanded(checked)

    def set_expanded(self, expanded: bool):
        """Expand/collapse programmatically without re-emitting toggled."""
        self.toggle_button.blockSignals(True)
        self.toggle_button.setChecked(expanded)
        self.toggle_button.blockSignals(False)

        self.content_area.setVisible(expanded)
        self.toggle_button.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
