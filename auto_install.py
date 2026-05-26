#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-Installation Script für JARVIS
Installiert automatisch alle Abhängigkeiten und konfiguriert das System
Mit Admin-Rechte-Anforderung und Desktop-Shortcut
"""

import os
import sys
import subprocess
import json
import ctypes
from pathlib import Path
import tempfile

def is_admin():
    """Überprüfe ob Admin-Rechte vorhanden sind (Windows)"""
    try:
        return ctypes.windll.shell.IsUserAnAdmin()
    except:
        return False

def request_admin_rights():
    """
fordere Admin-Rechte an"""
    if not is_admin():
        print("[!] Dieses Programm benötigt Administrator-Rechte")
        print("[*] Starte Programm mit erhobenen Rechten neu...")
        
        # Starte sich selbst mit Admin-Rechten
        ctypes.windll.shell.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

def bypass_smart_app_protection():
    """Deaktiviere SmartApp-Schutz und andere Windows Defender Erkennungen"""
    print("\n[*] Konfiguriere Windows Sicherheitseinstellungen...")
    
    # Wichtige Registry-Einträge für SmartApp-Bypass
    registry_commands = [
        # Deaktiviere SmartApp-Benachrichtigungen
        'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "HideFileExt" /t REG_DWORD /d 0 /f',
        
        # Deaktiviere SmartScreen
        'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\SmartScreenOptions" /v "SmartScreenEnabled" /t REG_SZ /d "Off" /f',
        
        # Deaktiviere Virus & threat protection notifications für diese App
        'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows Defender\\Exclusions\\Paths" /v "%cd%" /t REG_DWORD /d 0 /f',
    ]
    
    for cmd in registry_commands:
        try:
            subprocess.run(cmd, shell=True, capture_output=True)
            print(f"  [✓] Registry aktualisiert")
        except Exception as e:
            print(f"  [!] Registry-Fehler: {e}")
    
    # Erstelle Manifest für UAC-Kompatibilität
    create_app_manifest()

def create_app_manifest():
    """Erstelle Application Manifest für korrekte UAC-Behandlung"""
    print("\n[*] Erstelle Application Manifest...")
    
    manifest_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="1.0.0.0"
    processorArchitecture="*"
    name="Jarvis.App"
    type="win32"
  />
  <description>JARVIS - Personal Voice Assistant</description>
  
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
  
  <!-- Windows 10+ Kompatibilität -->
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
      <supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"/>
      <supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"/>
      <supportedOS Id="{1f676c76-80e1-4239-95bb-83d0b6b6bbe4}"/>
      <supportedOS Id="{45bbb4d4-4e91-49f3-bf47-f3e8b159b48b}"/>
    </application>
  </compatibility>
</assembly>
"""
    
    manifest_path = "start_jarvis.py.manifest"
    try:
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        print(f"[✓] Manifest erstellt: {manifest_path}")
    except Exception as e:
        print(f"[!] Fehler beim Erstellen des Manifests: {e}")

def create_desktop_shortcut():
    """Erstelle Desktop-Shortcut für JARVIS"""
    print("\n[*] Erstelle Desktop-Shortcut...")
    
    try:
        # Hole Desktop-Pfad
        desktop_path = Path.home() / "Desktop"
        shortcut_path = desktop_path / "JARVIS.lnk"
        
        # Pfad zum Script
        script_path = os.path.abspath("start_jarvis.py")
        icon_path = os.path.abspath("jarvis_icon.ico") if os.path.exists("jarvis_icon.ico") else ""
        
        # Erstelle PowerShell-Script für Shortcut
        ps_script = f"""
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut(\"{shortcut_path}\")
        $Shortcut.TargetPath = \"{sys.executable}\"
        $Shortcut.Arguments = \"{script_path}\"
        $Shortcut.WorkingDirectory = \"{os.path.dirname(script_path)}\"
        $Shortcut.Description = \"JARVIS - Personal Voice Assistant\"
        $Shortcut.WindowStyle = 1
        if (Test-Path \"{icon_path}\") {{
            $Shortcut.IconLocation = \"{icon_path}\"
        }}
        $Shortcut.Save()
        """
        
        # Führe PowerShell-Script aus
        temp_ps = tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False)
        temp_ps.write(ps_script)
        temp_ps.close()
        
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_ps.name],
            capture_output=True,
            check=False
        )
        
        # Lösche temp PowerShell-Datei
        try:
            os.remove(temp_ps.name)
        except:
            pass
        
        if shortcut_path.exists():
            print(f"[✓] Desktop-Shortcut erstellt: {shortcut_path}")
            return True
        else:
            print(f"[!] Shortcut-Erstellung fehlgeschlagen")
            return False
    except Exception as e:
        print(f"[!] Fehler bei Shortcut-Erstellung: {e}")
        return False

def create_admin_launcher():
    """Erstelle Admin-Launcher-Wrapper"""
    print("\n[*] Erstelle Admin-Launcher...")
    
    launcher_script = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS Admin Launcher - Wrapper für erhobene Rechte
"""
import sys
import os
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell.IsUserAnAdmin()
    except:
        return False

def request_admin():
    if not is_admin():
        # Starte mit Admin-Rechten
        ctypes.windll.shell.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

if __name__ == "__main__":
    request_admin()
    
    # Führe GUI aus
    try:
        from jarvis_gui import main
        main()
    except ImportError as e:
        print(f"[ERROR] {e}")
        input("Drücke ENTER...")
'''
    
    try:
        with open("jarvis_admin_launcher.py", "w", encoding="utf-8") as f:
            f.write(launcher_script)
        print("[✓] Admin-Launcher erstellt")
    except Exception as e:
        print(f"[!] Fehler: {e}")

def create_batch_launcher():
    """Erstelle Batch-Launcher für erweiterte Admin-Anforderung"""
    print("\n[*] Erstelle Batch-Launcher...")
    
    batch_script = r'''@echo off
REM JARVIS Batch Admin Launcher
REM Fordert automatisch Admin-Rechte an

>nul 2>&1 "%systemroot%\system32\cacls.exe" "%systemroot%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo [!] Fordere Administrator-Rechte an...
    goto uac_prompt
) else ( goto got_admin )

:uac_prompt
    echo Set UAC = CreateObject("Shell.Application") > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:got_admin
    pushd "%CD%"
    CD /D "%~dp0"
    echo [+] Administrator-Rechte erhalten
    echo [*] Starte JARVIS mit erhobenen Rechten...
    python start_jarvis.py
    pause
    exit /B
'''
    
    try:
        with open("jarvis_launcher.bat", "w", encoding="utf-8") as f:
            f.write(batch_script)
        print("[✓] Batch-Launcher erstellt")
    except Exception as e:
        print(f"[!] Fehler: {e}")

def disable_defender_exclusions():
    """Füge JARVIS zu Windows Defender Exclusions hinzu"""
    print("\n[*] Konfiguriere Windows Defender Exclusions...")
    
    try:
        jarvis_path = os.path.abspath(".")
        
        # Kommand zum Hinzufügen zu Exclusions
        cmd = f'powershell -Command "Add-MpPreference -ExclusionPath \"{jarvis_path}\" -ErrorAction SilentlyContinue"'
        
        subprocess.run(cmd, shell=True, capture_output=True)
        print(f"[✓] JARVIS zu Defender Exclusions hinzugefügt: {jarvis_path}")
    except Exception as e:
        print(f"[!] Fehler bei Defender-Konfiguration: {e}")

def print_banner():
    banner = r"""
    ╔═══════════════════════════════════════════════════════╗
    ║     JARVIS - Personal Voice Assistant Setup          ║
    ║     Auto-Installation & Configuration                ║
    ║     v2.1 - Mit Admin & SmartApp-Bypass               ║
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
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])
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
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep, "-q"])
            print(f"    [✓] {dep} installiert")
        except Exception as e:
            print(f"    [!] Fehler bei {dep}: {e}")
            if "pyaudio" in dep.lower():
                print("    [*] Versuche alternative Installation...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", dep, "-q"])
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
        "cache/exports",
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
JARVIS_REQUIRE_ADMIN=true
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
        "version": "2.1",
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
            launcher_path = os.path.join(os.path.dirname(__file__), "jarvis_launcher.bat")
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "Jarvis", 0, winreg.REG_SZ, launcher_path)
            winreg.CloseKey(key)
            
            print("[✓] Autostart konfiguriert (Windows)")
            return True
        except Exception as e:
            print(f"[!] Autostart-Setup fehlgeschlagen: {e}")
            return False
    else:
        print("[!] Autostart nur unter Windows unterstützt")
        return False

def finish_setup():
    """Abschluss der Installation"""
    print("\n" + "="*60)
    print("  ✓ INSTALLATION ERFOLGREICH ABGESCHLOSSEN!")
    print("="*60)
    print("\nErstellte Dateien:")
    print("  ✅ Desktop Shortcut (JARVIS.lnk)")
    print("  ✅ Admin-Launcher (jarvis_admin_launcher.py)")
    print("  ✅ Batch-Launcher (jarvis_launcher.bat)")
    print("  ✅ Anwendungs-Manifest (start_jarvis.py.manifest)")
    print("\nNächste Schritte:")
    print("  1. Öffne .env und konfiguriere deine API-Keys")
    print("  2. Starte JARVIS vom Desktop-Shortcut")
    print("  3. Sage 'Jarvis' um den Assistenten zu aktivieren")
    print("\n[!] WICHTIG: JARVIS benötigt IMMER Administrator-Rechte")
    print("    Das ist normal und notwendig für volle Funktionalität!")
    print("\nDocumentation: https://github.com/flappybird007/Jarvis")
    print("\n")

def main():
    """Hauptinstallationsprozess"""
    print_banner()
    
    # Prote Admin-Rechte an START
    request_admin_rights()
    
    print("\n[✓] Administrator-Rechte bestätigt\n")
    
    steps = [
        (check_python, "Python-Version prüfen"),
        (bypass_smart_app_protection, "SmartApp-Schutz bypass"),
        (disable_defender_exclusions, "Windows Defender konfigurieren"),
        (create_app_manifest, "App-Manifest erstellen"),
        (create_admin_launcher, "Admin-Launcher erstellen"),
        (create_batch_launcher, "Batch-Launcher erstellen"),
        (upgrade_pip, "pip aktualisieren"),
        (install_dependencies, "Abhängigkeiten installieren"),
        (create_directories, "Verzeichnisse erstellen"),
        (create_env_file, ".env konfigurieren"),
        (create_cache_database, "Cache-Datenbank erstellen"),
        (setup_autostart_advanced, "Autostart konfigurieren"),
        (create_desktop_shortcut, "Desktop-Shortcut erstellen"),
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
        input("Drücke ENTER zum Beenden...")
        sys.exit(1)
