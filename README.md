# 🐱 CPU RunningCat

A dope desktop tray app that shows an animated running cat 🐈💨 reflecting your CPU usage. Built with Python, `pystray`, and `Pillow`. Toggle speed boost and switch between dark/light themes right from the tray!

---

## ⚙️ Features

- Animated running cat in system tray  
- Speed Boost toggle for max animation speed  
- Dark / Light theme switch  
- Quit option from tray menu  

---

## 🧰 Built With

- Python 3.10+  
- [pystray](https://github.com/moses-palmer/pystray)  
- [Pillow (PIL)](https://pillow.readthedocs.io/)  

---

## 🚀 Getting Started

### Prerequisites

Make sure you’ve got Python 3.10 or newer installed on your system.

### Installation

```bash
git clone https://github.com/Fuad-Khan/CPU-RunningCat.git
cd CPU-RunningCat
pip install -r requirements.txt

## How to Run
python runcat.py

## Build Windows Executable (Optional)
# If you wanna flex with a standalone Windows .exe, use PyInstaller:
pyinstaller --onefile --windowed --add-data "cat;cat" runcat.py

