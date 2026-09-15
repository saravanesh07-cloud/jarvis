import os
import subprocess
import webbrowser
import datetime
import psutil
import pyautogui
import speech_recognition as sr
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

# Initialize Speech Recognizer once
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8
recognizer.dynamic_energy_threshold = True

WAKE_WORDS = [
    "hey jarvis", "hi jarvis", "hello jarvis", "ok jarvis", "okay jarvis",
    "red jarvis", "kids service", "dear jarvis", "jarvis", "javis",
    "travis", "service", "harvis"
]

def speak(text):
    print(f"JARVIS: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("[TTS Error]:", e)

def calibrate_mic():
    with sr.Microphone() as source:
        print("Calibrating microphone for ambient noise... please wait a second.")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        print("Microphone ready!")

def listen():
    with sr.Microphone() as source:
        print("\nListening...")
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
            text = ""
            # Try Indian English first, then fallback to general English
            try:
                text = recognizer.recognize_google(audio, language="en-IN")
            except Exception:
                try:
                    text = recognizer.recognize_google(audio, language="en-US")
                except Exception:
                    pass

            if text:
                print("YOU:", text)
            return text.lower().strip()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return ""
        except sr.RequestError:
            speak("Speech recognition needs an internet connection right now.")
            return ""

AI_STUDIO_URL = "https://aistudio.google.com/apps/4f16c366-9ec4-4659-a2aa-464a62c48747?showPreview=true&project=gen-lang-client-0597665184&showAssistant=true"

def open_app(name):
    name = name.lower().strip()
    
    if any(k in name for k in ["ai studio", "aistudio", "google ai", "studio", "my assistant", "gemini", "assistant", "ai"]):
        webbrowser.open(AI_STUDIO_URL)
        return "Google AI Studio"

    if "whatsapp" in name:
        os.startfile("whatsapp:")
        return "WhatsApp"
        
    if any(k in name for k in ["chrome", "google chrome", "browser"]):
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if os.path.exists(chrome_path):
            subprocess.Popen(f'"{chrome_path}"', shell=True)
        else:
            subprocess.Popen("start chrome", shell=True)
        return "Google Chrome"
        
    if any(k in name for k in ["vs code", "vscode", "code"]):
        subprocess.Popen("code", shell=True)
        return "Visual Studio Code"
        
    if "notepad" in name:
        subprocess.Popen("notepad.exe", shell=True)
        return "Notepad"
        
    if any(k in name for k in ["calc", "calculator"]):
        subprocess.Popen("calc.exe", shell=True)
        return "Calculator"
        
    if any(k in name for k in ["file explorer", "explorer", "files", "my computer"]):
        subprocess.Popen("explorer.exe", shell=True)
        return "File Explorer"
        
    if "download" in name:
        folder = os.path.join(os.path.expanduser("~"), "Downloads")
        os.startfile(folder)
        return "Downloads"
        
    if "desktop" in name:
        folder = os.path.join(os.path.expanduser("~"), "Desktop")
        os.startfile(folder)
        return "Desktop"
        
    # Generic fallback: try running directly
    try:
        os.startfile(name)
        return name.title()
    except Exception:
        return None

def close_app(name):
    name = name.lower().strip()
    proc_map = {
        "whatsapp": ["WhatsApp.exe", "WhatsAppHost.exe"],
        "chrome": ["chrome.exe"],
        "vs code": ["Code.exe"],
        "vscode": ["Code.exe"],
        "code": ["Code.exe"],
        "notepad": ["notepad.exe", "Notepad.exe"],
        "calculator": ["CalculatorApp.exe", "calc.exe", "Calculator.exe"],
        "calc": ["CalculatorApp.exe", "calc.exe", "Calculator.exe"],
    }
    
    # Special handle for File Explorer windows
    if any(k in name for k in ["file explorer", "explorer", "files"]):
        try:
            subprocess.run(["powershell", "-Command", "(New-Object -ComObject Shell.Application).Windows() | ForEach-Object { $_.Quit() }"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "File Explorer"
        except Exception:
            pass

    for key, procs in proc_map.items():
        if key in name:
            closed = False
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() in [p.lower() for p in procs]:
                        proc.terminate()
                        closed = True
                except Exception:
                    pass
            if closed:
                return key.title()
    return None

def handle(command):
    orig = command
    # Strip known wake words
    for w in sorted(WAKE_WORDS, key=len, reverse=True):
        if w in command:
            command = command.replace(w, "").strip()

    # Clean leading filler words
    for filler in ["hey", "hi", "ok", "okay", "please", "can you", "could you", "just"]:
        if command.startswith(filler + " "):
            command = command[len(filler):].strip()

    if not command:
        speak("I'm listening.")
        return True

    # 1. Close command
    if any(k in command for k in ["close ", "closed ", "kill ", "stop "]):
        for kw in ["close ", "closed ", "kill ", "stop "]:
            if kw in command:
                target = command.split(kw, 1)[1].strip()
                # Clean up target
                target = target.removeprefix("the ").removesuffix(" please").removesuffix(" app").strip()
                result = close_app(target)
                if result:
                    speak(f"Closed {result}.")
                else:
                    speak(f"Could not close {target}.")
                return True

    # 2. Open command
    if any(k in command for k in ["open ", "launch ", "start "]):
        for kw in ["open ", "launch ", "start "]:
            if kw in command:
                target = command.split(kw, 1)[1].strip()
                # Clean up target
                target = target.removeprefix("the ").removesuffix(" please").removesuffix(" app").strip()
                result = open_app(target)
                if result:
                    speak(f"Certainly. Opening {result}.")
                else:
                    speak(f"I couldn't find {target} as a configured application.")
                return True

    # Direct mention of app (e.g. user just said "whatsapp" or "ai studio")
    for direct in ["whatsapp", "chrome", "notepad", "calculator", "file explorer", "ai studio", "aistudio", "gemini", "assistant"]:
        if command == direct or command == f"open {direct}":
            result = open_app(direct)
            if result:
                speak(f"Opening {result}.")
                return True

    # 3. Screenshot
    if "screenshot" in command:
        folder = os.path.join(os.path.expanduser("~"), "Pictures", "JARVIS Screenshots")
        os.makedirs(folder, exist_ok=True)
        filename = datetime.datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
        path = os.path.join(folder, filename)
        pyautogui.screenshot(path)
        speak("Screenshot captured and saved.")
        return True

    # 4. Time
    if any(k in command for k in ["time", "what time is it", "tell me the time"]):
        speak(datetime.datetime.now().strftime("It is %I:%M %p."))
        return True

    # 5. System Stats
    if any(k in command for k in ["cpu", "system usage", "ram", "memory"]):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        speak(f"CPU usage is {cpu:.0f} percent and memory usage is {ram:.0f} percent.")
        return True

    # 6. Google Search
    if command.startswith("search ") or command.startswith("google "):
        query = command.split(" ", 1)[1].strip()
        webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "+"))
        speak(f"Searching for {query}.")
        return True

    # 7. YouTube Search
    if command.startswith("youtube ") or "play on youtube" in command:
        query = command.replace("youtube", "").replace("play on", "").strip()
        webbrowser.open("https://www.youtube.com/results?search_query=" + query.replace(" ", "+"))
        speak(f"Searching YouTube for {query}.")
        return True

    # 8. Exit
    if any(k in command for k in ["exit", "quit", "shutdown jarvis", "goodbye", "bye"]):
        speak("Understood. Going offline. See you soon.")
        return False

    speak("I heard: " + orig + ". Try saying: open WhatsApp, open Chrome, take screenshot, or check time.")
    return True

def main():
    calibrate_mic()
    speak("Good evening. I am JARVIS. I'm online and ready to help.")
    speak("Say JARVIS followed by your command.")
    while True:
        command = listen()
        if command:
            is_wake_word = any(w in command for w in ["jarvis", "javis", "service", "travis", "harvis", "hey"])
            is_direct_command = any(k in command for k in ["open", "close", "launch", "start", "screenshot", "time", "cpu", "ram", "search", "youtube", "exit", "quit", "bye", "whatsapp", "chrome", "studio", "assistant", "ai", "gemini"])
            if is_wake_word or is_direct_command:
                if not handle(command):
                    break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[JARVIS Error]: {e}")
        input("\nPress Enter to exit...")
