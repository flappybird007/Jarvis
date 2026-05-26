@echo off
REM Jarvis Installation Script für Windows
REM Führt alle Setup-Schritte automatisch durch

echo.
echo ===============================================
echo   JARVIS - Personal Voice Assistant Setup
echo ===============================================
echo.

REM Überprüfe Python Installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python nicht gefunden! Bitte installiere Python 3.8+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python gefunden
echo.

REM Installiere Dependencies
echo [*] Installiere Abhängigkeiten...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Dependencies konnten nicht installiert werden
    pause
    exit /b 1
)

echo [OK] Dependencies installiert
echo.

REM Kopiere .env.example zu .env
if not exist .env (
    echo [*] Erstelle .env Datei...
    copy .env.example .env
    echo [OK] .env erstellt - Bitte API-Keys eintragen!
) else (
    echo [OK] .env existiert bereits
)

echo.

REM Frage nach Autostart
echo [*] Möchtest du Jarvis zum Autostart hinzufügen?
echo Wähle J für JA oder N für NEIN
set /p choice="(J/N): "

if /i "%choice%"=="J" (
    echo [*] Richte Autostart ein...
    python setup_autostart.py
    if errorlevel 1 (
        echo [!] Autostart-Setup fehlgeschlagen. Bitte als Administrator ausführen.
    ) else (
        echo [OK] Autostart konfiguriert
    )
) else (
    echo [*] Autostart übersprungen
)

echo.
echo ===============================================
echo   Setup abgeschlossen!
echo ===============================================
echo.
echo Nächste Schritte:
echo 1. Öffne .env und trage deine API-Keys ein
echo 2. Starte Jarvis: python jarvis.py
echo 3. Sage "Jarvis" um den Assistenten zu aktivieren
echo.
pause