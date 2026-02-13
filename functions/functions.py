import subprocess
import webbrowser
import sys
import os

def run_command(command):
    # Öffnet ein Terminal und führt den Befehl aus
    # 'konsole' ist Standard bei KDE/Manjaro, sonst 'xfce4-terminal' o.ä.
    subprocess.Popen(['konsole', '-e', 'bash', '-c', f"{command}; echo 'Fertig! Beliebige Taste drücken...'; read -n1"])

def open_app(command):
    # Startet eine GUI App im Hintergrund
    subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def open_link(url):
    webbrowser.open(url)

def install_nvidia():
    # Beispielbefehl für CachyOS Treiber auf Manjaro-Basis
    run_command("sudo pacman -S --needed nvidia-cachyos-dkms nvidia-settings lib32-nvidia-utils")

def get_resource_path(relative_path):
    """ Ermöglicht den Zugriff auf Assets sowohl im Dev-Modus als auch im PyInstaller-Bundle """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)