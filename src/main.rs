mod system_info; mod callbacks; mod config;
use std::path::Path;
slint::include_modules!();

fn main() -> Result<(), slint::PlatformError> {
    let ui = AppWindow::new()?;
    let sys = system_info::get_system_info();
    let cfg = config::load_config();

    // Initiales Setzen der Daten
    ui.set_os_info(sys.os.into());
    ui.set_cpu_info(sys.cpu.into());
    ui.set_gpu_info(sys.gpu_clean.into());
    ui.set_ram_info(sys.ram.into());
    ui.set_kernel_info(sys.kernel.into());
    ui.set_active_lang(cfg.language.clone().into());
    ui.set_autostart_enabled(cfg.autostart);

    let nvidia = if !sys.gpu_raw.to_lowercase().contains("nvidia") { 0 }
    else if Path::new("/proc/driver/nvidia").exists() { 2 } else { 1 };
    ui.set_is_nvidia_needed(nvidia == 1);
    ui.set_nvidia_active(nvidia == 2);

    // Callbacks
    ui.on_open_link(|u| callbacks::open_link(u.as_str()));
    ui.on_open_app(|a| callbacks::open_app(a.as_str()));
    ui.on_install_nvidia(|| callbacks::run_in_term("pkexec bash /usr/share/welcome-veloxos/scripts/install_nvidia.sh"));
    ui.on_start_installer(|| callbacks::run_in_term("pkexec calamares"));

    ui.on_toggle_autostart(|e| {
        callbacks::toggle_autostart(e);
        let mut c = config::load_config();
        c.autostart = e;
        config::save_config(&c);
    });

    // WICHTIG: Live-Update der Sprache in der UI
    let ui_handle = ui.as_weak();
    ui.on_change_lang(move |lang| {
        let mut c = config::load_config();
        c.language = lang.to_string();
        config::save_config(&c);
        if let Some(ui) = ui_handle.upgrade() {
            ui.set_active_lang(lang); // Hier wird die UI getriggert!
        }
    });

    ui.run()
}