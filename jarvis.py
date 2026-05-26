#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS - Personal Voice Assistant for Windows
Ein Sprachassistent ähnlich wie Jarvis aus Iron Man
"""

import speech_recognition as sr
import pyttsx3
import os
import sys
import subprocess
import json
import requests
from datetime import datetime
from pathlib import Path
import threading
import webbrowser
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()

class JarvisAssistant:
    def __init__(self):
        """Initialisiere Jarvis"""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Sprechgeschwindigkeit
        self.engine.setProperty('volume', 0.9)
        
        # Konfiguration
        self.wake_word = "jarvis"
        self.running = True
        self.config_file = "jarvis_config.json"
        self.load_config()
        
        print("[JARVIS] System initialisiert und bereit.")
        self.speak("Jarvis online. Warte auf Aktivierungswort.")
    
    def load_config(self):
        """Lade Konfiguration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "weather_api": os.getenv("WEATHER_API_KEY", ""),
                "chatgpt_api": os.getenv("CHATGPT_API_KEY", ""),
                "city": "Berlin"
            }
    
    def speak(self, text):
        """Text-zu-Sprache Ausgabe"""
        print(f"[JARVIS] {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self, timeout=5):
        """Höre Spracheinput ab"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio, language="de-DE")
                print(f"[USER] {text}")
                return text.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            self.speak("Spracherkennungsfehler. Versuchen Sie es später erneut.")
            return ""
        except Exception as e:
            print(f"[ERROR] {e}")
            return ""
    
    def listen_for_wake_word(self):
        """Warte auf Aktivierungswort"""
        print("[JARVIS] Höre auf Aktivierungswort...")
        while self.running:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = self.recognizer.listen(source, timeout=3)
                    text = self.recognizer.recognize_google(audio, language="de-DE").lower()
                    
                    if self.wake_word in text:
                        print("[JARVIS] Aktivierungswort erkannt!")
                        self.speak("Ja, ich bin bereit. Was möchten Sie?")
                        self.process_command()
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
            except Exception as e:
                print(f"[ERROR] {e}")
    
    def process_command(self):
        """Verarbeite Befehle"""
        command = self.listen(timeout=8)
        
        if not command:
            return
        
        # Kommando-Routing
        if any(word in command for word in ["zeit", "uhrzeit", "wie spät"]):
            self.get_time()
        elif any(word in command for word in ["wetter", "temperatur", "regen"]):
            self.get_weather()
        elif any(word in command for word in ["google", "suche", "suchen"]):
            self.google_search(command)
        elif any(word in command for word in ["öffne", "starte"]):
            self.open_application(command)
        elif any(word in command for word in ["browser", "chrome", "firefox", "internet"]):
            self.open_browser()
        elif any(word in command for word in ["notepad", "editor", "notiz"]):
            self.open_notepad()
        elif any(word in command for word in ["rechner", "calculator"]):
            self.open_calculator()
        elif any(word in command for word in ["beende", "ausschalten", "herunterfahren"]):
            self.shutdown()
        elif any(word in command for word in ["heyruss", "hi", "hallo", "hey"]):
            self.speak("Hallo! Ich bin Jarvis. Wie kann ich dir helfen?")
        elif any(word in command for word in ["hilfe", "was kannst du"]):
            self.show_help()
        else:
            # Fallback: Versuche mit ChatGPT zu antworten (falls API verfügbar)
            self.ask_ai(command)
    
    def get_time(self):
        """Gebe aktuelle Zeit aus"""
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        self.speak(f"Die Uhrzeit ist {time_str}")
    
    def get_weather(self):
        """Hole Wetterdaten"""
        api_key = self.config.get("weather_api")
        city = self.config.get("city", "Berlin")
        
        if not api_key:
            self.speak("Wetter API nicht konfiguriert. Bitte API-Schlüssel hinzufügen.")
            return
        
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=de"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                self.speak(f"Das Wetter in {city}: {description}, Temperatur {temp} Grad Celsius.")
            else:
                self.speak("Wetter konnte nicht abgerufen werden.")
        except Exception as e:
            self.speak(f"Fehler beim Abrufen des Wetters: {str(e)}")
            print(f"[ERROR] {e}")
    
    def google_search(self, query):
        """Führe Google-Suche durch"""
        search_query = query.replace("google", "").replace("suche", "").strip()
        if search_query:
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            self.speak(f"Öffne Google-Suchergebnisse für {search_query}")
        else:
            self.speak("Bitte geben Sie einen Suchbegriff an.")
    
    def open_application(self, command):
        """Öffne Anwendungen"""
        apps = {
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "paint": "mspaint",
            "vlc": "vlc",
            "discord": "discord",
            "steam": "steam",
            "spotify": "spotify"
        }
        
        for app_name, app_path in apps.items():
            if app_name in command:
                try:
                    subprocess.Popen(app_path)
                    self.speak(f"Öffne {app_name}")
                    return
                except Exception as e:
                    self.speak(f"{app_name} konnte nicht geöffnet werden.")
                    print(f"[ERROR] {e}")
                    return
        
        self.speak("Anwendung nicht erkannt.")
    
    def open_browser(self):
        """Öffne Browser"""
        try:
            webbrowser.open("https://www.google.com")
            self.speak("Browser geöffnet.")
        except Exception as e:
            self.speak("Browser konnte nicht geöffnet werden.")
    
    def open_notepad(self):
        """Öffne Editor"""
        try:
            subprocess.Popen("notepad")
            self.speak("Notepad geöffnet.")
        except Exception as e:
            self.speak("Notepad konnte nicht geöffnet werden.")
    
    def open_calculator(self):
        """Öffne Taschenrechner"""
        try:
            subprocess.Popen("calc")
            self.speak("Taschenrechner geöffnet.")
        except Exception as e:
            self.speak("Taschenrechner konnte nicht geöffnet werden.")
    
    def ask_ai(self, question):
        """Frage KI (fallback für unbekannte Befehle)"""
        self.speak("Diese Funktion ist noch nicht vollständig konfiguriert.")
        print(f"[AI-FALLBACK] Frage: {question}")
    
    def show_help(self):
        """Zeige verfügbare Befehle"""
        help_text = """
        Verfügbare Befehle:
        - Jarvis, wie spät ist es?
        - Jarvis, wie ist das Wetter?
        - Jarvis, google [Suchbegriff]
        - Jarvis, öffne [Programm]
        - Jarvis, öffne Browser
        - Jarvis, öffne Notepad
        - Jarvis, öffne Rechner
        """
        self.speak("Verfügbare Befehle geladen. Siehe Konsole für Details.")
        print(help_text)
    
    def shutdown(self):
        """Fahre System herunter"""
        self.speak("System wird heruntergefahren.")
        os.system("shutdown /s /t 10")
    
    def run(self):
        """Starte Jarvis Hauptschleife"""
        try:
            self.listen_for_wake_word()
        except KeyboardInterrupt:
            self.speak("Jarvis wird beendet.")
            self.running = False
        except Exception as e:
            print(f"[CRITICAL ERROR] {e}")
            self.speak("Kritischer Fehler aufgetreten.")


if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()