import subprocess
import webbrowser

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