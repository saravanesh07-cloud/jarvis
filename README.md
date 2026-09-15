# JARVIS — Windows Voice Assistant

<p align="center">
  <img src="jarvis.png" width="220" alt="JARVIS HUD Icon">
</p>

An intelligent, voice-activated AI assistant for Windows that executes desktop commands, launches and closes apps, searches the web, captures screenshots, and connects directly to Google AI Studio.

---

## ⚡ Features
- **Voice Recognition**: Powered by Google Speech Recognition with Indian English (en-IN) & US English accent tuning.
- **Natural Voice Feedback**: Spoken feedback using offline Windows text-to-speech (pyttsx3).
- **Google AI Studio Integration**: Quick voice launch to custom Google AI Studio apps.
- **Application Control**:
  - **Open**: WhatsApp, Google Chrome, VS Code, Notepad, Calculator, File Explorer, Downloads, Desktop.
  - **Close**: Gracefully close open apps like File Explorer, WhatsApp, Chrome, VS Code, and Notepad.
- **Desktop Actions**:
  - Screenshot capture (auto-saved to Pictures/JARVIS Screenshots).
  - Time announcements.
  - Real-time CPU and RAM monitoring.
  - Google and YouTube search by voice.

---

## 🚀 Quick Setup

### Prerequisites
- Python 3.11 or 3.12 installed on Windows.
- Microphone & Internet connection (for Google speech-to-text).

### Installation
1. Clone this repository:
   `ash
   git clone https://github.com/saravanesh07-cloud/jarvis.git
   cd jarvis
   `
2. Create and activate a virtual environment:
   `powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   `
3. Install dependencies:
   `ash
   pip install -r requirements.txt
   `
4. Run JARVIS:
   `ash
   python jarvis.py
   `
   Or double-click start_jarvis.bat.

---

## 🎙️ Example Voice Commands
- *"Jarvis, open WhatsApp"*
- *"Jarvis, open AI Studio"*
- *"Jarvis, open File Explorer"*
- *"Jarvis, close File Explorer"*
- *"Jarvis, take a screenshot"*
- *"Jarvis, what time is it?"*
- *"Jarvis, check system usage"*
- *"Jarvis, search Quantum Computing on Google"*
- *"Jarvis, search Iron Man theme on YouTube"*
- *"Jarvis, exit"*
