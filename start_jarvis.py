#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
START JARVIS - Universal Launcher
Automatische Installation und Start
"""

import sys
import os
from pathlib import Path

def check_installation():
    """Überprüfe ob alle Komponenten installiert sind"""
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
    """Starte automatische Installation"""
    print("[*] Führe auto_install.py aus...")
    os.system(f"{sys.executable} auto_install.py")

def start_jarvis():
    """Starte JARVIS GUI"""
    print("[*] Starte JARVIS...")
    os.system(f"{sys.executable} jarvis_gui.py")

def main():
    """Hauptfunktion"""
    print("""
    ╔═══════════════════════════════════════╗
    ║  JARVIS - Personal Voice Assistant   ║
    ║  Starting System...                  ║
    ╚═══════════════════════════════════════╝
    """)
    
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
        sys.exit(1)
