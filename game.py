import sys
from PyQt5 import QtWidgets
from random_number_game import RandomNumberGame

app = QtWidgets.QApplication(sys.argv)  # create an application object
window = RandomNumberGame()  # create an instance of your main window class
window.show()  # show the main window
sys.exit(app.exec_())  # start the event loop
