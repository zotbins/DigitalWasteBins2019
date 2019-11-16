import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy, QVBoxLayout
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QByteArray, QSize
from PyQt5.QtGui import QMovie

# Added QSizePolicy, QVBoxLayout, QByteArray, QMovie

class ImagePlayer(QWidget):
    def __init__(self, filename, title, parent=None):
        QWidget.__init__(self, parent)

        # Obtain screen size and other dimensions
        screenSize = QtWidgets.QDesktopWidget().screenGeometry(-1)
        width = screenSize.width()
        height = screenSize.height()

        # Load the file into a QMovie
        self.movie = QMovie(filename, QByteArray(), self)

        # Set the size of the movie
        # size = QSize()
        # size = size.scaled(2000.000 / 10, 6000.000 / 10, QtCore.Qt.KeepAspectRatio)
        # self.movie.setScaledSize(size)

        self.movie_screen = QLabel()
        # Make label fit the gif
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)

        # Create the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)

        self.setLayout(main_layout)

        # Add the QMovie object to the label
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()

    def jumpToFrame(self, frame : int):
        self.movie.jumpToFrame(frame)

if __name__ == "__main__":
    gif = "Thickey.gif"
    app = QApplication(sys.argv)
    player = ImagePlayer(gif, "was")
    player.show()
    sys.exit(app.exec_())