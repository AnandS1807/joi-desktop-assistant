# 🤖 AI Desktop Assistant MVP

A **privacy-focused AI assistant** that observes desktop activities, learns user workflows, and automates repetitive tasks — entirely **locally**.

---

## 🎯 Overview

This project reimagines **AI–human computer interaction** by introducing an AI “dashcam” for your desktop.  
The assistant:

- **Watches** your desktop activities (screen + audio)  
- **Learns** your repetitive workflows using pattern recognition  
- **Automates** those workflows with computer vision and input simulation  
- **Runs 100% locally** — no cloud dependencies, ensuring complete privacy  

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Desktop AI Assistant                    │
├─────────────────────────────────────────────────────────────┤
│                      Observation Layer                      │
│   ├─ Screen Capture (PyAutoGUI)                             │
│   ├─ Audio Capture (PyAudio + Whisper)                      │
│   └─ Input Tracking (Mouse/Keyboard)                        │
├─────────────────────────────────────────────────────────────┤
│                    Understanding Layer                      │
│   ├─ Speech-to-Text (OpenAI Whisper)                        │
│   ├─ Behavior Analysis (Rule-based AI)                      │
│   └─ Pattern Recognition                                    │
├─────────────────────────────────────────────────────────────┤
│                      Automation Layer                       │
│   ├─ Workflow Execution (PyAutoGUI)                         │
│   ├─ Application Control                                    │
│   └─ Task Automation                                        │
├─────────────────────────────────────────────────────────────┤
│                          GUI Layer                          │
│   ├─ Control Panel Dashboard                                │
│   ├─ Real-time Monitoring                                   │
│   └─ Workflow Management                                    │
├─────────────────────────────────────────────────────────────┤
│               Local Storage – No Cloud Dependencies          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

- **Python 3.8+** — Core programming language  
- **PyAutoGUI** — Screen capture and automation  
- **OpenAI Whisper** — Local speech-to-text processing  
- **PyAudio** — Audio input recording  
- **Tkinter** — Graphical user interface  
- **PyGetWindow** — Window and focus management  
- **PsUtil** — System monitoring utilities  

---

## 📁 Project Structure

```
desktop-ai-assistant/
├── src/                     # Source code
│   ├── observation/         # Screen, audio, input capture
│   ├── processing/          # Speech, behavior analysis
│   ├── automation/          # Workflow execution
│   ├── gui/                 # User interface components
│   ├── data/                # Storage and data management
│   └── config/              # Configuration settings
├── data/                    # Local data storage
│   ├── observations/        # Screenshots, audio, logs
│   └── workflows/           # Learned workflows
├── models/                  # AI models (Whisper)
└── requirements.txt         # Project dependencies
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher  
- Windows 10/11 (macOS/Linux supported with minor modifications)  
- Functional microphone and speakers  

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd desktop-ai-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or use the installer:
   ```bash
   python install.py
   ```

3. **Run the application**

   **Option A: GUI Version (Recommended)**
   ```bash
   python run_gui.py
   ```

   **Option B: Interactive Console**
   ```bash
   python run_interactive.py
   ```

   **Option C: Basic Version**
   ```bash
   python run.py
   ```

---

## 🎮 How to Use

1. **Start the Assistant**  
   Launch the application using any run script.  
   The system begins observing your desktop in real-time.

2. **Perform Your Work**  
   Use applications like Excel, Word, File Explorer, or Chrome.  
   The AI automatically detects and learns your workflows.  
   You can use voice commands such as:  
   - “open excel”  
   - “save file”  
   - “create document”

3. **Enable Automation**  
   - In the GUI: click **Enable Automation**  
   - In the Console: type `enable` or `auto`

4. **Monitor Activity**  
   - View detected workflows in the activity log  
   - Track system status and data storage  
   - Manage learned workflows through the control interface  

---

## 🔧 Features

### ✅ Core Features
- Real-time desktop observation  
- Voice command recognition  
- Workflow pattern detection  
- One-click automation  
- 100% local processing  
- Privacy-first architecture  

### 🎯 Supported Applications
- **Microsoft Excel** — Budgets, formulas, data entry  
- **Microsoft Word** — Document creation and formatting  
- **File Explorer** — Navigation and organization  
- **Chrome / Firefox** — Web browsing and research  
- **VS Code** — Coding activity detection  

---

## 🛡️ Privacy & Security

- All data is processed and stored **locally**  
- **No data** is sent to cloud services  
- Automatic cleanup of old data  
- Transparent and accessible activity logging  

---

## 📊 Demo Workflows

| Workflow | Example Steps |
|-----------|----------------|
| **Excel Budget Creation** | Open Excel → Create template → Add formulas → Save |
| **Document Automation** | Open Word → Create document → Add content → Format |
| **File Organization** | Open File Explorer → Navigate → Create folder structure |
| **Web Research** | Open browser → Search → Browse results |

---

## 🧩 Troubleshooting

### Common Issues

**Audio not working**
- Check microphone permissions  
- Verify that PyAudio is installed correctly  

**Automation not executing**
- Ensure target applications are installed  
- Confirm automation is enabled in settings  

**High CPU usage**
- Increase capture interval in settings  
- Close unnecessary background apps  

### Getting Help
- Review logs in `data/observations/`  
- Check console output for error messages  
- Verify that all dependencies are installed  

---

## 💡 Use Cases

| User Type | Benefit |
|------------|----------|
| **Office Workers** | Automate repetitive Excel/Word tasks |
| **Developers** | Automate setup and file organization |
| **Researchers** | Automate data collection and analysis |
| **Students** | Simplify document creation and research |

---

## 🔮 Future Enhancements

- Cross-platform support  
- Advanced workflow editor  
- AI-powered planning engine  
- Plugin system for custom automations  
- Optional cloud synchronization  
- Mobile companion app  

---

## 📄 License

This project is created for **educational and demonstration purposes**.  
All rights reserved © 2025.
