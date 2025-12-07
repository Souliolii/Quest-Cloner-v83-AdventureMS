# quest_helper_gui.py
import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
import xml.etree.ElementTree as ET

# Import your existing helper functions / constants
import quest_helper  # this is your current script file

SCRIPT_DIR = quest_helper.get_script_dir()
QUESTINFO_PATH = os.path.join(SCRIPT_DIR, "QuestInfo.img.xml")


def load_questinfo():
    """Load QuestInfo.img.xml and return (tree, root)."""
    if not os.path.isfile(QUESTINFO_PATH):
        raise FileNotFoundError(f"{QUESTINFO_PATH} not found.")
    tree = ET.parse(QUESTINFO_PATH)
    root = tree.getroot()
    return tree, root


def get_quest_node(root, quest_id: int):
    """Return the <imgdir name="ID"> node or None."""
    return root.find(f"./imgdir[@name='{quest_id}']")


def extract_quest_text(node):
    """Return (name, summary, rewardSummary) from a QuestInfo node."""
    if node is None:
        return ("<not found>", "", "")
    name = ""
    summary = ""
    reward = ""
    for child in node:
        if child.tag != "string":
            continue
        n = child.get("name")
        v = child.get("value", "")
        if n == "name":
            name = v
        elif n in ("summary", "0"):
            summary = v
        elif n == "rewardSummary":
            reward = v
    return (name, summary, reward)


class QuestHelperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maple Quest Helper - GUI")

        # Try to load QuestInfo on startup
        try:
            self.tree, self.qroot = load_questinfo()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load QuestInfo.img.xml:\n{e}")
            self.tree, self.qroot = None, None

        self.create_widgets()
        if self.qroot is not None:
            self.populate_listbox()

    def create_widgets(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        # Left side: listbox of quests
        left_frame = ttk.Frame(main)
        left_frame.grid(row=0, column=0, sticky="nswe", padx=(0, 10))
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=3)
        main.rowconfigure(0, weight=1)

        ttk.Label(left_frame, text="Quests in QuestInfo.img.xml").pack(anchor="w")

        self.quest_list = tk.Listbox(left_frame, width=30, height=25)
        self.quest_list.pack(fill="both", expand=True)
        self.quest_list.bind("<<ListboxSelect>>", self.on_list_select)

        # Top-right: ID inputs + buttons
        right_frame = ttk.Frame(main)
        right_frame.grid(row=0, column=1, sticky="nswe")
        right_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(1, weight=1)

        id_frame = ttk.Frame(right_frame)
        id_frame.grid(row=0, column=0, columnspan=2, sticky="we", pady=(0, 10))
        ttk.Label(id_frame, text="Base ID:").grid(row=0, column=0, sticky="e")
        self.base_id_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.base_id_var, width=10).grid(row=0, column=1, sticky="w", padx=(5, 15))

        ttk.Label(id_frame, text="New ID:").grid(row=0, column=2, sticky="e")
        self.new_id_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.new_id_var, width=10).grid(row=0, column=3, sticky="w", padx=5)

        ttk.Button(id_frame, text="Preview IDs", command=self.preview_ids).grid(row=0, column=4, padx=(10, 0))
        ttk.Button(id_frame, text="Clone Quest", command=self.clone_quest).grid(row=0, column=5, padx=(10, 0))

        # Middle-right: Base quest text
        base_frame = ttk.LabelFrame(right_frame, text="Base Quest (source)")
        base_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        right_frame.rowconfigure(1, weight=1)

        self.base_name = tk.Text(base_frame, height=2, wrap="word")
        self.base_summary = tk.Text(base_frame, height=5, wrap="word")
        self.base_reward = tk.Text(base_frame, height=3, wrap="word")

        ttk.Label(base_frame, text="Name:").pack(anchor="w")
        self.base_name.pack(fill="x", pady=(0, 5))
        ttk.Label(base_frame, text="Summary:").pack(anchor="w")
        self.base_summary.pack(fill="both", expand=True, pady=(0, 5))
        ttk.Label(base_frame, text="Reward Summary:").pack(anchor="w")
        self.base_reward.pack(fill="x")

        # Middle-right: New quest text (existing target)
        new_frame = ttk.LabelFrame(right_frame, text="Target Quest (current/new)")
        new_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))

        self.new_name = tk.Text(new_frame, height=2, wrap="word")
        self.new_summary = tk.Text(new_frame, height=5, wrap="word")
        self.new_reward = tk.Text(new_frame, height=3, wrap="word")

        ttk.Label(new_frame, text="Name:").pack(anchor="w")
        self.new_name.pack(fill="x", pady=(0, 5))
        ttk.Label(new_frame, text="Summary:").pack(anchor="w")
        self.new_summary.pack(fill="both", expand=True, pady=(0, 5))
        ttk.Label(new_frame, text="Reward Summary:").pack(anchor="w")
        self.new_reward.pack(fill="x")

        # Bottom: override inputs for new quest text
        override_frame = ttk.LabelFrame(right_frame, text="Overrides for New Quest (optional)")
        override_frame.grid(row=2, column=0, columnspan=2, sticky="we", pady=(10, 0))

        ttk.Label(override_frame, text="New Name:").grid(row=0, column=0, sticky="e")
        self.override_name = tk.Entry(override_frame, width=50)
        self.override_name.grid(row=0, column=1, sticky="we", padx=5)

        ttk.Label(override_frame, text="New Summary:").grid(row=1, column=0, sticky="ne")
        self.override_summary = tk.Text(override_frame, height=3, wrap="word")
        self.override_summary.grid(row=1, column=1, sticky="we", padx=5, pady=2)

        ttk.Label(override_frame, text="New Reward Summary:").grid(row=2, column=0, sticky="ne")
        self.override_reward = tk.Text(override_frame, height=2, wrap="word")
        self.override_reward.grid(row=2, column=1, sticky="we", padx=5, pady=2)

        override_frame.columnconfigure(1, weight=1)

    def populate_listbox(self):
        """Fill the listbox with ID: name from QuestInfo."""
        self.quest_list.delete(0, tk.END)
        for imgdir in self.qroot.findall("./imgdir"):
            qid = imgdir.get("name")
            name, _, _ = extract_quest_text(imgdir)
            display = f"{qid}: {name}"
            self.quest_list.insert(tk.END, display)

    def on_list_select(self, event):
        """When you click a quest in the list, fill Base ID and preview."""
        if not self.quest_list.curselection():
            return
        idx = self.quest_list.curselection()[0]
        line = self.quest_list.get(idx)
        qid = line.split(":", 1)[0].strip()
        self.base_id_var.set(qid)
        self.preview_ids()

    def preview_ids(self):
        """Show base quest text and (if exists) target quest text."""
        if self.qroot is None:
            return

        base_id_str = self.base_id_var.get().strip()
        new_id_str = self.new_id_var.get().strip() or base_id_str

        if not base_id_str.isdigit() or not new_id_str.isdigit():
            messagebox.showwarning("Invalid IDs", "Base ID and New ID must be numbers.")
            return

        base_id = int(base_id_str)
        new_id = int(new_id_str)

        base_node = get_quest_node(self.qroot, base_id)
        new_node = get_quest_node(self.qroot, new_id)

        bname, bsum, brew = extract_quest_text(base_node)
        nname, nsum, nrew = extract_quest_text(new_node)

        self._set_text_widget(self.base_name, bname)
        self._set_text_widget(self.base_summary, bsum)
        self._set_text_widget(self.base_reward, brew)

        self._set_text_widget(self.new_name, nname)
        self._set_text_widget(self.new_summary, nsum)
        self._set_text_widget(self.new_reward, nrew)

    def _set_text_widget(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text)
        widget.config(state="disabled")

    def clone_quest(self):
        """Run your existing clone logic for all XML files, using overrides."""
        base_id_str = self.base_id_var.get().strip()
        new_id_str = self.new_id_var.get().strip()

        if not base_id_str.isdigit() or not new_id_str.isdigit():
            messagebox.showwarning("Invalid IDs", "Base ID and New ID must be numbers.")
            return

        base_id = int(base_id_str)
        new_id = int(new_id_str)

        # Get optional overrides
        new_name = self.override_name.get().strip()
        new_summary = self.override_summary.get("1.0", tk.END).strip()
        new_reward = self.override_reward.get("1.0", tk.END).strip()

        # Loop over all files like in your console script
        messages = []
        for fname in quest_helper.FILES:
            path = os.path.join(SCRIPT_DIR, fname)
            if not os.path.isfile(path):
                messages.append(f"[INFO] {fname} not found, skipping.")
                continue

            # Backup first
            backup_path = path + ".bak"
            shutil.copy2(path, backup_path)

            tree = ET.parse(path)
            root = tree.getroot()

            new_node, msg = quest_helper.clone_node(root, base_id, new_id)
            messages.append(f"{fname}: {msg}")

            if fname == "QuestInfo.img.xml" and new_node is not None:
                quest_helper.update_questinfo_text(new_node, new_name, new_summary, new_reward)
                messages.append("    QuestInfo text updated.")

            tree.write(path, encoding="utf-8", xml_declaration=True)

        # Reload QuestInfo so the list and preview are accurate
        try:
            self.tree, self.qroot = load_questinfo()
            self.populate_listbox()
            self.preview_ids()
        except Exception:
            pass

        messagebox.showinfo("Clone complete", "\n".join(messages))


if __name__ == "__main__":
    root = tk.Tk()
    app = QuestHelperGUI(root)
    root.mainloop()
