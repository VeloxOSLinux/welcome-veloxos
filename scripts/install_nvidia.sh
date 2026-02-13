#!/bin/bash

# Sprachprüfung (Prüft, ob 'de' in der System-Sprache vorkommt)
if [[ $LANG == de* ]]; then
    MSG_SYNC="Synchronisiere Repositories..."
    MSG_CHWD="CHWD wird nachinstalliert..."
    MSG_DETECT="Starte Hardware-Erkennung..."
    MSG_FALLBACK="CHWD fehlgeschlagen. Starte manuellen Fallback..."
    MSG_GRUB="Konfiguriere GRUB für NVIDIA Modesetting..."
    MSG_KNP="Aktualisiere Kernel-Abbilder (mkinitcpio)..."
    MSG_DONE="Installation abgeschlossen! Bitte das System neu starten."
else
    MSG_SYNC="Synchronizing repositories..."
    MSG_CHWD="Installing CHWD..."
    MSG_DETECT="Starting hardware detection..."
    MSG_FALLBACK="CHWD failed. Starting manual fallback..."
    MSG_GRUB="Configuring GRUB for NVIDIA modesetting..."
    MSG_KNP="Updating kernel images (mkinitcpio)..."
    MSG_DONE="Installation complete! Please restart your system."
fi

echo "--------------------------------------------------"
echo "$MSG_SYNC"
pacman -Sy --noconfirm

if ! command -v chwd &> /dev/null; then
    echo "$MSG_CHWD"
    pacman -S --noconfirm chwd
fi

echo "$MSG_DETECT"
chwd -a pci nonfree_nvidia 0300

if [ $? -ne 0 ]; then
    echo "$MSG_FALLBACK"
    pacman -S --noconfirm nvidia-cachyos-bore nvidia-utils lib32-nvidia-utils nvidia-settings
fi

if [ -f /etc/default/grub ] && command -v grub-mkconfig &> /dev/null; then
    if ! grep -q "nvidia-drm.modeset=1" /etc/default/grub; then
        echo "$MSG_GRUB"
        sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="nvidia-drm.modeset=1 /' /etc/default/grub
        grub-mkconfig -o /boot/grub/grub.cfg
    fi
fi

echo "$MSG_KNP"
mkinitcpio -P

echo "--------------------------------------------------"
echo "$MSG_DONE"