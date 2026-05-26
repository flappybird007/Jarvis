#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS GUI - Modern & Futuristic Voice Assistant Interface
PyQt6-basierte Benutzeroberfläche mit futuristischem Design
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QProgressBar, QComboBox
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap, QLinearGradient, QBrush
from PyQt6.QtCore import QTimer
import speech_recognition as sr
import pyttsx3
import threading
from dotenv import load_dotenv

load_dotenv()

class VoiceWorker(QThread):
    """Worker-Thread für Spracherkennung"""
    command_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
    
    def run(self):
        """Führe Spracherkennung aus"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10)
                text = self.recognizer.recognize_google(audio, language="de-DE")
                self.command_received.emit(text)
        except sr.UnknownValueError:
            self.error_occurred.emit("Sprachbefehl nicht erkannt")
        except sr.RequestError as e:
            self.error_occurred.emit(f"Fehler: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"Fehler: {str(e)}")

class CacheManager:
    """Verwaltet die Cache- und Verlaufsdatenbank"""
    
    def __init__(self):
        self.db_path = "cache/database/app_history.json"
        self.load_database()
    
    def load_database(self):
        """Lade Cache-Datenbank"""
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            else:
                self.data = self.create_empty_db()
        except Exception as e:
            print(f"[ERROR] Fehler beim Laden der Datenbank: {e}")
            self.data = self.create_empty_db()
    
    def create_empty_db(self):
        """Erstelle leere Datenbank"""
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
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
    
    def add_command(self, command, app=None, status="success"):
        """Füge Befehl zum Verlauf hinzu"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "application": app,
            "status": status
        }
        self.data["command_history"].append(entry)
        self.data["total_commands"] += 1
        
        if app and app not in [a["name"] for a in self.data["applications_executed"]]:
            self.data["applications_executed"].append({
                "name": app,
                "count": 1,
                "last_used": datetime.now().isoformat()
            })
        
        self.save_database()
    
    def save_database(self):
        """Speichere Datenbank"""
        try:
            Path("cache/database").mkdir(parents=True, exist_ok=True)
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Fehler beim Speichern der Datenbank: {e}")
    
    def get_statistics(self):
        """Hole Statistiken"""
        return self.data.get("statistics", {})
    
    def get_history(self, limit=50):
        """Hole Befehlsverlauf"""
        history = self.data.get("command_history", [])
        return history[-limit:][::-1]  # Neueste zuerst

class JarvisGUI(QMainWindow):
    """Hauptfenster der JARVIS GUI"""
    
    def __init__(self):
        super().__init__()
        self.cache_manager = CacheManager()
        self.voice_worker = None
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        self.setWindowTitle("JARVIS - Personal Voice Assistant")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(self.get_futuristic_stylesheet())
        
        self.init_ui()
        self.load_history()
    
    def get_futuristic_stylesheet(self):
        """Futuristisches Design-Stylesheet"""
        return """
        QMainWindow {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                       stop: 0 #0a0e27, stop: 1 #1a1f3a);
        }
        
        QWidget {
            background-color: transparent;
            color: #00ff88;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }
        
        QTabWidget::pane {
            border: 2px solid #00ff88;
            background-color: #0a0e27;
        }
        
        QTabBar::tab {
            background-color: #1a1f3a;
            color: #00ff88;
            padding: 8px 20px;
            margin: 2px;
            border: 1px solid #00ff88;
            border-radius: 5px;
        }
        
        QTabBar::tab:selected {
            background-color: #00ff88;
            color: #0a0e27;
            font-weight: bold;
        }
        
        QPushButton {
            background-color: #1a1f3a;
            color: #00ff88;
            border: 2px solid #00ff88;
            padding: 8px 15px;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        QPushButton:hover {
            background-color: #00ff88;
            color: #0a0e27;
            border: 2px solid #00ff88;
        }
        
        QPushButton:pressed {
            background-color: #00cc66;
            border: 2px solid #00cc66;
        }
        
        QLabel {
            color: #00ff88;
            font-weight: bold;
        }
        
        QListWidget {
            background-color: #0a0e27;
            border: 2px solid #00ff88;
            border-radius: 5px;
        }
        
        QListWidget::item {
            padding: 5px;
            background-color: #1a1f3a;
            color: #00ff88;
            border-bottom: 1px solid #00ff88;
        }
        
        QListWidget::item:selected {
            background-color: #00ff88;
            color: #0a0e27;
        }
        
        QTableWidget {
            background-color: #0a0e27;
            border: 2px solid #00ff88;
            gridline-color: #00ff88;
        }
        
        QTableWidget::item {
            padding: 5px;
            color: #00ff88;
            background-color: #1a1f3a;
            border: 1px solid #00ff88;
        }
        
        QHeaderView::section {
            background-color: #00ff88;
            color: #0a0e27;
            padding: 5px;
            border: 1px solid #00ff88;
            font-weight: bold;
        }
        
        QProgressBar {
            border: 2px solid #00ff88;
            border-radius: 5px;
            background-color: #1a1f3a;
            text-align: center;
            color: #00ff88;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                       stop: 0 #00ff88, stop: 1 #00cc66);
            border-radius: 3px;
        }
        
        QTextEdit {
            background-color: #0a0e27;
            color: #00ff88;
            border: 2px solid #00ff88;
            border-radius: 5px;
        }
        
        QComboBox {
            background-color: #1a1f3a;
            color: #00ff88;
            border: 2px solid #00ff88;
            border-radius: 5px;
            padding: 5px;
        }
        
        QComboBox::drop-down {
            background-color: #00ff88;
            border: none;
        }
        """
    
    def init_ui(self):
        """Initialisiere Benutzeroberfläche"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Linkes Panel - Steuerung
        left_panel = self.create_control_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Rechtes Panel - Tabs
        right_panel = self.create_tabs()
        main_layout.addWidget(right_panel, 2)
    
    def create_control_panel(self):
        """Erstelle Kontrollpanel"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Logo/Titel
        title = QLabel("JARVIS")
        title_font = QFont("Courier New", 24, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #00ff88; text-shadow: 0px 0px 10px #00ff88;")
        layout.addWidget(title)
        
        # Status-Anzeige
        self.status_label = QLabel("● STANDBY")
        self.status_label.setStyleSheet("color: #ffaa00; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Separator
        separator = QLabel("―" * 20)
        separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(separator)
        
        # Voice Button
        self.voice_btn = QPushButton("🎤 LISTEN")
        self.voice_btn.setMinimumHeight(60)
        self.voice_btn.setStyleSheet("""
            QPushButton {
                background-color: #00ff88;
                color: #0a0e27;
                font-size: 14pt;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #00cc66;
            }
        """)
        self.voice_btn.clicked.connect(self.start_listening)
        layout.addWidget(self.voice_btn)
        
        # Status Bar
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(150)
        layout.addWidget(QLabel("OUTPUT:"))
        layout.addWidget(self.output_text)
        
        # System-Info
        layout.addWidget(QLabel("SYSTEM INFO:"))
        info_box = QTextEdit()
        info_box.setReadOnly(True)
        info_box.setMaximumHeight(100)
        
        system_info = f"""
VERSION: 1.0.0
STATUS: ONLINE
COMMANDS: {self.cache_manager.data.get('total_commands', 0)}
APPS TRACKED: {len(self.cache_manager.data.get('applications_executed', []))}
        """
        info_box.setText(system_info)
        layout.addWidget(info_box)
        
        # Buttons
        button_layout = QVBoxLayout()
        
        settings_btn = QPushButton("⚙️ SETTINGS")
        settings_btn.clicked.connect(self.show_settings)
        button_layout.addWidget(settings_btn)
        
        clear_btn = QPushButton("🗑️ CLEAR CACHE")
        clear_btn.clicked.connect(self.clear_cache)
        button_layout.addWidget(clear_btn)
        
        exit_btn = QPushButton("⏹️ EXIT")
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        panel.setLayout(layout)
        panel.setMaximumWidth(350)
        return panel
    
    def create_tabs(self):
        """Erstelle Tab-Panel"""
        tabs = QTabWidget()
        
        # Tab 1: Dashboard
        dashboard = self.create_dashboard_tab()
        tabs.addTab(dashboard, "📊 DASHBOARD")
        
        # Tab 2: Command History
        history = self.create_history_tab()
        tabs.addTab(history, "📜 HISTORY")
        
        # Tab 3: Applications
        applications = self.create_applications_tab()
        tabs.addTab(applications, "🚀 APPS")
        
        # Tab 4: Statistics
        statistics = self.create_statistics_tab()
        tabs.addTab(statistics, "📈 STATS")
        
        return tabs
    
    def create_dashboard_tab(self):
        """Erstelle Dashboard-Tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("SYSTEM DASHBOARD")
        title.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Stats
        stats_layout = QHBoxLayout()
        
        for label, value in [
            ("Total Commands", str(self.cache_manager.data.get('total_commands', 0))),
            ("Apps Tracked", str(len(self.cache_manager.data.get('applications_executed', [])))),
            ("Uptime", "Connected")
        ]:
            stat_widget = QWidget()
            stat_layout = QVBoxLayout()
            stat_layout.addWidget(QLabel(label))
            value_label = QLabel(value)
            value_label.setFont(QFont("Courier New", 16, QFont.Weight.Bold))
            value_label.setStyleSheet("color: #00ff88;")
            stat_layout.addWidget(value_label)
            stat_widget.setLayout(stat_layout)
            stat_widget.setStyleSheet("""
                QWidget {
                    border: 2px solid #00ff88;
                    border-radius: 5px;
                    padding: 10px;
                    background-color: #1a1f3a;
                }
            """)
            stats_layout.addWidget(stat_widget)
        
        layout.addLayout(stats_layout)
        
        # Recent Commands
        layout.addWidget(QLabel("RECENT COMMANDS:"))
        self.recent_list = QListWidget()
        layout.addWidget(self.recent_list)
        
        widget.setLayout(layout)
        return widget
    
    def create_history_tab(self):
        """Erstelle Verlauf-Tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("COMMAND HISTORY:"))
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Time", "Command", "App", "Status"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.history_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        export_btn = QPushButton("📥 EXPORT")
        export_btn.clicked.connect(self.export_history)
        button_layout.addWidget(export_btn)
        
        refresh_btn = QPushButton("🔄 REFRESH")
        refresh_btn.clicked.connect(self.load_history)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        widget.setLayout(layout)
        return widget
    
    def create_applications_tab(self):
        """Erstelle Anwendungen-Tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("TRACKED APPLICATIONS:"))
        
        self.apps_table = QTableWidget()
        self.apps_table.setColumnCount(3)
        self.apps_table.setHorizontalHeaderLabels(["Application", "Executions", "Last Used"])
        self.apps_table.horizontalHeader().setStretchLastSection(True)
        
        # Fülle mit Daten
        apps = self.cache_manager.data.get('applications_executed', [])
        self.apps_table.setRowCount(len(apps))
        
        for row, app in enumerate(apps):
            self.apps_table.setItem(row, 0, QTableWidgetItem(app.get('name', 'Unknown')))
            self.apps_table.setItem(row, 1, QTableWidgetItem(str(app.get('count', 0))))
            last_used = app.get('last_used', 'Unknown')
            if last_used.startswith("20"):
                last_used = last_used.split('T')[0]
            self.apps_table.setItem(row, 2, QTableWidgetItem(last_used))
        
        layout.addWidget(self.apps_table)
        widget.setLayout(layout)
        return widget
    
    def create_statistics_tab(self):
        """Erstelle Statistik-Tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("SYSTEM STATISTICS:"))
        
        # Statistics Display
        stats = self.cache_manager.get_statistics()
        stats_text = QTextEdit()
        stats_text.setReadOnly(True)
        
        stats_content = f"""
╔══════════════════════════════════════╗
║       JARVIS STATISTICS REPORT       ║
╚══════════════════════════════════════╝

📊 GENERAL INFO:
  • Total Commands: {self.cache_manager.data.get('total_commands', 0)}
  • Tracked Applications: {len(self.cache_manager.data.get('applications_executed', []))}
  • Database Size: {len(self.cache_manager.data.get('command_history', []))} entries

🎯 USAGE PATTERNS:
  • Most Used App: {stats.get('most_used_app', 'N/A')}
  • Most Used Command: {stats.get('most_used_command', 'N/A')}
  • Total Runtime: {stats.get('total_time_running', 0)} minutes

📈 TRENDS:
  • Commands Today: {sum(1 for c in self.cache_manager.data.get('command_history', []) if datetime.now().date().isoformat() in c.get('timestamp', ''))}
  • This Week: {len(self.cache_manager.data.get('command_history', []))}

💾 CACHE INFO:
  • Created: {self.cache_manager.data.get('created_at', 'Unknown')}
  • Version: {self.cache_manager.data.get('version', '1.0')}
        """
        
        stats_text.setText(stats_content)
        layout.addWidget(stats_text)
        
        widget.setLayout(layout)
        return widget
    
    def load_history(self):
        """Lade Befehlsverlauf"""
        history = self.cache_manager.get_history()
        
        # Dashboard Liste
        self.recent_list.clear()
        for entry in history[:10]:
            item = QListWidgetItem(f"{entry.get('command', 'Unknown')} ({entry.get('timestamp', '')[:19]}))")
            self.recent_list.addItem(item)
        
        # History Table
        self.history_table.setRowCount(len(history))
        for row, entry in enumerate(history):
            timestamp = entry.get('timestamp', '')[:19]
            command = entry.get('command', 'Unknown')
            app = entry.get('application', '-')
            status = entry.get('status', 'unknown')
            
            self.history_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.history_table.setItem(row, 1, QTableWidgetItem(command))
            self.history_table.setItem(row, 2, QTableWidgetItem(app))
            self.history_table.setItem(row, 3, QTableWidgetItem(status))
    
    def start_listening(self):
        """Starte Spracherkennung"""
        self.status_label.setText("● LISTENING...")
        self.status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.voice_btn.setEnabled(False)
        
        self.voice_worker = VoiceWorker()
        self.voice_worker.command_received.connect(self.process_command)
        self.voice_worker.error_occurred.connect(self.handle_error)
        self.voice_worker.start()
    
    def process_command(self, command):
        """Verarbeite empfangenen Befehl"""
        self.output_text.append(f"Command: {command}")
        self.cache_manager.add_command(command)
        self.load_history()
        
        self.status_label.setText("● PROCESSING")
        self.status_label.setStyleSheet("color: #ffaa00; font-weight: bold;")
        
        QTimer.singleShot(2000, self.reset_status)
        self.voice_btn.setEnabled(True)
    
    def handle_error(self, error):
        """Verarbeite Fehler"""
        self.output_text.append(f"Error: {error}")
        self.reset_status()
        self.voice_btn.setEnabled(True)
    
    def reset_status(self):
        """Setze Status zurück"""
        self.status_label.setText("● STANDBY")
        self.status_label.setStyleSheet("color: #ffaa00; font-weight: bold;")
    
    def show_settings(self):
        """Zeige Einstellungen"""
        settings_text = """
╔══════════════════════════════════╗
║        JARVIS SETTINGS           ║
╚══════════════════════════════════╝

[Config Loaded]

• Wake Word: jarvis
• Language: Deutsch (de-DE)
• Voice Speed: 150 bpm
• Volume: 0.9

[Advanced]
• Cache Location: cache/
• Database: cache/database/
• Logs: cache/logs/

Open .env to modify settings
        """
        self.output_text.setText(settings_text)
    
    def clear_cache(self):
        """Lösche Cache"""
        reply = self.confirm_action()
        if reply:
            self.cache_manager.data = self.cache_manager.create_empty_db()
            self.cache_manager.save_database()
            self.load_history()
            self.output_text.setText("[✓] Cache cleared successfully")
    
    def export_history(self):
        """Exportiere Verlauf"""
        filename = f"jarvis_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"cache/exports/{filename}"
        
        Path("cache/exports").mkdir(parents=True, exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.cache_manager.data, f, indent=2, ensure_ascii=False)
        
        self.output_text.setText(f"[✓] History exported to {filepath}")
    
    def confirm_action(self):
        """Bestätigung für Aktion"""
        return True  # Vereinfacht für Demo

def main():
    """Starte Anwendung"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Moderner Style
    
    window = JarvisGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
