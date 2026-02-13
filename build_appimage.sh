#!/bin/bash
set -e

echo "Installiere Konvertierungs-Tools..."
sudo apt-get update && sudo apt-get install -y imagemagick

echo "Bündle VeloxOS Welcome mit PyInstaller..."
pip install pyinstaller psutil GPUtil PyQt6 --quiet

python3 -m PyInstaller --noconfirm --onefile --windowed \
            --add-data "assets:assets" \
            --add-data "functions:functions" \
            --add-data "gui:gui" \
            --add-data "style:style" \
            --name "VeloxOS-Welcome" \
            main.py

# Icon für linuxdeploy konvertieren (linuxdeploy braucht PNG oder SVG)
echo "Konvertiere Icon für AppImage..."
convert assets/logo.webp assets/logo.png

if [ ! -f linuxdeploy-x86_64.AppImage ]; then
    echo "Lade linuxdeploy herunter..."
    wget -c https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
    chmod +x linuxdeploy-x86_64.AppImage
fi

export OUTPUT="VeloxOS-Welcome-x86_64.AppImage"
export APPIMAGE_EXTRACT_AND_RUN=1

./linuxdeploy-x86_64.AppImage --executable dist/VeloxOS-Welcome \
    --icon-file assets/logo.png \
    --appdir AppDir \
    --create-desktop-file \
    --output appimage

# Aufräumen
rm assets/logo.png