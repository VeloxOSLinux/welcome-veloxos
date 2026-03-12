# Maintainer: timo <admin@veloxos.org>
pkgname=welcome-veloxos
pkgver=1.0.0
pkgrel=1
pkgdesc="Rust-based Welcome Tool for VeloxOS"
arch=('x86_64') # Rust kompiliert für spezifische Architekturen
url="https://github.com/VeloxOSLinux/welcome-veloxos"
license=('GPL3')

# Benötigte Programme zur Laufzeit
depends=('slint-cpp' 'velox-package-manager' 'manjaro-settings-manager' 'calamares')

# Benötigt zum Bauen
makedepends=('git' 'rust' 'cargo')

source=("${pkgname}::git+https://github.com/VeloxOSLinux/welcome-veloxos.git")
sha256sums=('SKIP')

prepare() {
  cd "${srcdir}/${pkgname}"
  # Cargo-Lockfile/Abhängigkeiten vorbereiten
  cargo fetch --locked --target "$CARCH-unknown-linux-gnu"
}

build() {
  cd "${srcdir}/${pkgname}"
  # Das Tool im Release-Modus bauen
  export SLINT_NO_UI=1 # Falls auf dem Build-Server kein X11 ist
  cargo build --release --frozen
}

package() {
  cd "${srcdir}/${pkgname}"

  # 1. Die Binary installieren
  install -Dm755 "target/release/welcome-veloxos" "${pkgdir}/usr/bin/welcome-veloxos"

  # 2. Desktop-Datei installieren
  install -Dm644 "welcome-veloxos.desktop" "${pkgdir}/usr/share/applications/welcome-veloxos.desktop"

  # 3. Autostart (optional, falls es bei jedem Boot kommen soll)
  install -Dm644 "welcome-veloxos.desktop" "${pkgdir}/etc/xdg/autostart/welcome-veloxos.desktop"

  # 4. Icon installieren (Pfad anpassen, falls dein Icon anders heißt)
  if [ -f "assets/logo.png" ]; then
    install -Dm644 "assets/logo.png" "${pkgdir}/usr/share/icons/hicolor/512x512/apps/welcome-veloxos.png"
  fi
}
