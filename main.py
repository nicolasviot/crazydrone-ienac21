import interface
import plan
from PyQt5 import QtWidgets


app = QtWidgets.QApplication([])
plan.w_begin()
main_window = interface.Flight_Plan_Editor()
main_window.setStyleSheet("background-color : rgb(66, 66, 66)")
main_window.show()
app.exec()
