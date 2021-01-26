from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPen

GRID_COLOR = "lightgrey"
AXIS_COLOR = "black"
AXIS_WIDTH = 3
GRID_WIDTH = 1
FONT_Z_VALUE = 0
GRID_Z_VALUE = 1
AXIS_Z_VALUE = 5

FOND_BRUSH = QtGui.QBrush(QtGui.QColor("white"))

grid_pen = QPen(QtGui.QColor(GRID_COLOR), GRID_WIDTH)
axis_pen = QPen(QtGui.QColor(AXIS_COLOR), AXIS_WIDTH)


class elevation_bar(QtWidgets.QWidget):
    """This class is use to display the representation of the altitude of the Drone for each element"""
    def __init__(self):
        super().__init__()
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.view.setFixedSize(550, 200)

        item = QGraphicsRectItem(-270, -95, 545, 195)  # We add a white font
        item.setBrush(FOND_BRUSH)
        item.setZValue(FONT_Z_VALUE)
        self.scene.addItem(item)

        self.label_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(self.label_group)

        self.grid_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(self.grid_group)
        self.grid_group.setZValue(GRID_Z_VALUE)
        self.add_grid_items()

        self.axis_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(self.axis_group)
        self.axis_group.setZValue(AXIS_Z_VALUE)
        self.add_axis_items()

        self.label_orig = QtWidgets.QGraphicsTextItem("0")
        self.label_orig.setPos(-253, 63)
        self.scene.addItem(self.label_orig)

        self.label_1 = QtWidgets.QGraphicsTextItem("20", self.label_group)
        self.label_1.setPos(-267, 38)

        self.label_2 = QtWidgets.QGraphicsTextItem("40", self.label_group)
        self.label_2.setPos(-267, 13)

        self.label_3 = QtWidgets.QGraphicsTextItem("60", self.label_group)
        self.label_3.setPos(-267, -12)

        self.label_4 = QtWidgets.QGraphicsTextItem("80", self.label_group)
        self.label_4.setPos(-267, -37)

        self.label_5 = QtWidgets.QGraphicsTextItem("100", self.label_group)
        self.label_5.setPos(-267, -62)

        self.label_height = QtWidgets.QGraphicsTextItem("Height (cm)")
        self.label_height.setPos(-257, -95)
        self.scene.addItem(self.label_height)

        self.label_number = QtWidgets.QGraphicsTextItem("Number of movement")
        self.label_number.setPos(135, 75)
        self.scene.addItem(self.label_number)

    def add_grid_items(self):
        """This function add the grid which represent the different elevation of the drone"""
        for line in draw_grid():
            path = QtGui.QPainterPath()
            path.moveTo(line[0][0], line[0][1])
            path.lineTo(line[1][0], line[1][1])
            item = QtWidgets.QGraphicsPathItem(path, self.grid_group)
            item.setPen(grid_pen)

    def add_axis_items(self):
        """This function add the two axis on the elevation interface"""
        path = QtGui.QPainterPath()
        path.moveTo(-235, 75)
        path.lineTo(-235, -75)
        path.moveTo(-235, -75)
        path.lineTo(-240, -70)
        path.moveTo(-235, -75)
        path.lineTo(-230, -70)
        path.moveTo(-235, 75)
        path.lineTo(250, 75)
        path.moveTo(250, 75)
        path.lineTo(245, 70)
        path.moveTo(250, 75)
        path.lineTo(245, 80)
        item = QtWidgets.QGraphicsPathItem(path, self.axis_group)
        item.setPen(axis_pen)


def draw_grid(pas=-25):
    """This function serve to calculate the points used for creating the grid in add_grid_items"""
    L = []
    for i in range(75, -71, pas):
        L.append(((-235, i), (250, i)))
    return L
