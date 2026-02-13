import subprocess
import webbrowser
import sys
import os
import socket

def has_internet():
    """ Prüft kurz, ob eine Verbindung zu einem DNS-Server möglich ist """
    try:
        # Versucht Google DNS auf Port 53 zu erreichen
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except socket.error:
        return False
    
def get_terminal():
    """ Findet das passende Terminal für das aktuelle System """
    terminals = ['cosmic-term', 'konsole', 'xfce4-terminal', 'gnome-terminal', 'alacritty']
    for term in terminals:
        if subprocess.run(['which', term], capture_output=True).returncode == 0:
            return term
    return 'xterm'

def run_command(command):
    chosen_term = get_terminal()
    # COSMIC-Term nutzt '--', fast alle anderen '-e'
    flag = '--' if chosen_term == 'cosmic-term' else '-e'
    subprocess.Popen([chosen_term, flag, 'bash', '-c', f"{command}; echo 'Fertig! Taste drücken...'; read -n1"])

def open_app(command):
    try:
        subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Fehler beim Starten der App: {e}")

def open_link(url):
    webbrowser.open(url)

def check_nvidia_status():
    try:
        has_gpu = subprocess.run("lspci | grep -i nvidia", shell=True, capture_output=True).returncode == 0
        if not has_gpu:
            return 0
        is_loaded = subprocess.run("lsmod | grep -i nvidia", shell=True, capture_output=True).returncode == 0
        return 2 if is_loaded else 1
    except:
        return 0

def install_nvidia():
    if not has_internet():
        # Wir nutzen das Terminal, um dem User die Fehlermeldung zu zeigen
        chosen_term = get_terminal()
        flag = '--' if chosen_term == 'cosmic-term' else '-e'
        subprocess.Popen([chosen_term, flag, 'bash', '-c', 
            "echo 'FEHLER: Keine Internetverbindung gefunden!'; "
            "echo 'Bitte verbinde dich mit dem WLAN/LAN, um Treiber zu laden.'; "
            "read -n1"])
        return

    script_path = get_resource_path("scripts/install_nvidia.sh")
    chosen_term = get_terminal()
    flag = '--' if chosen_term == 'cosmic-term' else '-e'
    cmd = f"pkexec bash {script_path}"
    subprocess.Popen([chosen_term, flag, 'bash', '-c', f"{cmd}; echo 'Fertig! Bitte neustarten oder Installation starten.'; read -n1"])

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)