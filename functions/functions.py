import subprocess
import webbrowser
import sys
import os
import socket


def get_terminal():
    # Wir prüfen zusätzlich auf 'cosmic-terminal'
    terminals = ['cosmic-term', 'cosmic-terminal', 'konsole', 'xfce4-terminal', 'alacritty']
    for term in terminals:
        if subprocess.run(['which', term], capture_output=True).returncode == 0:
            return term
    return 'xterm'


def run_safe_process(args):
    """ Führt einen Prozess aus und bereinigt die Library-Pfade für das AppImage """
    env = os.environ.copy()
    # Entferne AppImage-spezifische Pfade, damit System-Bibliotheken genutzt werden
    if "LD_LIBRARY_PATH" in env:
        # Wir filtern die Pfade, die auf /tmp/.mount_... (das AppImage) zeigen
        paths = env["LD_LIBRARY_PATH"].split(":")
        new_paths = [p for p in paths if not p.startswith("/tmp/.mount_")]
        env["LD_LIBRARY_PATH"] = ":".join(new_paths)

    return subprocess.Popen(args, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_command(command):
    chosen_term = get_terminal()
    flag = '--' if 'cosmic' in chosen_term else '-e'
    # Wir nutzen run_safe_process für den Terminal-Start
    run_safe_process([chosen_term, flag, 'bash', '-c', f"{command}; echo 'Fertig! Taste drücken...'; read -n1"])


def open_app(command):
    # Wichtig: Wir nutzen shell=True ODER übergeben die Argumente sauber als Liste
    # Damit 'cachyos-settings-manager' gefunden wird, nutzen wir 'sh -c'
    run_safe_process(['sh', '-c', f"{command} &"])


def open_link(url):
    webbrowser.open(url)


def check_nvidia_status():
    """
    0 = Keine Nvidia Karte
    1 = Karte da, aber Treiber fehlen
    2 = Karte da und Treiber aktiv
    """
    try:
        has_gpu = subprocess.run("lspci | grep -i nvidia", shell=True, capture_output=True).returncode == 0
        if not has_gpu:
            return 0

        is_loaded = subprocess.run("lsmod | grep -i nvidia", shell=True, capture_output=True).returncode == 0
        return 2 if is_loaded else 1
    except:
        return 0


def has_internet():
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except:
        return False


def get_resource_path(relative_path):
    """ Ermöglicht Zugriff auf Assets im AppImage und Dev-Modus """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)

def install_nvidia():
    if not has_internet():
        run_command("echo 'FEHLER: Kein Internet!'")
        return

    script_path = get_resource_path("scripts/install_nvidia.sh")
    chosen_term = get_terminal()
    flag = '--' if 'cosmic' in chosen_term else '-e'

    # pkexec braucht eine saubere Umgebung
    cmd = f"pkexec bash {script_path}"
    run_safe_process([chosen_term, flag, 'bash', '-c', f"{cmd}; echo 'Fertig!'; read -n1"])