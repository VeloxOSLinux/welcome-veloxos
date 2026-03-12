use sysinfo::System;
use std::process::Command;

pub struct SysData {
    pub os: String, pub cpu: String, pub ram: String,
    pub kernel: String, pub gpu_raw: String, pub gpu_clean: String,
}

pub fn get_system_info() -> SysData {
    let mut sys = System::new_all();
    sys.refresh_all();
    let os = System::name().unwrap_or_else(|| "VeloxOS".to_string());
    let kernel = System::kernel_version().unwrap_or_else(|| "Unknown".to_string());
    let cpu = sys.cpus().first().map(|c| c.brand()).unwrap_or("Unknown").trim().to_string();
    let ram = format!("{:.1} GB", sys.total_memory() as f64 / 1024.0 / 1024.0 / 1024.0);
    let gpu_raw = Command::new("sh").arg("-c").arg("lspci | grep -E 'VGA|3D' | cut -d ':' -f3").output()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string()).unwrap_or_default();
    let gpu_clean = gpu_raw.replace("Corporation", "").replace("Advanced Micro Devices, Inc.", "").replace("[AMD/ATI]", "").trim().to_string();
    SysData { os, cpu, ram, kernel, gpu_raw, gpu_clean }
}