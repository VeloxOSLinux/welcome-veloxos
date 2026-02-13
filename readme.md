# VeloxOS Welcome Tool 🚀

Welcome to the official **VeloxOS Welcome** application. This tool is designed to provide a seamless post-installation experience for VeloxOS users, helping them to configure their system, install essential drivers, and join the community.

![VeloxOS Banner](https://raw.githubusercontent.com/VeloxOS/assets/logo.webp) 

## ✨ Features

* **System Information**: Real-time display of your Hardware (CPU, GPU, RAM) and Kernel version.
* **One-Click Updates**: Easily trigger system updates via Pacman.
* **Driver Management**: Dedicated support for NVIDIA driver installation.
* **Software Center**: Quick access to the Pamac manager for app discovery.
* **Community Links**: Direct access to our Wiki, Website, Discord, and Social Media.
* **Multilingual Support**: Fully translated into English and German.
* **Custom UI**: Modern, dark-themed interface built with PyQt6 and custom QSS styling.

## 🛠️ Tech Stack

* **Language**: Python 3.12+
* **UI Framework**: PyQt6
* **Hardware Detection**: GPUtil, psutil
* **Styling**: Custom CSS/QSS with Radial Gradients

## 📥 Installation

To run this tool locally or for development, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/VeloxOS/welcome-veloxos.git](https://github.com/VeloxOS/welcome-veloxos.git)
   cd welcome-veloxos
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the app:**
   ```bash
   python main.py
   ```

## 📂 Project Structure

```
.
├── assets/                # Icons, logos, and images
├── functions/             # Backend logic (System info, config, translations)
├── gui/                   # UI definitions (PyQt6 classes)
├── style/                 # QSS stylesheets
├── .gitignore             # Files to be ignored by Git
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
└── .veloxos_welcome.json  # Generated user config (local only)
```

## 🤝 Contributing
We welcome contributions! If you want to help improve VeloxOS Welcome:
1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.