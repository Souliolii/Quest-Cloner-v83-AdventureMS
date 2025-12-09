# main.py
import os
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from app.ui.main_window import QuestEditorWindow


def load_stylesheet(app: QApplication) -> None:
    """
    Load the global dark theme stylesheet from theme.qss.

    Works both:
      - when running from source
      - when running from a PyInstaller-built EXE
    """
    # When running under PyInstaller, sys._MEIPASS points to the temp bundle dir.
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    theme_path = os.path.join(base_dir, "theme.qss")

    if not os.path.exists(theme_path):
        # Fallback: try a resources folder if you ever move it.
        alt_path = os.path.join(base_dir, "resources", "theme.qss")
        if os.path.exists(alt_path):
            theme_path = alt_path
        else:
            # No stylesheet found, just run with default Qt theme.
            return

    try:
        with open(theme_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        # Fail silently; the app should still run without the theme.
        print(f"Failed to load stylesheet: {e}", file=sys.stderr)


def main():
    app = QApplication(sys.argv)

    # If you add an app icon later, you can uncomment this
    # icon_path = os.path.join(os.path.dirname(__file__), "resources", "icons", "app_icon.png")
    # if os.path.exists(icon_path):
    #     app.setWindowIcon(QIcon(icon_path))

    load_stylesheet(app)

    window = QuestEditorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
