use std::process::{Command, Stdio};
use std::{env, fs, path::Path};

const NVIDIA_SCRIPT: &str = include_str!("../scripts/install_nvidia.sh");

fn create_safe_cmd(prog: &str) -> Command {
    let mut cmd = Command::new(prog);
    if let Ok(lp) = env::var("LD_LIBRARY_PATH") {
        let filtered = lp.split(':')
            .filter(|p| !p.starts_with("/tmp/.mount_"))
            .collect::<Vec<_>>()
            .join(":");
        cmd.env("LD_LIBRARY_PATH", filtered);
    }
    cmd
}

fn get_term() -> String {
    let ts = ["cosmic-term", "konsole", "xfce4-terminal", "alacritty", "xterm"];
    ts.iter().find(|&&t| Command::new("which").arg(t).stdout(Stdio::null()).status().map(|s| s.success()).unwrap_or(false))
        .map(|s| s.to_string()).unwrap_or("xterm".to_string())
}

pub fn open_link(url: &str) {
    let _ = create_safe_cmd("xdg-open").arg(url).spawn();
}

pub fn open_app(cmd: &str) {
    let _ = create_safe_cmd("sh").arg("-c").arg(format!("{} &", cmd)).spawn();
}

pub fn install_nvidia() {
    let t = get_term();
    let f = if t.contains("cosmic") { "--" } else { "-e" };
    let _ = create_safe_cmd(&t).arg(f).arg("pkexec").arg("bash").arg("-c").arg(NVIDIA_SCRIPT).spawn();
}

pub fn start_calamares() {
    let _ = create_safe_cmd("pkexec").arg("calamares").spawn();
}

pub fn _run_in_term(c: &str) {
    let t = get_term();
    let f = if t.contains("cosmic") { "--" } else { "-e" };
    let _ = create_safe_cmd(&t).arg(f).arg("bash").arg("-c").arg(format!("{}; echo 'Fertig!'; read -n1", c)).spawn();
}

pub fn toggle_autostart(enabled: bool) {
    let h = env::var("HOME").unwrap_or_default();
    let dp = format!("{}/.config/autostart/welcome-veloxos.desktop", h);
    let sp = "/etc/xdg/autostart/welcome-veloxos.desktop";
    if !Path::new(&dp).exists() && Path::new(sp).exists() { let _ = fs::copy(sp, &dp); }
    if let Ok(c) = fs::read_to_string(&dp) {
        let nl: Vec<String> = c.lines().map(|l| if l.starts_with("Hidden=") { format!("Hidden={}", !enabled) } else { l.to_string() }).collect();
        let _ = fs::write(&dp, nl.join("\n"));
    }
}