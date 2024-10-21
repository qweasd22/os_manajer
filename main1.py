import speech_recognition as sr
from PyQt5 import QtCore, QtGui, QtWidgets
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        # Настройка кнопок
        self.start_button = QtWidgets.QPushButton("Старт")
        self.stop_button = QtWidgets.QPushButton("Стоп")
        self.say_hello_button = QtWidgets.QPushButton("Привет")
        self.play_music_button = QtWidgets.QPushButton("Музыка")
        self.open_browser_button = QtWidgets.QPushButton("Браузер")
        
        # Связь кнопок с функциями
        self.start_button.clicked.connect(self.start_speech)
        self.stop_button.clicked.connect(self.stop_speech)
        self.say_hello_button.clicked.connect(self.say_hello)
        self.play_music_button.clicked.connect(self.play_music)
        self.open_browser_button.clicked.connect(self.open_browser)
        
        # Размещение кнопок на экране
        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.say_hello_button)
        layout.addWidget(self.play_music_button)
        layout.addWidget(self.open_browser_button)
        
        # Создание микрофона и функция для распознавания речи
        self.microphone = sr.Microphone()
        self.recognizer = sr.Recognizer()
        self.commands = {"Привет": self.say_hello, "Музыка": self.play_music, "Браузер": self.open_browser}
        
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
    
    def stop_speech(self):
        print('Остановка распознавания речи...')
        
        
    
    def say_hello(self):
        print('Привет!')
        pass
    
    def play_music(self):
        try:
            command = input("Какую музыку хотите послушать? ")
            if not command:
                return
            os.system(f'mpg321 "{command}"')
        except Exception as e:
            print(e)
    
    def open_browser(self):
        try:
            command = input("Куда открыть браузер? ")
            if not command:
                return
            os.system(f'xdg-open "{command}"')
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()