# JARVIS - Personal Voice Assistant

Ein Sprachassistent für Windows, inspiriert von Jarvis aus Iron Man.

## 🚀 Features

✅ Spracherkennung (Deutsch)  
✅ Text-to-Speech Ausgabe  
✅ Automatischer Systemstart  
✅ Wetterdaten abrufen  
✅ Programme starten  
✅ Google-Suche  
✅ Systemsteuerung (Uhrzeit, Herunterfahren)  
✅ Erweiterbar mit Custom-Commands  

## 📋 Voraussetzungen

- **Python 3.8+**
- **Windows 10/11** (für Autostart)
- **Mikrofon** und **Lautsprecher**
- **Internet-Verbindung** (für APIs)

## 🔧 Installation

### 1. Repository klonen oder Dateien herunterladen

```bash
git clone https://github.com/flappybird007/Jarvis
cd Jarvis
```

### 2. Installation ausführen

Doppelklick auf `install.bat` oder:

```bash
install.bat
```

### 3. API-Keys konfigurieren

Öffne `.env` und füge deine API-Keys ein:

```env
# OpenWeatherMap API (kostenlos)
WEATHER_API_KEY=your_api_key_here
CITY=Berlin
```

**API-Keys holen:**
- 🌤️ **Wetter**: https://openweathermap.org/api (kostenlos)

## 🎤 Verwendung

### Direktes Starten

```bash
python jarvis.py
```

### Sprachbefehle

1. **Jarvis** sagen (Aktivierungswort)
2. Befehl sprechen

**Beispiele:**
- "Jarvis, wie spät ist es?"
- "Jarvis, wie ist das Wetter?"
- "Jarvis, google Python Tutorial"
- "Jarvis, öffne Notepad"
- "Jarvis, öffne Browser"
- "Jarvis, öffne Rechner"

## 📝 Verfügbare Befehle

| Befehl | Beispiel |
|--------|----------|
| Zeit | "Wie spät ist es?" |
| Wetter | "Wie ist das Wetter?" |
| Google | "Google Python" |
| Programme | "Öffne Notepad", "Öffne Word" |
| Browser | "Öffne Browser" |
| Rechner | "Öffne Rechner" |
| Hilfe | "Welche Befehle gibt es?" |
| Herunterfahren | "Fahre System herunter" |

## 🛠️ Erweiterte Konfiguration

### Custom-Commands hinzufügen

Öffne `jarvis.py` und füge in der `process_command()`-Methode neue Befehle ein:

```python
elif any(word in command for word in ["mein_befehl"]):
    self.meine_funktion()
```

### Sprachgeschwindigkeit anpassen

In `jarvis.py`, Zeile ~32:
```python
self.engine.setProperty('rate', 150)  # 100 = langsam, 200 = schnell
```

### Lautstärke ändern

```python
self.engine.setProperty('volume', 0.9)  # 0.0 - 1.0
```

## ⚙️ Troubleshooting

### Problem: "Spracherkennungsfehler"
- Überprüfe Internet-Verbindung
- Teste Mikrofon-Eingang
- Versuche Lautstärke zu erhöhen

### Problem: "PyAudio nicht installiert"
```bash
pip install pipwin
pipwin install pyaudio
```

### Problem: "Microphone not found"
- Teste Mikrofon in Windows Einstellungen
- Überprüfe Audio-Geräte

### Problem: Autostart funktioniert nicht
- Starte als Administrator
- Überprüfe Windows Defender Firewall
- Manuelle Alternative: Erstelle Shortcut in `shell:startup`

## 🔒 Sicherheit & Disclaimer

⚠️ **Wichtig**: Dieses Programm hat breite Systemzugriffe. Verwende es nur auf eigenen Systemen.

- Das Programm startet automatisch beim Hochfahren
- Es kann Dateien ausführen und auf APIs zugreifen
- Achte auf Phishing und verdächtige Befehle
- API-Keys sollten sicher verwahrt sein

## 📚 Weitere Entwicklung

Geplante Features:
- [ ] ChatGPT Integration
- [ ] Alexa/Google Assistant Sync
- [ ] Datei-Management
- [ ] Email-Support
- [ ] Smart Home Integration
- [ ] Offline-Spracherkennung

## 📄 Lizenz

MIT License - Frei verwendbar

## 👨‍💻 Support

Für Fragen und Bugs: GitHub Issues öffnen

---

**Made with ❤️ by flappybird007**