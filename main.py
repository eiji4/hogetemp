import csv
import datetime
import playsound
import threading
from PySide2 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Notes Creator")
        self.setGeometry(1000, 500, 400, 300)
        self.music_label = QtWidgets.QLabel("Music File Path")
        self.music_file = QtWidgets.QLineEdit(r"D:\music.mp3")
        self.csv_label = QtWidgets.QLabel("CSV File Path")
        self.csv_file = QtWidgets.QLineEdit(r"D:\out.csv")
        self.play_button = QtWidgets.QPushButton("Play")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.music_label)
        self.layout.addWidget(self.music_file)
        self.layout.addWidget(self.csv_label)
        self.layout.addWidget(self.csv_file)
        self.layout.addWidget(self.play_button)
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.play_button.clicked.connect(self.play)

        self.is_playing = False
        self.played_time = None
        self.data = []

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if self.is_playing:
            pressed = event.key()
            time = datetime.datetime.now()
            time_diff = time - self.played_time
            print(time_diff)
            if pressed == QtCore.Qt.Key_A:
                self.data.append([time_diff, "A"])
            elif pressed == QtCore.Qt.Key_S:
                self.data.append([time_diff, "S"])
            elif pressed == QtCore.Qt.Key_D:
                self.data.append([time_diff, "D"])

    def write_csv(self):
        csv_file = self.csv_file.text()
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(self.data)

    def play(self):
        self.data = []
        self.thread1 = threading.Thread(target=self.create_play_thread)
        self.thread1.start()
        self.is_playing = True
        self.play_button.setEnabled(False)
        self.music_file.setEnabled(False)
        self.csv_file.setEnabled(False)
        print("play clicked")
        self.setFocus()

    def create_play_thread(self):
        thread1 = threading.Thread(target=self.play_internal)
        self.played_time = datetime.datetime.now()
        thread1.start()
        thread1.join()
        print("done")
        self.write_csv()
        self.is_playing = False
        self.play_button.setEnabled(True)
        self.music_file.setEnabled(True)
        self.csv_file.setEnabled(True)

    def play_internal(self):
        file = self.music_file.text()
        playsound.playsound(file)


app = QtWidgets.QApplication()
window = MainWindow()
window.show()
app.exec_()