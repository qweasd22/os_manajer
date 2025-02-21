import os, sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, QFileInfo
import subprocess
import pyscreenshot
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWidgets import QLabel
import time
import pyttsx3
import pyaudio
import threading
import speech_recognition as sr
from PyQt5.QtCore import QSettings


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("My App")
        self.resize(800, 600)
        self.create_ui()

        
    def create_ui(self):
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        central_widget.setLayout(layout)
        self.label = QLabel()
        layout.addWidget(self.label)
        self.start_button = QtWidgets.QPushButton("Старт")
        self.start_button.clicked.connect(self.start_speech)
        layout.addWidget(self.start_button)
        label = QtWidgets.QLabel("Голосовые команды - Файл, Документ, Таблица, Презентация, Выключить, Перезагрузить, Камера, Калькулятор, Клавиатура, Браузер, Блокнот, Скриншот, Папка, VS")
        layout.addWidget(label)

        


        open_button = QtWidgets.QPushButton("Открыть файл")
        word_button = QtWidgets.QPushButton("Открыть Microsoft Word")
        excel_button = QtWidgets.QPushButton("Открыть Microsoft Excel")
        powerpoint_button = QtWidgets.QPushButton("Открыть Microsoft PowerPoint")
        shutdown_button = QtWidgets.QPushButton("Выключить компьютер")
        restart_button = QtWidgets.QPushButton("Перезагрузить компьютер")
        camera_button = QtWidgets.QPushButton("Открыть камеру")
        calculator_button = QtWidgets.QPushButton("Открыть калькулятор")
        keyboard_button = QtWidgets.QPushButton("Открыть клавиатуру")
        browser_button = QtWidgets.QPushButton("Открыть браузер")
        notepad_button = QtWidgets.QPushButton("Открыть блокнот")
        screenshot_button = QtWidgets.QPushButton("Сделать скриншот")
        explorer_button = QtWidgets.QPushButton("Открыть папку с файлами")
        settings_button = QtWidgets.QPushButton("Панель управления")
        vscode_button = QtWidgets.QPushButton("Открыть VS Code")

        open_button.clicked.connect(self.open_fileonnewwindow)
        word_button.clicked.connect(self.open_word)
        excel_button.clicked.connect(self.open_Excel)
        powerpoint_button.clicked.connect(self.open_PowerPoint)
        shutdown_button.clicked.connect(self.shutdown)
        restart_button.clicked.connect(self.restart)
        camera_button.clicked.connect(self.camera)
        calculator_button.clicked.connect(self.calculator)
        keyboard_button.clicked.connect(self.keyboard)
        browser_button.clicked.connect(self.open_browser)
        notepad_button.clicked.connect(self.open_notepad)
        screenshot_button.clicked.connect(self.open_screenshot)
        explorer_button.clicked.connect(self.explorer)
        settings_button.clicked.connect(self.settings)
        vscode_button.clicked.connect(self.vscode)

        layout.addWidget(settings_button)
        layout.addWidget(open_button)
        layout.addWidget(word_button)
        layout.addWidget(excel_button)
        layout.addWidget(powerpoint_button)
        layout.addWidget(shutdown_button)
        layout.addWidget(restart_button)
        layout.addWidget(camera_button)
        layout.addWidget(calculator_button)
        layout.addWidget(keyboard_button)
        layout.addWidget(browser_button)
        layout.addWidget(notepad_button)
        layout.addWidget(screenshot_button)
        layout.addWidget(explorer_button)
        layout.addWidget(vscode_button)

        self.microphone = sr.Microphone()
        self.recognizer = sr.Recognizer()
        self.commands = {"файл": self.open_fileonnewwindow,
                         "документ": self.open_word,
                         "таблица": self.open_Excel,
                         "презентация": self.open_PowerPoint,
                         "выключить": self.shutdown,
                         "перезагрузить": self.restart,
                         "камера": self.camera,
                         "калькулятор": self.calculator,
                         "клавиатура": self.keyboard,
                         "браузер": self.open_browser,
                         "блокнот": self.open_notepad,
                         "скриншот": self.open_screenshot,
                         "папка": self.explorer,
                         "панель": self.settings,
                         "vs": self.vscode}
        self.setCentralWidget(central_widget)
           
    def start_speech(self):
            print('Начало распознавания речи...')
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                timer = QtCore.QTimer(self)
                timer.timeout.connect(lambda: None)
                timer.start(1000)
                max_time = 5
                while timer.remainingTime() > max_time:
                    audio = self.recognizer.listen(source)
                    try:
                        command = self.recognizer.recognize_google(audio, language="ru")
                        self.commands[command]()
                    except sr.UnknownValueError:
                        print("Неизвестная команда")
                    except sr.RequestError:
                        print("Произошла ошибка при распознавании речи")
                    except KeyError:
                        print("Команда не найдена")
                    except SystemExit:
                        timer.stop()
                        break
        
    def open_fileonnewwindow(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Все файлы (*)")
        if fileName:
            filePath = QFileInfo(fileName).absoluteFilePath()
            url = QUrl.fromLocalFile(filePath)
            QDesktopServices.openUrl(url)

    def settings(self):
        subprocess.Popen(["control"])
        
    def explorer(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        QDesktopServices.openUrl(QUrl.fromLocalFile(directory))

    def open_word(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"))

    def open_Excel(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"))

    def open_PowerPoint(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile("C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"))
    def shutdown(self):
        os.system("shutdown /s /t 0")
    def restart(self):
        os.system("shutdown /r /t 0")
        
    def calculator(self):
        os.system("calc.exe")
    def camera(self):
        os.system("start microsoft.windows.camera:")
    def keyboard(self):
        os.system("start c:\windows\system32\osk.exe")
    
    def open_browser(self):
        os.system("start browser.exe")
    def open_notepad(self):
        os.system("start notepad.exe")
    def open_screenshot(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        pyscreenshot.grab().save(directory + "/screenshot.png")
    def vscode(self):
        os.system("code")
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())