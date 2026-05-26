#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autostart-Setup für Jarvis
Fügt Jarvis zur Windows Autostart hinzu
"""

import os
import sys
import winreg
from pathlib import Path

def setup_autostart():
    """Registriere Jarvis im Windows Autostart"""
    try:
        # Pfad zum Jarvis-Skript
        jarvis_path = os.path.join(os.path.dirname(__file__), "jarvis.py")
        python_path = sys.executable
        
        # Command zum Ausführen
        command = f'"{python_path}" "{jarvis_path}"'
        
        # Öffne Windows Registry
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # Setze Wert
        winreg.SetValueEx(key, "Jarvis", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        
        print("[✓] Jarvis wurde zum Autostart hinzugefügt!")
        print(f"[✓] Start-Befehl: {command}")
        print("[✓] Jarvis startet automatisch beim nächsten Neustart.")
        
        return True
    except Exception as e:
        print(f"[✗] Fehler beim Setup: {e}")
        print("[!] Bitte mit Administrator-Rechten ausführen!")
        return False

def remove_autostart():
    """Entferne Jarvis aus Windows Autostart"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, "Jarvis")
        winreg.CloseKey(key)
        
        print("[✓] Jarvis wurde aus dem Autostart entfernt!")
        return True
    except FileNotFoundError:
        print("[!] Jarvis ist nicht im Autostart registriert.")
        return False
    except Exception as e:
        print(f"[✗] Fehler: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--remove":
        remove_autostart()
    else:
        setup_autostart()