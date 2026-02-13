#!/bin/bash
set -e # Abbrechen bei Fehlern

echo "Bündle VeloxOS Welcome mit PyInstaller..."
pip install pyinstaller psutil GPUtil PyQt6 --quiet

# PyInstaller erstellt eine einzelne Binärdatei
# --add-data "Quelle:Ziel" (Unter Linux ist der Trenner ein Doppelpunkt)
python3 -m PyInstaller --noconfirm --onefile --windowed \
            --add-data "assets:assets" \
            --add-data "functions:functions" \
            --add-data "gui:gui" \
            --add-data "style:style" \
            --name "VeloxOS-Welcome" \
            main.py

if [ ! -f linuxdeploy-x86_64.AppImage ]; then
    echo "Lade linuxdeploy herunter..."
    wget -c https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
    chmod +x linuxdeploy-x86_64.AppImage
fi

# Wir brauchen ein Icon im PNG oder SVG Format für linuxdeploy. 
# Falls du nur .webp hast, wird linuxdeploy meckern. 
# Ich nutze hier dein logo.webp - falls es fehlschlägt, konvertiere es zu .png
export OUTPUT="VeloxOS-Welcome-x86_64.AppImage"
export APPIMAGE_EXTRACT_AND_RUN=1

./linuxdeploy-x86_64.AppImage --executable dist/VeloxOS-Welcome \
    --icon-file assets/logo.webp \
    --appdir AppDir \
    --create-desktop-file \
    --output appimage