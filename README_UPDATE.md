# JARVIS - Personal Voice Assistant
## Version 2.0 - Mit futuristischer GUI & automatischer Installation

## 🚀 Neue Features v2.0

✨ **Automatische Installation**
- `auto_install.py` installiert alle Abhängigkeiten
- Erstellt automatisch Cache-Verzeichnisse
- Konfiguriert Windows Autostart

💫 **Futuristische GUI (PyQt6)**
- Modernes Dark-Theme mit Neon-Effekten
- Real-time Command-Verlauf
- Interaktive Statistiken & Dashboard
- Performance-optimiert

📊 **Intelligente Cache & Tracking**
- Speichert ALLE Anwendungen die je gestartet wurden
- Befehlsverlauf mit Timestamps
- Statistiken & Usage-Patterns
- Export-Funktionalität (JSON)

## 📋 System-Anforderungen

- **OS**: Windows 10/11 (Linux/Mac mit Anpassungen)
- **Python**: 3.8+
- **RAM**: Min. 2GB
- **Disk**: Min. 500MB
- **Microphone**: Ja
- **Internet**: Für API-Zugriff

## ⚡ Quick Start

### 1. Download & Setup
```bash
git clone https://github.com/flappybird007/Jarvis
cd Jarvis
```

### 2. Doppelklick auf `start_jarvis.py`
ODER im Terminal:
```bash
python start_jarvis.py
```

Das System führt automatisch aus:
- ✅ Python-Version prüfen
- ✅ Alle Dependencies installieren (pip upgrade, PyQt6, etc.)
- ✅ Cache-Verzeichnisse erstellen
- ✅ Datenbank initialisieren
- ✅ Autostart konfigurieren
- ✅ GUI starten

### 3. API-Keys konfigurieren
Öffne `.env` (wird automatisch erstellt):
```env
WEATHER_API_KEY=dein_api_key_hier
CITY=Berlin
```

Kostenlose API: https://openweathermap.org/api

## 🎮 GUI Bedienung

### Tabs
1. **📊 DASHBOARD** - Überblick & System-Status
2. **📜 HISTORY** - Vollständiger Befehlsverlauf
3. **🚀 APPS** - Alle jemals gestarteten Anwendungen
4. **📈 STATS** - Detaillierte Statistiken & Trends

### Buttons
- **🎤 LISTEN** - Spracherkennung starten
- **⚙️ SETTINGS** - Konfiguration anzeigen
- **🗑️ CLEAR CACHE** - Cache löschen
- **📥 EXPORT** - Verlauf als JSON exportieren

## 💾 Cache & Datenbank-Struktur

```
cache/
├── database/
│   └── app_history.json          # Hauptdatenbank
├── logs/                         # Logs
├── app_history/                  # App-Tracking
└── exports/                      # Exportierte Daten

app_history.json Struktur:
{
  "version": "1.0",
  "created_at": "ISO-Timestamp",
  "total_commands": 42,
  "applications_executed": [
    {
      "name": "Notepad",
      "count": 15,
      "last_used": "ISO-Timestamp"
    }
  ],
  "command_history": [
    {
      "timestamp": "ISO-Timestamp",
      "command": "google python",
      "application": "Chrome",
      "status": "success"
    }
  ],
  "statistics": {
    "total_time_running": 120,
    "total_voice_commands": 42,
    "most_used_app": "Notepad",
    "most_used_command": "google"
  }
}
```

## 🎤 Voice Commands (German)

```
"Jarvis, wie spät ist es?"        → Sagt aktuelle Uhrzeit
"Jarvis, wie ist das Wetter?"     → Wetterbericht abrufen
"Jarvis, google [Suche]"           → Google öffnen + suchen
"Jarvis, öffne [Programm]"         → Programm starten
"Jarvis, öffne Browser"            → Browser öffnen
"Jarvis, öffne Notepad"            → Notepad öffnen
"Jarvis, öffne Rechner"            → Taschenrechner öffnen
```

## 🔧 Erweiterte Konfiguration

### Custom Voice Commands hinzufügen

Öffne `jarvis_gui.py` und füge in der `process_command()` Methode hinzu:

```python
elif any(word in command for word in ["dein_kommando"]):
    self.deine_funktion()
```

### Sprachgeschwindigkeit anpassen

In `jarvis_gui.py` (Zeile ~90):
```python
self.engine.setProperty('rate', 150)  # 100=langsam, 200=schnell
```

### Theme ändern

Das Stylesheet befindet sich in `get_futuristic_stylesheet()`:
- Farben: `#00ff88` (Neon-Grün) anpassen
- `#0a0e27` (Dunkelblau) für Hintergrund
- `#1a1f3a` (Panel-Farbe)

## 🐛 Troubleshooting

### Problem: PyAudio Installation fehlgeschlagen
```bash
pip install pipwin
pipwin install pyaudio
```

### Problem: "Microphone not found"
- Teste Mikrofon in Windows Einstellungen
- Überprüfe Audio-Geräte
- Starte als Administrator

### Problem: GUI startet nicht
```bash
python -m pip install --upgrade PyQt6
```

### Problem: "Permission denied" bei Autostart
- Starte als Administrator
- Oder: Erstelle Manual-Shortcut in `shell:startup`

## 📊 Performance-Tipps

- Cache regelmäßig exportieren: **Export-Button in GUI**
- Alte Logs löschen: **Clear Cache Button**
- Cache-Größe checken: Datei-Explorer → `cache/database/app_history.json`

## 🔐 Sicherheit

⚠️ **Wichtig:**
- API-Keys gehören NICHT in Git!
- `.env` Datei ist gitignored
- Nicht public machen!

## 📈 Roadmap

- [ ] ChatGPT Integration
- [ ] Cloud-Sync für Verlauf
- [ ] Sprachprofile (Multiple Users)
- [ ] Dark/Light Theme Toggle
- [ ] Email-Notifications
- [ ] Smart Home Integration
- [ ] Offline-Spracherkennung
- [ ] Mobile App

## 📄 Lizenz

MIT License - Frei verwendbar

## 👨‍💻 Autor

Made with ❤️ by **flappybird007**

## 🤝 Support

Probleme oder Vorschläge? → [GitHub Issues](https://github.com/flappybird007/Jarvis/issues)

---

**Version**: 2.0.0  
**Last Updated**: 2026-05-26  
**Status**: ✅ Production Ready
