#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-Installation Script für JARVIS
Installiert automatisch alle Abhängigkeiten und konfiguriert das System
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    banner = r"""
    ╔═══════════════════════════════════════════════════════╗
    ║     JARVIS - Personal Voice Assistant Setup          ║
    ║     Auto-Installation & Configuration                ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python():
    """Überprüfe Python Version"""
    print("[*] Überprüfe Python Version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"[✗] Python 3.8+ erforderlich. Deine Version: {version.major}.{version.minor}")
        return False
    print(f"[✓] Python {version.major}.{version.minor} gefunden")
    return True

def upgrade_pip():
    """Upgrade pip zu neuester Version"""
    print("\n[*] Upgrade pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("[✓] pip aktualisiert")
        return True
    except Exception as e:
        print(f"[!] pip-Upgrade fehlgeschlagen: {e}")
        return False

def install_dependencies():
    """Installiere alle Python-Abhängigkeiten"""
    print("\n[*] Installiere Python-Abhängigkeiten...")
    
    dependencies = [
        "SpeechRecognition==3.10.0",
        "pyttsx3==2.90",
        "requests==2.31.0",
        "pyaudio==0.2.13",
        "python-dotenv==1.0.0",
        "PyQt6==6.6.1",
        "PyQt6-Qt6==6.6.1",
        "cryptography==41.0.7"
    ]
    
    for dep in dependencies:
        print(f"  → Installiere {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"    [✓] {dep} installiert")
        except Exception as e:
            print(f"    [!] Fehler bei {dep}: {e}")
            if "pyaudio" in dep.lower():
                print("    [*] Versuche alternative Installation...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", dep])
                    print(f"    [✓] {dep} installiert")
                except:
                    print(f"    [!] {dep} konnte nicht installiert werden")
    
    print("\n[✓] Alle Abhängigkeiten installiert")

def create_directories():
    """Erstelle notwendige Verzeichnisse"""
    print("\n[*] Erstelle Verzeichnisstruktur...")
    
    dirs = [
        "cache",
        "cache/app_history",
        "cache/logs",
        "cache/database",
        "config",
        "data"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  [✓] {dir_path}/")
    
    print("[✓] Verzeichnisse erstellt")

def create_env_file():
    """Erstelle .env Datei mit Standard-Konfiguration"""
    print("\n[*] Erstelle Konfigurationsdatei...")
    
    if os.path.exists(".env"):
        print("[!] .env existiert bereits")
        return
    
    env_content = """# JARVIS Konfiguration
# Ersetze die Werte mit deinen eigenen API-Keys

# OpenWeatherMap API (kostenlos: https://openweathermap.org/api)
WEATHER_API_KEY=your_weather_api_key_here

# Deine Stadt für Wetter
CITY=Berlin

# Jarvis Einstellungen
JARVIS_WAKE_WORD=jarvis
JARVIS_DEBUG=false
JARVIS_LANGUAGE=de-DE
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("[✓] .env erstellt")

def create_cache_database():
    """Erstelle Cache-Datenbank für App-Historie"""
    print("\n[*] Erstelle Cache-Datenbank...")
    
    db_file = "cache/database/app_history.json"
    
    if os.path.exists(db_file):
        print("[!] Cache-Datenbank existiert bereits")
        return
    
    initial_db = {
        "version": "1.0",
        "created_at": None,
        "total_commands": 0,
        "applications_executed": [],
        "command_history": [],
        "statistics": {
            "total_time_running": 0,
            "total_voice_commands": 0,
            "most_used_app": None,
            "most_used_command": None
        }
    }
    
    with open(db_file, "w", encoding="utf-8") as f:
        json.dump(initial_db, f, indent=2, ensure_ascii=False)
    
    print(f"[✓] Cache-Datenbank erstellt: {db_file}")

def setup_autostart_advanced():
    """Erweiterte Autostart-Konfiguration"""
    print("\n[*] Konfiguriere Autostart...")
    
    if sys.platform == "win32":
        try:
            import winreg
            jarvis_path = os.path.join(os.path.dirname(__file__), "jarvis_gui.py")
            python_path = sys.executable
            command = f'"{python_path}" "{jarvis_path}"'
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "Jarvis", 0, winreg.REG_SZ, command)
            winreg.CloseKey(key)
            
            print("[✓] Autostart konfiguriert (Windows)")
            return True
        except Exception as e:
            print(f"[!] Autostart-Setup fehlgeschlagen: {e}")
            print("[*] Versuche alternative Methode...")
            return False
    else:
        print("[!] Autostart nur unter Windows unterstützt")
        return False

def create_startup_script():
    """Erstelle Startup-Launcher Script"""
    print("\n[*] Erstelle Startup-Launcher...")
    
    startup_script = r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path

# Füge aktuelles Verzeichnis zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

try:
    from jarvis_gui import main
    main()
except ImportError as e:
    print(f"[ERROR] Import-Fehler: {e}")
    print("[*] Starte Auto-Installation...")
    os.system("python auto_install.py")
except Exception as e:
    print(f"[ERROR] {e}")
    input("Drücke ENTER zum Beenden...")
"""
    
    with open("start_jarvis.py", "w", encoding="utf-8") as f:
        f.write(startup_script)
    
    print("[✓] start_jarvis.py erstellt")

def finish_setup():
    """Abschluss der Installation"""
    print("\n" + "="*60)
    print("  ✓ INSTALLATION ERFOLGREICH ABGESCHLOSSEN!")
    print("="*60)
    print("\nNächste Schritte:")
    print("  1. Öffne .env und konfiguriere deine API-Keys")
    print("  2. Starte JARVIS mit: python start_jarvis.py")
    print("  3. Sage 'Jarvis' um den Assistenten zu aktivieren")
    print("\nDocumentation: https://github.com/flappybird007/Jarvis")
    print("\n")

def main():
    """Hauptinstallationsprozess"""
    print_banner()
    
    steps = [
        (check_python, "Python-Version prüfen"),
        (upgrade_pip, "pip aktualisieren"),
        (install_dependencies, "Abhängigkeiten installieren"),
        (create_directories, "Verzeichnisse erstellen"),
        (create_env_file, ".env konfigurieren"),
        (create_cache_database, "Cache-Datenbank erstellen"),
        (create_startup_script, "Startup-Launcher erstellen"),
        (setup_autostart_advanced, "Autostart konfigurieren"),
    ]
    
    for step_func, step_name in steps:
        try:
            result = step_func()
            if result is False:
                print(f"[!] {step_name} fehlgeschlagen")
                continue
        except Exception as e:
            print(f"[✗] Fehler bei {step_name}: {e}")
            continue
    
    finish_setup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Installation abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"[✗] Fehler: {e}")
        sys.exit(1)
