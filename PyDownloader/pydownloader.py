from PyQt4.QtCore import *
from PyQt4.QtGui import *
from tkinter import messagebox
import sys

import urllib.request
import tkinter
# import ctypes

# hide tk main window
root = tkinter.Tk()
root.withdraw()

class Downloader(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        layout = QVBoxLayout()

        self.url = QLineEdit()
        self.save_location = QLineEdit()
        self.progress = QProgressBar()
        download = QPushButton("Download")

        self.url.setPlaceholderText("Url")
        self.save_location.setPlaceholderText("Download path")
        # file name is needed

        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.url)
        layout.addWidget(self.save_location)
        layout.addWidget(self.progress)
        layout.addWidget(download)

        self.setLayout(layout)
        self.setWindowTitle("PyDownloader")
        self.setFocus()

        download.clicked.connect(self.download)

    def download(self):
        url = self.url.text()
        save_location = self.save_location.text()
        if url != '':
            urllib.request.urlretrieve(url, save_location, self.report)
        else:
            messagebox.showerror("Url Error", "Please enter valid url")
            # msg = ctypes.windll.user32.MessageBoxW
            # msg(None, "Please enter url", "Error", 0)

    def report(self, blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 100 / totalsize
            self.progress.setValue(int(percent))


app = QApplication(sys.argv)
dlg = Downloader()
dlg.show()
app.exec()