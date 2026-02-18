from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QCheckBox, QComboBox, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPainter, QRadialGradient, QColor, QBrush, QPixmap
import os

# Importiere die neuen Hardware-Funktionen
from functions.functions import (run_command, open_app, open_link, 
                                 check_nvidia_status, install_nvidia, get_resource_path)
from functions.translations import TRANSLATIONS
from functions.system_info import get_sys_info
from functions.config_manager import load_config, save_config

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VeloxOS Welcome")
        self.setFixedSize(920, 600)
        
        # Einstellungen laden
        config = load_config()
        self.current_lang = config["language"]
        self.start_enabled = config["autostart"]

        self.main_container = QWidget()
        self.setCentralWidget(self.main_container)
        self.main_container.setObjectName("centralWidget")
        
        self.root_layout = QHBoxLayout(self.main_container)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        self.init_ui()

    def is_live_system(self):
        """ Prüft, ob wir uns im Miso Live-System befinden """
        return os.path.exists("/run/miso/bootmnt")

    def init_ui(self):
        if hasattr(self, 'sidebar'): self.sidebar.deleteLater()
        if hasattr(self, 'content_area'): self.content_area.deleteLater()

        lang = TRANSLATIONS[self.current_lang]
        sys_data = get_sys_info()
        nvidia_state = check_nvidia_status() # 0: Keine, 1: Braucht Treiber, 2: OK

        # --- SIDEBAR (Links) ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(25, 40, 25, 30)

        logo_label = QLabel()
        # Wichtig: Nutze das PNG für linuxdeploy Kompatibilität
        pixmap = QPixmap(get_resource_path("assets/VeloxOS-Welcome.png"))
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaledToHeight(100, Qt.TransformationMode.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo_label)

        sidebar_desc = QLabel(lang["subtitle"])
        sidebar_desc.setObjectName("sidebarDesc")
        sidebar_desc.setWordWrap(True)
        sidebar_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(sidebar_desc)

        # System Info Box
        sidebar_layout.addSpacing(20)
        info_frame = QFrame()
        info_frame.setObjectName("sysInfoBox")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(8)
        
        specs = [
            ("OS", sys_data["os"]),
            ("CPU", sys_data["cpu"]),
            ("GPU", sys_data["gpu"]),
            ("RAM", sys_data["ram"]),
            ("Kern", sys_data["kernel"])
        ]
        
        for label, value in specs:
            row = QLabel(f"<b>{label}:</b><br>{value}")
            row.setObjectName("sysInfoText")
            row.setWordWrap(True) 
            info_layout.addWidget(row)
        
        sidebar_layout.addWidget(info_frame)
        sidebar_layout.addStretch()

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Deutsch"])
        self.lang_combo.setCurrentIndex(0 if self.current_lang == "en" else 1)
        self.lang_combo.currentIndexChanged.connect(self.update_settings)
        sidebar_layout.addWidget(self.lang_combo)
        
        sidebar_layout.addSpacing(10)

        self.autostart_cb = QCheckBox(lang["autostart"])
        self.autostart_cb.setChecked(self.start_enabled)
        self.autostart_cb.toggled.connect(self.update_settings)
        sidebar_layout.addWidget(self.autostart_cb)

        # --- CONTENT AREA (Rechts) ---
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(40, 50, 40, 40)

        hero_title = QLabel(lang["title"])
        hero_title.setObjectName("heroTitle")
        self.content_layout.addWidget(hero_title)

        hero_desc = QLabel(
            "Thank you for choosing VeloxOS! This tool helps you to set up your system, "
            "install drivers and discover our community." if self.current_lang == "en" else
            "Danke, dass du dich für VeloxOS entschieden hast! Dieses Tool hilft dir dabei, "
            "dein System einzurichten, Treiber zu installieren und unsere Community zu entdecken."
        )
        hero_desc.setObjectName("heroDesc")
        hero_desc.setWordWrap(True)
        self.content_layout.addWidget(hero_desc)
        
        self.content_layout.addSpacing(40)

        columns_layout = QHBoxLayout()
        columns_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        columns_layout.setSpacing(20)
        
        # Spalte 1: Dokumentation & Community
        columns_layout.addLayout(self.create_column(lang["col_doc"], [
            (lang["btn_web"], lambda: open_link("https://veloxos.org")),
            (lang["btn_wiki"], lambda: open_link("https://wiki.veloxos.org")),
            ("GitHub", lambda: open_link("https://github.com/VeloxOS")),
        ], is_external=True))

        # Spalte 2: Einstellungen & Verwaltung
        columns_layout.addLayout(self.create_column(lang["col_set"], [
            (lang["btn_update"], lambda: open_app("pamac-manager --updates")),
            ("COSMIC Settings", lambda: open_app("cosmic-settings")),
            ("Kernel Manager", lambda: open_app("cachyos-kernel-manager")),
        ]))

        # Spalte 3: Installation & Optimierung
        # Hier bauen wir die Logik für NVIDIA und den Installer ein
        install_buttons = []
        
        # NVIDIA Logik
        if nvidia_state == 1:
            # Karte gefunden, aber Treiber fehlen (GELBER BUTTON wie in Yad)
            btn_text = "➊ Install NVIDIA Drivers" if self.current_lang == "en" else "NVIDIA Treiber installieren"
            install_buttons.append((btn_text, install_nvidia, "#ffcc00"))
        elif nvidia_state == 2:
            btn_text = "NVIDIA Drivers Active" if self.current_lang == "en" else "NVIDIA Treiber aktiv"
            install_buttons.append((btn_text, None, "#2ecc71"))
        
        # Installer nur im Live-System anzeigen
        if self.is_live_system():
            btn_text = "➋ Install VeloxOS" if self.current_lang == "en" else "VeloxOS Installieren"
            install_buttons.append((btn_text, lambda: run_command("sudo -E calamares"), "#00ff00"))
        
        # Standard Apps (Pamac) immer anzeigen
        install_buttons.append((lang["btn_apps"], lambda: open_app("pamac-manager"), None))

        columns_layout.addLayout(self.create_column(lang["col_inst"], install_buttons))

        self.content_layout.addLayout(columns_layout)
        self.content_layout.addStretch()

        # Footer (Socials)
        footer_socials = QHBoxLayout()
        socials = [
            ("discord.svg", "https://discord.gg/pgHSK8NGxG"),
            ("mastodon.svg", "https://mastodon.social"),
            ("x.svg", "https://x.com")
        ]

        for icon, link in socials:
            s_btn = QPushButton()
            s_btn.setObjectName("socialButton")
            s_btn.setIcon(QIcon(get_resource_path(f"assets/{icon}")))
            s_btn.setIconSize(QSize(22, 22))
            s_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            s_btn.clicked.connect(lambda checked, l=link: open_link(l))
            footer_socials.addWidget(s_btn)
        
        footer_socials.addStretch()
        self.content_layout.addLayout(footer_socials)

        self.root_layout.addWidget(self.sidebar)
        self.root_layout.addWidget(self.content_area)

    def update_settings(self):
        self.current_lang = "en" if self.lang_combo.currentIndex() == 0 else "de"
        self.start_enabled = self.autostart_cb.isChecked()
        save_config(self.current_lang, self.start_enabled)
        self.init_ui()

    def create_column(self, title_text, buttons, is_external=False):
        col_wrapper = QVBoxLayout()
        col_wrapper.setAlignment(Qt.AlignmentFlag.AlignTop)
        col_wrapper.setSpacing(10)
        lbl = QLabel(title_text)
        lbl.setObjectName("columnHeader")
        lbl.setMinimumHeight(20) 
        col_wrapper.addWidget(lbl)
        
        for item in buttons:
            text, func = item[0], item[1]
            custom_color = item[2] if len(item) > 2 else None
            
            btn = QPushButton(text)
            btn.setObjectName("actionButton")
            
            if custom_color:
                btn.setStyleSheet(f"background-color: {custom_color}; color: black; font-weight: bold;")
            
            if func:
                btn.clicked.connect(func)
            else:
                btn.setEnabled(False)

            if is_external:
                btn.setIcon(QIcon(get_resource_path("assets/external-link.svg")))
                btn.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
                btn.setIconSize(QSize(14, 14))
                
            col_wrapper.addWidget(btn)
        return col_wrapper

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QRadialGradient(self.width()*0.6, self.height()/2, self.width()*0.8)
        gradient.setColorAt(0.0, QColor(0, 170, 255, 45))
        gradient.setColorAt(1.0, QColor(11, 14, 20, 255))
        painter.fillRect(self.rect(), QBrush(gradient))