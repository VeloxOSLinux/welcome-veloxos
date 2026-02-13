#!/bin/bash

# Prüfen ob chwd installiert ist
if ! command -v chwd &> /dev/null; then
    echo "CHWD nicht gefunden! Installiere chwd..."
    sudo pacman -Sy --noconfirm chwd
fi

echo "Starte Hardware-Erkennung und Treiber-Installation..."

# chwd Logik:
# -a: auto install
# pci: pci bus
# free_nvidia: Nutze 'free' (open source) oder 'nonfree_nvidia' (proprietär)
# Da du volle Gaming-Performance willst, nutzen wir 'nonfree_nvidia'
sudo chwd -a pci nonfree_nvidia 0300

# Falls chwd fehlschlägt oder nicht greift, forcieren wir die Pakete 
# für den CachyOS-Bore Kernel, die du im yad Skript hattest
if [ $? -ne 0 ]; then
    echo "CHWD fehlgeschlagen. Versuche manuellen Fallback..."
    sudo pacman -S --noconfirm nvidia-cachyos-bore nvidia-utils lib32-nvidia-utils nvidia-settings
fi

# Kernel-Module für Wayland (KDE/GNOME) aktivieren
if ! grep -q "nvidia-drm.modeset=1" /etc/default/grub; then
    echo "Aktiviere NVIDIA Modesetting für Wayland..."
    sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="nvidia-drm.modeset=1 /' /etc/default/grub
    sudo grub-mkconfig -o /boot/grub/grub.cfg
fi