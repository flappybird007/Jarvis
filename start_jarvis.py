#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
START JARVIS - Universal Launcher mit Admin-Rechte-Anforderung
Automatische Installation und Start
"""

import sys
import os
import ctypes
from pathlib import Path

def is_admin():
    """Überprüfe ob Admin-Rechte vorhanden sind"""
    try:
        return ctypes.windll.shell.IsUserAnAdmin()
    except:
        return False

def request_admin_rights():
    """
    Fordere Admin-Rechte an falls nicht vorhanden
    Diese Funktion wird immer aufgerufen
    """
    if not is_admin():
        print("[!] JARVIS benötigt Administrator-Rechte")
        print("[*] Bitte bestätige die UAC-Anfrage...")
        
        # Starte sich selbst mit Admin-Rechten über UAC
        ctypes.windll.shell.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

def check_installation():
    """
    Überprüfe ob alle Komponenten installiert sind
    """
    required_files = [
        "jarvis_gui.py",
        "auto_install.py",
        ".env"
    ]
    
    required_dirs = [
        "cache",
        "cache/database",
        "config"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    missing_dirs = [d for d in required_dirs if not os.path.isdir(d)]
    
    if missing_files or missing_dirs:
        print("[*] Fehlende Dateien/Verzeichnisse erkannt.")
        print("[*] Starte Auto-Installation...")
        return False
    return True

def run_auto_install():
    """
    Starte automatische Installation
    """
    print("[*] Führe auto_install.py aus...")
    os.system(f"{sys.executable} auto_install.py")

def start_jarvis():
    """
    Starte JARVIS GUI
    """
    print("[*] Starte JARVIS...")
    try:
        os.system(f"{sys.executable} jarvis_gui.py")
    except Exception as e:
        print(f"[ERROR] {e}")
        input("Drücke ENTER zum Beenden...")

def main():
    """
    Hauptfunktion
    """
    banner = r"""
    ╔════════════════════════════════════════════════════════════╗
    ║  JARVIS - Personal Voice Assistant                        ║
    ║  Starting System...                                       ║
    ║  v2.1 - Admin & SmartApp Protection                       ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)
    
    # KRITISCH: Admin-Rechte IMMER anforden
    print("\n[*] Überprüfe Administrator-Rechte...")
    request_admin_rights()
    print("[✓] Administrator-Rechte bestätigt\n")
    
    if not check_installation():
        run_auto_install()
    
    start_jarvis()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Abgebrochen")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        input("Drücke ENTER zum Beenden...")
        sys.exit(1)
