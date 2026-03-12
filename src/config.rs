use serde::{Serialize, Deserialize};
use std::{fs, env};

#[derive(Serialize, Deserialize, Clone)]
pub struct AppConfig { pub language: String, pub autostart: bool }
impl Default for AppConfig { fn default() -> Self { Self { language: "en".to_string(), autostart: true } } }

pub fn load_config() -> AppConfig {
    let path = format!("{}/.veloxos_welcome.json", env::var("HOME").unwrap_or_default());
    fs::read_to_string(path).map(|c| serde_json::from_str(&c).unwrap_or_default()).unwrap_or_default()
}

pub fn save_config(config: &AppConfig) {
    let path = format!("{}/.veloxos_welcome.json", env::var("HOME").unwrap_or_default());
    if let Ok(j) = serde_json::to_string_pretty(config) { let _ = fs::write(path, j); }
}