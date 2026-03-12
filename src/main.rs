mod system_info;
mod callbacks;
mod config;

use std::path::Path;
use std::process::Command;
slint::include_modules!();

fn is_live_session() -> bool {
    Path::new("/run/archiso/").exists() ||
        std::env::var("USER").unwrap_or_default() == "veloxos"
}

fn main() -> Result<(), slint::PlatformError> {
    let ui = AppWindow::new()?;
    let sys = system_info::get_system_info();
    let cfg = config::load_config();
    let is_live = is_live_session();

    // --- 1. System-Daten an UI binden ---
    ui.set_os_info(sys.os.into());
    ui.set_cpu_info(sys.cpu.into());
    ui.set_gpu_info(sys.gpu_clean.into());
    ui.set_ram_info(sys.ram.into());
    ui.set_kernel_info(sys.kernel.into());
    ui.set_show_install_button(is_live);

    // --- 2. Config-Daten an UI binden ---
    ui.set_active_lang(cfg.language.clone().into());
    ui.set_autostart_enabled(cfg.autostart);

    // --- 3. NVIDIA-Erkennung ---
    let nvidia_status = {
        let has_nvidia_hwd = sys.gpu_raw.to_lowercase().contains("nvidia");
        let has_official_driver = Path::new("/proc/driver/nvidia/version").exists();
        let is_nouveau_active = Command::new("sh")
            .arg("-c").arg("lsmod | grep -q nouveau")
            .status().map(|s| s.success()).unwrap_or(false);

        if !has_nvidia_hwd { 0 }
        else if has_official_driver { 2 }
        else if is_nouveau_active { 1 }
        else { 1 }
    };

    ui.set_is_nvidia_needed(nvidia_status == 1);
    ui.set_nvidia_active(nvidia_status == 2);

    // --- 4. Callbacks ---

    ui.on_open_link(|u| callbacks::open_link(u.as_str()));
    ui.on_open_app(|a| callbacks::open_app(a.as_str()));

    ui.on_install_nvidia(|| {
        callbacks::install_nvidia();
    });

    // Dieser Callback ist NUR für Calamares
    ui.on_start_installer(|| {
        callbacks::start_calamares();
    });

    ui.on_toggle_autostart(|e| {
        callbacks::toggle_autostart(e);
        let mut c = config::load_config();
        c.autostart = e;
        config::save_config(&c);
    });

    let ui_handle = ui.as_weak();
    ui.on_change_lang(move |lang| {
        let mut c = config::load_config();
        c.language = lang.to_string();
        config::save_config(&c);
        if let Some(ui) = ui_handle.upgrade() {
            ui.set_active_lang(lang);
        }
    });

    ui.run()
}