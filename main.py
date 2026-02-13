import sys
import os
from PyQt6.QtWidgets import QApplication
from gui.gui import WelcomeWindow
from functions.functions import get_resource_path

def load_stylesheet(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def main():
    app = QApplication(sys.argv)
    
    style_path = get_resource_path(os.path.join("style", "style.qss"))
    
    app.setStyleSheet(load_stylesheet(style_path))
    
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()