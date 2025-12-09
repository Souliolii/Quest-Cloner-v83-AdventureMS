from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout

from .collapsible_section import CollapsibleSection
from .forms.quest_info_form import QuestInfoForm
from .forms.requirements_form import RequirementsForm
from .forms.rewards_form import RewardsForm


class QuestEditorPanel(QWidget):
    """
    Right panel: scrollable area with two sets of collapsible sections:
    - Left: Base Quest (readonly view of existing quest)
    - Right: New Quest (editable, used for cloning / editing)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        root_layout.addWidget(scroll_area)

        container = QWidget()
        scroll_area.setWidget(container)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(8)

        # Horizontal layout: Base Quest | New Quest
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(12)

        # ===== Base Quest column (readonly) =====
        base_column = QWidget(container)
        base_layout = QVBoxLayout(base_column)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(8)

        self.base_questinfo_section = CollapsibleSection("Base Quest — Quest Info", base_column)
        base_qi_layout = QVBoxLayout()
        self.base_questinfo_form = QuestInfoForm(self.base_questinfo_section, read_only=True, title_suffix=" (Base)")
        base_qi_layout.addWidget(self.base_questinfo_form)
        self.base_questinfo_section.setContentLayout(base_qi_layout)

        self.base_requirements_section = CollapsibleSection("Base Quest — Requirements", base_column)
        base_req_layout = QVBoxLayout()
        self.base_requirements_form = RequirementsForm(self.base_requirements_section, read_only=True, title_suffix=" (Base)")
        base_req_layout.addWidget(self.base_requirements_form)
        self.base_requirements_section.setContentLayout(base_req_layout)

        self.base_rewards_section = CollapsibleSection("Base Quest — Rewards", base_column)
        base_rew_layout = QVBoxLayout()
        self.base_rewards_form = RewardsForm(self.base_rewards_section, read_only=True, title_suffix=" (Base)")
        base_rew_layout.addWidget(self.base_rewards_form)
        self.base_rewards_section.setContentLayout(base_rew_layout)

        base_layout.addWidget(self.base_questinfo_section)
        base_layout.addWidget(self.base_requirements_section)
        base_layout.addWidget(self.base_rewards_section)
        base_layout.addStretch(1)

        # ===== New Quest column (editable) =====
        new_column = QWidget(container)
        new_layout = QVBoxLayout(new_column)
        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(8)

        self.new_questinfo_section = CollapsibleSection("New Quest — Quest Info", new_column)
        new_qi_layout = QVBoxLayout()
        self.new_questinfo_form = QuestInfoForm(self.new_questinfo_section, read_only=False, title_suffix=" (New)")
        new_qi_layout.addWidget(self.new_questinfo_form)
        self.new_questinfo_section.setContentLayout(new_qi_layout)

        self.new_requirements_section = CollapsibleSection("New Quest — Requirements", new_column)
        new_req_layout = QVBoxLayout()
        self.new_requirements_form = RequirementsForm(self.new_requirements_section, read_only=False, title_suffix=" (New)")
        new_req_layout.addWidget(self.new_requirements_form)
        self.new_requirements_section.setContentLayout(new_req_layout)

        self.new_rewards_section = CollapsibleSection("New Quest — Rewards", new_column)
        new_rew_layout = QVBoxLayout()
        self.new_rewards_form = RewardsForm(self.new_rewards_section, read_only=False, title_suffix=" (New)")
        new_rew_layout.addWidget(self.new_rewards_form)
        self.new_rewards_section.setContentLayout(new_rew_layout)

        new_layout.addWidget(self.new_questinfo_section)
        new_layout.addWidget(self.new_requirements_section)
        new_layout.addWidget(self.new_rewards_section)
        new_layout.addStretch(1)

        # Add both columns to the container
        columns_layout.addWidget(base_column)
        columns_layout.addWidget(new_column)
        container_layout.addLayout(columns_layout)

        # Link collapsible sections so base + new open/close together
        self._link_sections(self.base_questinfo_section, self.new_questinfo_section)
        self._link_sections(self.base_requirements_section, self.new_requirements_section)
        self._link_sections(self.base_rewards_section, self.new_rewards_section)

    def _link_sections(self, a: CollapsibleSection, b: CollapsibleSection):
        """Ensure that when one section is toggled, the paired section follows."""

        def on_a(checked: bool):
            b.set_expanded(checked)

        def on_b(checked: bool):
            a.set_expanded(checked)

        a.toggle_button.toggled.connect(on_a)
        b.toggle_button.toggled.connect(on_b)
