from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from tkinter import messagebox
import sys

import urllib.request
# import tkinter
# import ctypes

## hide tk main window
#root = tkinter.Tk()
#root.withdraw()

class Downloader(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        systray_icon = QIcon("ESALogo.png")
        systray = QSystemTrayIcon(systray_icon, self)

        menu = QMenu()
        restore = QAction("Restore", self)
        close = QAction("Close", self)

        menu.addActions([restore, close])
        systray.setContextMenu(menu)

        systray.show()

        close.triggered.connect(self.close)

        layout = QVBoxLayout()

        self.url = QLineEdit()
        self.save_location = QLineEdit()
        self.progress = QProgressBar()
        download = QPushButton("Download")
        browse = QPushButton("Browse path")

        self.url.setPlaceholderText("Url") # http://spatialkeydocs.s3.amazonaws.com/FL_insurance_sample.csv.zip
        self.save_location.setPlaceholderText("Download path") # C:\Users\wguo\Downloads
        # file name is needed

        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.url)
        layout.addWidget(self.save_location)
        layout.addWidget(browse)
        layout.addWidget(self.progress)
        layout.addWidget(download)

        self.setLayout(layout)
        self.setWindowTitle("PyDownloader")
        self.setFocus()

        download.clicked.connect(self.download)
        browse.clicked.connect(self.browse_file)

    def browse_file(self):
        save_file = QFileDialog.getSaveFileName(self, caption="Save file as", directory=".", filter="All Files (*.*)")
        self.save_location.setText(QDir.toNativeSeparators(save_file))

    def download(self):
        url = self.url.text()
        save_location = self.save_location.text()
        if url != '':
            try:
                urllib.request.urlretrieve(url, save_location, self.report)
                QMessageBox.information(self, "Information", "Download completed")
                self.progress.setValue(0)
                self.url.setText("")
                self.save_location.setText("")
            except Exception:
                QMessageBox.warning(self, "Warning", "Download failed")
                return
        else:
            # messagebox.showerror("Url Error", "Please enter valid url")
            # msg = ctypes.windll.user32.MessageBoxW
            # msg(None, "Please enter url", "Error", 0)
            QMessageBox.warning(self, "Ulr Error", "Please enter valid url")
            self.url.setFocus()

    def report(self, blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 100 / totalsize
            self.progress.setValue(int(percent))


app = QApplication(sys.argv)
dlg = Downloader()
dlg.show()
app.exec()