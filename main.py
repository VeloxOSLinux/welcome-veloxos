import sys
import os
from PyQt6.QtWidgets import QApplication
from gui.gui import WelcomeWindow

def load_stylesheet(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def main():
    app = QApplication(sys.argv)
    
    # Pfad zur style.qss ermitteln
    base_dir = os.path.dirname(__file__)
    style_path = os.path.join(base_dir, "style", "style.qss")
    
    # Stylesheet laden und anwenden
    app.setStyleSheet(load_stylesheet(style_path))
    
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()