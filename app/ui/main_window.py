# app/ui/main_window.py
import os
import re

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSplitter,
    QToolBar,
    QMessageBox,
    QFileDialog,
    QListWidgetItem,
    QApplication,
)
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtCore import Qt, QFile, QTextStream

from app.core.settings import get_default_paths
from app.xml import xml_loader
from app.xml.questinfo_helpers import (
    get_all_quest_ids,
    extract_questinfo,
    apply_questinfo,
)
from app.xml.check_helpers import (
    extract_requirements,
    apply_requirements,
)
from app.xml.act_helpers import (
    extract_rewards,
    apply_rewards,
)
from app.xml.xml_loader import save_xml, backup

from .quest_list_panel import QuestListPanel
from .middle_actions_panel import MiddleActionsPanel
from .quest_editor_panel import QuestEditorPanel


class QuestEditorWindow(QMainWindow):
    """
    Main window for the MapleStory Quest Editor.
    Layout:
    [ QuestListPanel ] [ MiddleActionsPanel ] [ QuestEditorPanel ]
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MapleStory Quest Editor (PySide6)")
        self.resize(1400, 800)

        self.paths = get_default_paths()

        # Where XML/IMG files live (folder chosen at startup)
        self.xml_folder = self.paths.base_dir
        self.questinfo_path: str | None = None
        self.check_path: str | None = None
        self.act_path: str | None = None

        # XML trees / roots
        self.questinfo_tree = None
        self.questinfo_root = None
        self.check_tree = None
        self.check_root = None
        self.act_tree = None
        self.act_root = None

        self.current_base_quest_id: int | None = None
        self.all_quests: list[tuple[int, str]] = []

        self._create_menu_bar()
        self._create_toolbar()
        self._create_central_layout()
        self._load_xml_files()
        self._populate_quest_list()
        self._connect_signals()

    # ---------------- Menu bar (Settings / Theme) ----------------

    def _create_menu_bar(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")
        theme_menu = settings_menu.addMenu("Theme")

        self.action_theme_dark = QAction("Dark", self)
        self.action_theme_light = QAction("Light", self)
        self.action_theme_dark.setCheckable(True)
        self.action_theme_light.setCheckable(True)

        group = QActionGroup(self)
        group.setExclusive(True)
        group.addAction(self.action_theme_dark)
        group.addAction(self.action_theme_light)

        theme_menu.addAction(self.action_theme_dark)
        theme_menu.addAction(self.action_theme_light)

        # default at startup is dark (theme.qss loaded in main.py)
        self.action_theme_dark.setChecked(True)

        self.action_theme_dark.triggered.connect(self._set_dark_theme)
        self.action_theme_light.triggered.connect(self._set_light_theme)

    def _set_dark_theme(self):
        """Switch back to the dark QSS theme (works in dev and in the EXE)."""
        app = QApplication.instance()
        if not app:
            return

        import sys

        # When running from source, __file__ → app/ui/main_window.py
        # base_dir → project root (one level above "app")
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        # When running from a PyInstaller bundle, sys._MEIPASS is the root.
        base_dir = getattr(sys, "_MEIPASS", base_dir)

        # Check a couple of common locations:
        candidates = [
            os.path.join(base_dir, "resources", "theme.qss"),  # if you keep it under resources/
            os.path.join(base_dir, "theme.qss"),               # if it's next to the EXE / main.py
        ]

        qss_path = None
        for path in candidates:
            if os.path.exists(path):
                qss_path = path
                break

        if not qss_path:
            # No theme file found; do nothing (stay in whatever style is active)
            return

        try:
            with open(qss_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            # Don't crash if anything goes wrong; just log and keep current theme.
            print(f"Failed to load dark theme stylesheet: {e}")
            return

        self.action_theme_dark.setChecked(True)
        self.action_theme_light.setChecked(False)


    def _set_light_theme(self):
        app = QApplication.instance()
        if not app:
            return
        # Clear stylesheet → default Qt light theme
        app.setStyleSheet("")
        self.action_theme_dark.setChecked(False)
        self.action_theme_light.setChecked(True)

    # ---------------- Toolbar ----------------

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setMovable(False)

        self.clone_action = QAction("Clone / Save", self)
        self.delete_action = QAction("Delete Quest", self)
        self.preview_action = QAction("Preview IDs", self)

        toolbar.addAction(self.clone_action)
        toolbar.addAction(self.delete_action)
        toolbar.addAction(self.preview_action)

        self.addToolBar(Qt.TopToolBarArea, toolbar)

        self.clone_action.triggered.connect(self._on_clone_save)
        self.delete_action.triggered.connect(self._on_delete_quest)
        self.preview_action.triggered.connect(self._on_preview_ids)

    # ---------------- Layout ----------------

    def _create_central_layout(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        splitter = QSplitter(Qt.Horizontal, central_widget)

        # Left: Quest list
        self.quest_list_panel = QuestListPanel(splitter)

        # Middle: actions (copy base → new, clear new)
        self.middle_actions_panel = MiddleActionsPanel(splitter)

        # Right: main quest editor (collapsible sections)
        self.quest_editor_panel = QuestEditorPanel(splitter)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        splitter.setStretchFactor(2, 3)

        main_layout.addWidget(splitter)

    # ---------------- XML loading ----------------

    def _load_xml_files(self):
        """
        Ask the user for a folder, then look inside it for:
        - QuestInfo.img(.xml)
        - Check.img(.xml)
        - Act.img(.xml)
        """
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select folder containing QuestInfo / Check / Act IMG/XML files",
            self.paths.base_dir,
        )
        if not folder:
            QMessageBox.warning(
                self,
                "No folder selected",
                "No folder was selected. The editor will open, but no XML files are loaded.",
            )
            return

        self.xml_folder = folder

        def find_file(base_name: str) -> str | None:
            candidates = [
                f"{base_name}.img.xml",
                f"{base_name}.img",
                f"{base_name}.xml",
            ]
            for fname in candidates:
                path = os.path.join(folder, fname)
                if os.path.exists(path):
                    return path
            return None

        self.questinfo_path = find_file("QuestInfo")
        self.check_path = find_file("Check")
        self.act_path = find_file("Act")

        def load_tree(path: str | None):
            return xml_loader.load_xml(path) if path else None

        self.questinfo_tree = load_tree(self.questinfo_path)
        self.questinfo_root = (
            self.questinfo_tree.getroot() if self.questinfo_tree is not None else None
        )

        self.check_tree = load_tree(self.check_path)
        self.check_root = (
            self.check_tree.getroot() if self.check_tree is not None else None
        )

        self.act_tree = load_tree(self.act_path)
        self.act_root = (
            self.act_tree.getroot() if self.act_tree is not None else None
        )

        missing = []
        if self.questinfo_tree is None:
            missing.append("QuestInfo.img / QuestInfo.img.xml")
        if self.check_tree is None:
            missing.append("Check.img / Check.img.xml")
        if self.act_tree is None:
            missing.append("Act.img / Act.img.xml")

        if missing:
            QMessageBox.warning(
                self,
                "Missing XML files",
                "Could not find or load the following files in:\n"
                f"{folder}\n\n"
                + "\n".join(missing)
                + "\n\nThe editor will still open, but some features will be disabled.",
            )

    # ---------------- Quest list + search ----------------

    def _populate_quest_list(self):
        lw = self.quest_list_panel.list_widget

        # Avoid firing selection-changed signals while we rebuild the list,
        # so we don't accidentally clear the forms.
        lw.blockSignals(True)
        lw.clear()
        self.all_quests = []

        if self.questinfo_root is None:
            lw.blockSignals(False)
            return

        self.all_quests = get_all_quest_ids(self.questinfo_root)

        # Keep whatever the user typed in the search box,
        # so we don't blow away their filter/place.
        current_filter = self.quest_list_panel.search_edit.text()
        self._refresh_quest_list(current_filter)
        lw.blockSignals(False)

    def _refresh_quest_list(self, filter_text: str):
        """Refill the quest list widget based on current self.all_quests and a filter string."""
        lw = self.quest_list_panel.list_widget

        # Avoid clearing forms when the list is re-filtered.
        lw.blockSignals(True)
        lw.clear()

        if not self.all_quests:
            lw.blockSignals(False)
            return

        filt = (filter_text or "").strip().lower()

        for qid, name in self.all_quests:
            label = f"{qid}: {name}"
            if filt:
                if filt not in str(qid) and filt not in name.lower():
                    continue
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, qid)
            lw.addItem(item)

        lw.blockSignals(False)




    # ---------------- Signals ----------------

    def _connect_signals(self):
        lw = self.quest_list_panel.list_widget
        lw.currentItemChanged.connect(self._on_quest_selected)

        self.quest_list_panel.search_edit.textChanged.connect(
            self._on_search_text_changed
        )

        self.middle_actions_panel.copy_button.clicked.connect(
            self._on_copy_base_to_new
        )
        self.middle_actions_panel.clear_button.clicked.connect(self._on_clear_new)

    # ---------------- Event handlers ----------------

    def _on_search_text_changed(self, text: str):
        self._refresh_quest_list(text)

    def _on_quest_selected(self, current, previous):
        if current is None or self.questinfo_root is None:
            self.current_base_quest_id = None
            self._clear_base_forms()
            self._clear_new_forms()
            return

        quest_id = current.data(Qt.UserRole)
        if quest_id is None:
            self.current_base_quest_id = None
            self._clear_base_forms()
            self._clear_new_forms()
            return

        self.current_base_quest_id = int(quest_id)

        # QuestInfo
        qi_data = extract_questinfo(self.questinfo_root, self.current_base_quest_id)
        qi_data["id"] = self.current_base_quest_id

        # Requirements / Rewards
        req_data = extract_requirements(self.check_root, self.current_base_quest_id)
        rew_data = extract_rewards(self.act_root, self.current_base_quest_id)

        # Fill Base column
        self.quest_editor_panel.base_questinfo_form.set_data(qi_data)
        self.quest_editor_panel.base_requirements_form.set_data(req_data)
        self.quest_editor_panel.base_rewards_form.set_data(rew_data)

        # New column is cleared until you hit Copy Base → New
        self._clear_new_forms()

    def _clear_base_forms(self):
        empty = {}
        self.quest_editor_panel.base_questinfo_form.set_data(empty)
        self.quest_editor_panel.base_requirements_form.set_data(empty)
        self.quest_editor_panel.base_rewards_form.set_data(empty)

    def _clear_new_forms(self):
        empty = {}
        self.quest_editor_panel.new_questinfo_form.set_data(empty)
        self.quest_editor_panel.new_requirements_form.set_data(empty)
        self.quest_editor_panel.new_rewards_form.set_data(empty)

    def _on_copy_base_to_new(self):
        """
        Copy Base forms → New forms.
        """
        base_qi = self.quest_editor_panel.base_questinfo_form.to_data()
        base_qi["id"] = ""  # force user to type new ID for clones
        self.quest_editor_panel.new_questinfo_form.set_data(base_qi)

        base_req = self.quest_editor_panel.base_requirements_form.to_data()
        base_rew = self.quest_editor_panel.base_rewards_form.to_data()

        self.quest_editor_panel.new_requirements_form.set_data(base_req)
        self.quest_editor_panel.new_rewards_form.set_data(base_rew)

    def _on_clear_new(self):
        """Clear only the New Quest column forms."""
        self._clear_new_forms()



    def _on_clone_save(self):
        """
        Clone / save the New Quest column into the XMLs.

        Behavior:
          - Uses the currently selected quest on the left as the *base* quest.
          - New Quest → Quest Info "ID" field may contain one or more IDs
            (separated by spaces/commas).
          - For each target ID, QuestInfo / Check / Act are written from the
            New Quest forms.
        """
        if self.questinfo_root is None:
            QMessageBox.warning(
                self,
                "No QuestInfo loaded",
                "QuestInfo.img.xml is not loaded. Cannot clone/save quests.",
            )
            return

        if self.current_base_quest_id is None:
            QMessageBox.warning(
                self,
                "No Base Quest",
                "Select a base quest on the left first.",
            )
            return

        # Collect form data (New column)
        qi_data = self.quest_editor_panel.new_questinfo_form.to_data()
        req_data = self.quest_editor_panel.new_requirements_form.to_data()
        rew_data = self.quest_editor_panel.new_rewards_form.to_data()

        id_text = str(qi_data.get("id", "")).strip()
        if not id_text:
            QMessageBox.warning(
                self,
                "Missing New ID",
                "Enter at least one New Quest ID in the New Quest → Quest Info section.",
            )
            return

        # Parse IDs: allow "3000 3001,3002"
        tokens = [t for t in re.split(r"[\\s,]+", id_text) if t]
        new_ids = []
        invalid_tokens = []
        for t in tokens:
            if t.isdigit():
                new_ids.append(int(t))
            else:
                invalid_tokens.append(t)

        if invalid_tokens or not new_ids:
            QMessageBox.warning(
                self,
                "Invalid Quest ID(s)",
                "Quest IDs must be numeric.\n\n"
                f"Invalid tokens: {', '.join(invalid_tokens) if invalid_tokens else 'none'}",
            )
            return

        base_id = self.current_base_quest_id

        # Warn if any targets already exist (and are not just the base-id edit-in-place case)
        existing_ids: list[int] = []
        for nid in new_ids:
            if nid == base_id:
                # Editing the base quest in-place is allowed without warning.
                continue
            node = self.questinfo_root.find(f"./imgdir[@name='{nid}']")
            if node is not None:
                existing_ids.append(nid)

        if existing_ids:
            resp = QMessageBox.question(
                self,
                "Overwrite existing quests?",
                "The following quest IDs already exist and will be overwritten:\n"
                f"{', '.join(str(i) for i in existing_ids)}\n\n"
                "Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if resp != QMessageBox.Yes:
                return

        # --- Apply changes in-memory ---
        messages: list[str] = []
        saved_labels: list[str] = []

        for nid in new_ids:
            # Ensure the data dict has the correct ID for this target
            qi_for_id = dict(qi_data)
            qi_for_id["id"] = nid

            # Track what we actually saved so we can show it in the popup.
            qname = qi_for_id.get("name", "")
            if qname:
                saved_labels.append(f"{nid}: {qname}")
            else:
                saved_labels.append(str(nid))

            apply_questinfo(self.questinfo_root, nid, qi_for_id)
            apply_requirements(self.check_root, nid, req_data)
            apply_rewards(self.act_root, nid, rew_data)

        # --- Save XMLs with .bak backups, like the old tool ---
        if self.questinfo_tree and self.questinfo_path:
            backup(self.questinfo_path)
            save_xml(self.questinfo_tree, self.questinfo_path)
            if saved_labels:
                messages.append(
                    f"QuestInfo: saved {len(new_ids)} quest(s): "
                    + ", ".join(saved_labels)
                )
            else:
                messages.append(f"QuestInfo: saved {len(new_ids)} quest(s).")

        else:
            messages.append("QuestInfo: not loaded, skipping.")

        if self.check_tree and self.check_path:
            backup(self.check_path)
            save_xml(self.check_tree, self.check_path)
            messages.append("Check: updated requirements.")
        else:
            messages.append("Check: not loaded, skipping.")

        if self.act_tree and self.act_path:
            backup(self.act_path)
            save_xml(self.act_tree, self.act_path)
            messages.append("Act: updated rewards.")
        else:
            messages.append("Act: not loaded, skipping.")

        # --- Keep your place in the quest list ---
        # Remember which quest was selected as base
        selected_id = self.current_base_quest_id

        # Rebuild the quest list from updated QuestInfo
        self._populate_quest_list()

        # Restore selection to the same base quest without firing selection handler
        if selected_id is not None:
            lw = self.quest_list_panel.list_widget
            target_item = None
            for i in range(lw.count()):
                item = lw.item(i)
                if item.data(Qt.UserRole) == selected_id:
                    target_item = item
                    break

            if target_item is not None:
                lw.blockSignals(True)
                lw.setCurrentItem(target_item)
                lw.blockSignals(False)
                lw.scrollToItem(target_item)

        QMessageBox.information(
            self,
            "Clone / Save",
            "\n".join(messages),
        )


    def _on_delete_quest(self):
        """
        Delete a quest from all loaded XMLs (QuestInfo / Check / Act).

        Priority for picking the quest ID:
          1) Currently selected quest in the left list
          2) Quest ID in the New Quest form
        """
        # 1) Try the currently selected quest in the list
        qid: int | None = None
        lw = self.quest_list_panel.list_widget
        current_item = lw.currentItem()
        if current_item is not None:
            data = current_item.data(Qt.UserRole)
            if isinstance(data, int):
                qid = data

        # 2) Fallback: quest ID typed in the New Quest form
        if qid is None:
            new_id_text = (
                self.quest_editor_panel.new_questinfo_form.quest_id_edit.text().strip()
            )
            if new_id_text.isdigit():
                qid = int(new_id_text)

        if qid is None:
            QMessageBox.warning(
                self,
                "Delete Quest",
                "Select a quest in the list OR enter a quest ID in the New Quest form.",
            )
            return

        # Confirm with user
        reply = QMessageBox.question(
            self,
            "Delete Quest",
            f"Delete quest {qid} from all loaded XML files?\n\n"
            "A .bak backup will be created next to each XML before changes.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        messages: list[str] = []

        def delete_from(name: str, tree, root, path: str | None):
            if tree is None or root is None or not path:
                messages.append(f"{name}: not loaded, skipping.")
                return

            # Backup original file
            backup(path)

            node = root.find(f"./imgdir[@name='{qid}']")
            if node is not None:
                root.remove(node)
                save_xml(tree, path)
                messages.append(f"{name}: removed quest {qid}.")
            else:
                messages.append(f"{name}: quest {qid} not present.")

        # Delete from each loaded XML
        delete_from("QuestInfo", self.questinfo_tree, self.questinfo_root, self.questinfo_path)
        delete_from("Check", self.check_tree, self.check_root, self.check_path)
        delete_from("Act", self.act_tree, self.act_root, self.act_path)

        # If we just deleted the current base quest, clear it
        if self.current_base_quest_id == qid:
            self.current_base_quest_id = None
            self._clear_base_forms()
            self._clear_new_forms()

        # Refresh quest list from updated QuestInfo root
        self._populate_quest_list()

        QMessageBox.information(self, "Delete Quest", "\n".join(messages))


    def _on_preview_ids(self):
        QMessageBox.information(
            self,
            "Not implemented yet",
            "Preview IDs behavior will be implemented later.",
        )
