from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QGraphicsRectItem, QMenuBar
from ToolbarLeft import Ui_ToolbarLeft
from ToolbarRight import Ui_ToolbarRight
from elevation_bar import elevation_bar
import plan
import math
import geometry
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPen, QPixmap, QIcon
from PyQt5.QtCore import QSize
import subprocess
import os

FONT_Z_VALUE = 1
ROAD_Z_VALUE = 50
AXIS_Z_VALUE = 30

ROAD_COLOR = "blue"
GRID_COLOR = "lightgrey"
START_COLOR = "green"
LIVE_COLOR = "lightgreen"
ELEV_COLOR = "blue"
ORDINATE_COLOR = "black"

DRONE_BRUSH = QtGui.QBrush(QtGui.QColor(START_COLOR))
FONT_BRUSH = QtGui.QBrush(QtGui.QColor("white"))

GRID_WIDTH = 1
ROAD_WIDTH = 3
ELEV_WIDTH = 2

road_pen = QPen(QtGui.QColor(ROAD_COLOR), ROAD_WIDTH)
road_pen.setCapStyle(QtCore.Qt.RoundCap)

grid_pen = QPen(QtGui.QColor(GRID_COLOR), GRID_WIDTH)
grid_pen.setCapStyle(QtCore.Qt.RoundCap)

elev_pen = QPen(QtGui.QColor(ELEV_COLOR), ELEV_WIDTH)
elev_pen.setCapStyle(QtCore.Qt.RoundCap)

ordinate_grid_pen = QPen(QtGui.QColor(ORDINATE_COLOR), GRID_WIDTH)
ordinate_grid_pen.setCapStyle(QtCore.Qt.RoundCap)

live_pen = QPen(QtGui.QColor(LIVE_COLOR), ROAD_WIDTH, Qt.DashLine)
live_pen.setCapStyle(QtCore.Qt.RoundCap)


class Flight_Plan_Editor(QtWidgets.QWidget):
    """This class is the main class which is used to display the interface"""
    def __init__(self):
        super().__init__()

        root_layout = QtWidgets.QHBoxLayout(self)  # The main layout
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.view.setFixedSize(550, 550)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)

        interface_layout = QtWidgets.QVBoxLayout()  # The layout where we add the two view of the drone's trajectory

        item = QGraphicsRectItem(-270, -270, 545, 545)
        item.setBrush(FONT_BRUSH)
        item.setZValue(0)
        self.scene.addItem(item)  # We add a white font to our scene for the visibility

        self.add_grid_items()  # We add the grid on the top view of the drone

        self.elevation_bar = elevation_bar()  # We create the view of the elevation of the drone

        interface_layout.addWidget(self.view)
        interface_layout.addWidget(self.elevation_bar.view)

        item = QtWidgets.QGraphicsEllipseItem()
        item.setBrush(DRONE_BRUSH)
        item.setZValue(100)
        item.setRect(-5, -5, 10, 10)
        self.scene.addItem(item)  # We add the representation of the beginning point on the top view

        self.road_group = QtWidgets.QGraphicsItemGroup()
        self.road_group.setZValue(ROAD_Z_VALUE)
        self.scene.addItem(self.road_group)  # The group of the road on the top view

        self.elevation_grid_group = QtWidgets.QGraphicsItemGroup()
        self.elevation_grid_group.setZValue(ROAD_Z_VALUE)
        self.elevation_bar.scene.addItem(self.elevation_grid_group)  # The group of the elevation's representation

        self.toolbar_left_widget = QtWidgets.QWidget()
        self.toolbar_left = Ui_ToolbarLeft()
        self.toolbar_left.setupUi(self.toolbar_left_widget)  # Creation of the left toolbar

        self.toolbar_right_widget = QtWidgets.QWidget()
        self.toolbar_right = Ui_ToolbarRight()
        self.toolbar_right.setupUi(self.toolbar_right_widget)  # Creation of the right toolbar

        root_layout.addWidget(self.toolbar_left_widget)  # Construction of the final interface
        root_layout.addLayout(interface_layout)
        root_layout.addWidget(self.toolbar_right_widget)

        menubar = QMenuBar()  # Here we create the QMenuBar
        root_layout.addWidget(menubar)
        helpMenu = menubar.addMenu("Help")
        User_Manual = QtWidgets.QAction("User Manual", self)
        User_Manual.triggered.connect(open_manual)
        helpMenu.addAction(User_Manual)

        self.flight_plan = plan.FlightPlan(self)  # Creation of the flight plan

        self.list_point = [geometry.Point(0, 0)]  # Initialisation of the list of the point where the drone fly

        self.live_element_list = []
        self.live_list_point = []

        self.toolbar_left.pushButton_Line.clicked.connect(self.addElementLine)  # Assigning buttons to functions
        self.toolbar_left.pushButton_CircleRight.clicked.connect(self.addElementCircle_R)
        self.toolbar_left.pushButton_CircleLeft.clicked.connect(self.addElementCircle_L)
        self.toolbar_left.pushButton_Back_Start.clicked.connect(self.back_to_start)
        self.toolbar_right.pushButton_Go.clicked.connect(self.flight_plan.exportPython)
        self.toolbar_right.pushButton_Previous.clicked.connect(self.remove_element)
        self.toolbar_right.pushButton_Stop.clicked.connect(plan.kill_process)
        self.toolbar_left.spinBox_Line_Length.valueChanged.connect(self.live_line)
        self.toolbar_left.spinBox_Line_Angle.valueChanged.connect(self.live_line)
        self.toolbar_left.spinBox_Circle_Radius.valueChanged.connect(self.live_circle)
        self.toolbar_left.spinBox_Speed.valueChanged.connect(self.update_live_scene)
        self.toolbar_left.spinBox_Elevation.valueChanged.connect(self.update_live_scene)

        self.toolbar_left.pushButton_Line.setIcon(QIcon("line.png"))  # Set the icons on the different button and label
        self.toolbar_left.pushButton_Line.setIconSize(QSize(80, 80))
        self.toolbar_left.pushButton_CircleLeft.setIcon(QIcon("Circle_Left.png"))
        self.toolbar_left.pushButton_CircleLeft.setIconSize(QSize(80, 80))
        self.toolbar_left.pushButton_CircleRight.setIcon(QIcon("Circle_Right.png"))
        self.toolbar_left.pushButton_CircleRight.setIconSize(QSize(80, 80))
        self.toolbar_left.pushButton_Back_Start.setIcon(QIcon("House.png"))
        self.toolbar_left.pushButton_Back_Start.setIconSize(QSize(80, 80))
        image_scale = QPixmap("scale.png")
        image_scale2 = image_scale.scaled(150, 130)
        self.toolbar_left.label_scale.setPixmap(image_scale2)
        image_angle = QPixmap("Angles.png")
        image_angle2 = image_angle.scaled(150, 130)
        self.toolbar_left.label_angle.setPixmap(image_angle2)

        self.view.setStyleSheet('QToolTip{background-color: black; color: white; border: black solid 1px}')
        # set the color of the tooltip

    def add_grid_items(self):
        """This function add the grid which represent the top view of the trajectory"""
        grid_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(grid_group)
        grid_group.setZValue(FONT_Z_VALUE)
        for line in draw_grid():
            path = QtGui.QPainterPath()
            path.moveTo(line[0][0], line[0][1])
            path.lineTo(line[1][0], line[1][1])
            item = QtWidgets.QGraphicsPathItem(path, grid_group)
            item.setPen(grid_pen)

    def addElementLine(self):
        """The function call when we click on the line button
        It create a Line object and call the function that draw on the interface"""
        Length = self.toolbar_left.spinBox_Line_Length.value()
        Speed = self.toolbar_left.spinBox_Speed.value()
        if Length == 0:
            return None
        elif Speed <= 0.001:  # We correct the rounding error
            print("Your line as a speed of 0 m/s")
            return None
        else:
            Angle = self.toolbar_left.spinBox_Line_Angle.value()
            Elevation = self.toolbar_left.spinBox_Elevation.value()
            Pdep = self.list_point[-1]
            Line = plan.Line(Length, Angle, Pdep, Speed, Elevation)
            self.flight_plan.addElement(Line)
            Line.pos = len(self.flight_plan.elts) - 1
            line_prev = self.flight_plan.elts[Line.pos - 1]
            i = 1
            while i != Line.pos and self.flight_plan.elts[Line.pos - i].name != "line":  # Calculate the angle send
                # to the Drone
                i = i + 1
                line_prev = self.flight_plan.elts[Line.pos - i]
            if i == Line.pos:
                Line.real_angle = Angle
            else:
                real_angle = (180 + Angle - line_prev.angle) % 360 - 180
                Line.real_angle = real_angle
            self.update_scene()

    def addElementCircle_R(self):
        """The function call when we click on the circle right button
        It create a Circle_Right object and call the function that draw on the interface"""
        radius = self.toolbar_left.spinBox_Circle_Radius.value()
        Speed = self.toolbar_left.spinBox_Speed.value()
        if radius == 0:
            return None
        elif Speed <= 0.001:  # We correct the rounding error
            print("Your circle as a speed of 0 m/s")
            return None
        else:
            Elevation = self.toolbar_left.spinBox_Elevation.value()
            Pdep = self.list_point[-1]
            Circle = plan.Circle_Right(radius, Pdep, Speed, Elevation)
            Circle.pos = len(self.flight_plan.elts)
            Circle.center = self.center_circle(Circle, self.flight_plan.elts, self.list_point)[0]
            self.flight_plan.addElement(Circle)
            self.update_scene()

    def addElementCircle_L(self):
        """The function call when we click on the circle left button
        It create a Circle_Left object and call the function that draw on the interface"""
        radius = self.toolbar_left.spinBox_Circle_Radius.value()
        Speed = self.toolbar_left.spinBox_Speed.value()
        if radius == 0:
            return None
        elif Speed <= 0.001:  # We correct the rounding error
            print("Your circle as a speed of 0 m/s")
            return None
        else:
            Elevation = self.toolbar_left.spinBox_Elevation.value()
            Pdep = self.list_point[-1]
            Circle = plan.Circle_Left(radius, Pdep, Speed, Elevation)
            Circle.pos = len(self.flight_plan.elts)
            Circle.center = self.center_circle(Circle, self.flight_plan.elts, self.list_point)[0]
            self.flight_plan.addElement(Circle)
            self.update_scene()

    def back_to_start(self):
        """The function call when we click on the home button
        It create a Line object to the start point and call the function that draw on the interface"""
        Speed = self.toolbar_left.spinBox_Speed.value()
        Elevation = self.toolbar_left.spinBox_Elevation.value()
        Pdep = self.list_point[-1]
        length = math.sqrt((Pdep.x/100)**2 + (Pdep.y/100)**2)
        if 0.001 >= Pdep.x >= -0.001 and 0.001 >= Pdep.y >= -0.001:  # We correct rounding errors
            return None
        elif Speed <= 0.001:  # We correct the rounding error
            print("Your line as a speed of 0 m/s")
            return None
        else:
            if Pdep.x < 0:
                angle = math.atan(Pdep.y/Pdep.x)*180/math.pi + 90
            elif Pdep.x > 0:
                angle = math.atan(Pdep.y / Pdep.x) * 180 / math.pi - 90
            elif Pdep.x == 0 and Pdep.y < 0:
                angle = 180
            else:
                angle = 0
            Line = plan.Line(length, angle, Pdep, Speed, Elevation)
            self.flight_plan.addElement(Line)
            Line.pos = len(self.flight_plan.elts) - 1
            line_prev = self.flight_plan.elts[Line.pos - 1]
            i = 1
            while i != Line.pos and self.flight_plan.elts[Line.pos - i].name != "line":
                i = i + 1
                line_prev = self.flight_plan.elts[Line.pos - i]
            if i == Line.pos:
                Line.real_angle = angle
            else:
                real_angle = (180 + angle - line_prev.angle) % 360 - 180
                Line.real_angle = real_angle
            self.update_scene()

    def update_scene(self):
        """The function that draw on both the top view and the elevation view
        For each object created or removed this function is called to refresh the 2 views"""
        self.scene.removeItem(self.road_group)
        self.road_group = QtWidgets.QGraphicsItemGroup()
        self.road_group.setZValue(ROAD_Z_VALUE)
        self.list_point = [geometry.Point(0, 0)]
        for element in self.flight_plan.elts:
            path = QtGui.QPainterPath()
            if element.name == "line":
                path.moveTo(element.pdep.x, element.pdep.y)
                Parr = element.pdep.scale_line(element.angle, element.length)
                self.list_point.append(Parr)
                path.lineTo(Parr.x, Parr.y)
                item = QtWidgets.QGraphicsPathItem(path, self.road_group)
                item.setPen(road_pen)
                item.setToolTip('Elevation = ' + str(element.elevation) + '\nSpeed = ' + str(element.speed))
            elif element.name == "circle right" or element.name == "circle left":
                path.moveTo(element.pdep.x, element.pdep.y)
                point = self.center_circle(element, self.flight_plan.elts, self.list_point)[0]
                element.center = point
                path.addEllipse(self.center_circle(element, self.flight_plan.elts, self.list_point)[1],
                                element.radius * 100, element.radius * 100)
                path.moveTo(point.x + element.radius*100, point.y)
                if element.name == "circle left":  # Add the arrow representing the direction of the circle
                    path.lineTo(point.x + element.radius*100 + 10, point.y + 10)
                    path.moveTo(point.x + element.radius*100, point.y)
                    path.lineTo(point.x + element.radius*100 - 10, point.y + 10)
                elif element.name == "circle right":
                    path.lineTo(point.x + element.radius*100 + 10, point.y - 10)
                    path.moveTo(point.x + element.radius*100, point.y)
                    path.lineTo(point.x + element.radius*100 - 10, point.y - 10)
                item = QtWidgets.QGraphicsPathItem(path, self.road_group)
                item.setPen(road_pen)
                item.setToolTip('Elevation = ' + str(element.elevation) + '\nSpeed = ' + str(element.speed))
        self.update_elev(self.flight_plan.elts)
        self.scene.addItem(self.road_group)

    def update_elev(self, list_element):
        """This function is called by the update_scene function and draw and refresh
        the elevation of each object on the elevation interface for each object created or removed"""
        if len(list_element) == 0:
            self.elevation_bar.scene.removeItem(self.elevation_grid_group)
            self.elevation_grid_group = QtWidgets.QGraphicsItemGroup()
            self.elevation_grid_group.setZValue(FONT_Z_VALUE)
            self.elevation_bar.scene.addItem(self.elevation_grid_group)
            return None
        self.elevation_bar.scene.removeItem(self.elevation_grid_group)
        self.elevation_grid_group = QtWidgets.QGraphicsItemGroup()
        self.elevation_grid_group.setZValue(FONT_Z_VALUE)
        self.elevation_bar.scene.removeItem(self.elevation_bar.label_group)
        self.elevation_bar.label_group = QtWidgets.QGraphicsItemGroup()
        list_elevation = []
        for element in list_element:
            list_elevation.append(element.elevation)
        if max(list_elevation) <= 1:  # Adjust label to the maximum height of the drone
            scale = 125
            self.elevation_bar.label_1 = QtWidgets.QGraphicsTextItem("20", self.elevation_bar.label_group)
            self.elevation_bar.label_2 = QtWidgets.QGraphicsTextItem("40", self.elevation_bar.label_group)
            self.elevation_bar.label_3 = QtWidgets.QGraphicsTextItem("60", self.elevation_bar.label_group)
            self.elevation_bar.label_4 = QtWidgets.QGraphicsTextItem("80", self.elevation_bar.label_group)
            self.elevation_bar.label_5 = QtWidgets.QGraphicsTextItem("100", self.elevation_bar.label_group)
        elif 2.001 >= max(list_elevation) > 1:
            scale = 62.5
            self.elevation_bar.label_1 = QtWidgets.QGraphicsTextItem("40", self.elevation_bar.label_group)
            self.elevation_bar.label_2 = QtWidgets.QGraphicsTextItem("80", self.elevation_bar.label_group)
            self.elevation_bar.label_3 = QtWidgets.QGraphicsTextItem("120", self.elevation_bar.label_group)
            self.elevation_bar.label_4 = QtWidgets.QGraphicsTextItem("160", self.elevation_bar.label_group)
            self.elevation_bar.label_5 = QtWidgets.QGraphicsTextItem("200", self.elevation_bar.label_group)
        elif 3.001 >= max(list_elevation) > 2:
            scale = 41.67
            self.elevation_bar.label_1 = QtWidgets.QGraphicsTextItem("60", self.elevation_bar.label_group)
            self.elevation_bar.label_2 = QtWidgets.QGraphicsTextItem("120", self.elevation_bar.label_group)
            self.elevation_bar.label_3 = QtWidgets.QGraphicsTextItem("180", self.elevation_bar.label_group)
            self.elevation_bar.label_4 = QtWidgets.QGraphicsTextItem("240", self.elevation_bar.label_group)
            self.elevation_bar.label_5 = QtWidgets.QGraphicsTextItem("300", self.elevation_bar.label_group)
        elif 4.001 >= max(list_elevation) > 3:
            scale = 31.25
            self.elevation_bar.label_1 = QtWidgets.QGraphicsTextItem("80", self.elevation_bar.label_group)
            self.elevation_bar.label_2 = QtWidgets.QGraphicsTextItem("160", self.elevation_bar.label_group)
            self.elevation_bar.label_3 = QtWidgets.QGraphicsTextItem("240", self.elevation_bar.label_group)
            self.elevation_bar.label_4 = QtWidgets.QGraphicsTextItem("320", self.elevation_bar.label_group)
            self.elevation_bar.label_5 = QtWidgets.QGraphicsTextItem("400", self.elevation_bar.label_group)
        else:
            print("Wrong max elevation of the Drone")
            return None
        self.elevation_bar.label_1.setPos(-267, 38)
        self.elevation_bar.label_2.setPos(-267, 13)
        self.elevation_bar.label_3.setPos(-267, -12)
        self.elevation_bar.label_4.setPos(-267, -37)
        self.elevation_bar.label_5.setPos(-267, -62)
        for element in list_element:
            length = 480 / len(list_element)
            high = element.elevation * scale
            if element.color == ROAD_COLOR:
                elev_path = QtGui.QPainterPath()
                elev_path.moveTo(element.pos * length - 235, 75 - high)
                elev_path.lineTo((element.pos + 1) * length - 235, 75 - high)
                item_elev = QtWidgets.QGraphicsPathItem(elev_path, self.elevation_grid_group)
                item_elev.setPen(elev_pen)
            else:
                live_path = QtGui.QPainterPath()
                live_path.moveTo(element.pos * length - 235, 75 - high)
                live_path.lineTo((element.pos + 1) * length - 235, 75 - high)
                item_live = QtWidgets.QGraphicsPathItem(live_path, self.elevation_grid_group)
                item_live.setPen(live_pen)
            ordinate_grid_path = QtGui.QPainterPath()
            ordinate_grid_path.moveTo((element.pos + 1) * length - 235, -50)
            ordinate_grid_path.lineTo((element.pos + 1) * length - 235, 75)
            item_ordinate_grid = QtWidgets.QGraphicsPathItem(ordinate_grid_path, self.elevation_grid_group)
            item_ordinate_grid.setPen(ordinate_grid_pen)
        self.elevation_bar.scene.addItem(self.elevation_grid_group)
        self.elevation_bar.scene.addItem(self.elevation_bar.label_group)

    def center_circle(self, element, list_element, list_point):  # Not a static method beacause list_element and
        # list_point use self attribute
        """This function is used to calculate the center point of a circle"""
        if element.pos == 0:
            point = geometry.Point(0, -element.radius * 100)
            pt_mid = QPointF(0, -element.radius * 100)
        else:
            Parr = element.pdep
            list_point.append(Parr)
            pt1 = list_point[-2]
            line_prev = list_element[element.pos - 1]
            i = 1
            while i != element.pos and line_prev.name != "line":
                i = i + 1
                line_prev = list_element[element.pos - i]
            if line_prev.name == "line":
                point = pt1.scale_line(line_prev.angle, element.radius)
                pt_mid = QPointF(point.x, point.y)
            else:
                point = geometry.Point(0, -element.radius * 100)
                pt_mid = QPointF(0, -element.radius * 100)
        return point, pt_mid

    def remove_element(self):
        """This function is called when we push on the previous button
        It remove the last element added
        If there is no element added yet, it return an information message
        that tell to the users that nothing can be deleted"""
        if not self.flight_plan.elts:
            print("You have not created an item yet")
        else:
            self.flight_plan.remove_Last_Element()
            self.update_scene()

    def live_line(self):
        """Create a preview of the line we want to add"""
        Length = self.toolbar_left.spinBox_Line_Length.value()
        Angle = self.toolbar_left.spinBox_Line_Angle.value()
        Speed = self.toolbar_left.spinBox_Speed.value()
        Elevation = self.toolbar_left.spinBox_Elevation.value()
        Pdep = self.list_point[-1]
        live_element = plan.Line(Length, Angle, Pdep, Speed, Elevation)
        Parr = live_element.pdep.scale_line(live_element.angle, live_element.length)
        if plan.in_grid(Parr):
            self.live_element_list = self.flight_plan.elts[:]
            self.live_element_list.append(live_element)
            live_element.color = LIVE_COLOR
            live_element.pos = len(self.live_element_list) - 1
        else:
            print("The line exceeds the limits of the grid")
            if len(self.live_element_list) == len(self.flight_plan.elts) or self.live_element_list[-1].name ==\
                    "circle left" or self.live_element_list[-1].name == "circle right":
                return None
            live_element = self.live_element_list[-1]
            self.toolbar_left.spinBox_Line_Angle.setValue(live_element.angle)
            self.toolbar_left.spinBox_Line_Length.setValue(live_element.length)
            Parr = live_element.pdep.scale_line(live_element.angle, live_element.length)
        self.update_scene()
        self.update_elev(self.live_element_list)
        live_path = QtGui.QPainterPath()
        live_path.moveTo(live_element.pdep.x, live_element.pdep.y)
        live_path.lineTo(Parr.x, Parr.y)
        item = QtWidgets.QGraphicsPathItem(live_path, self.road_group)
        item.setPen(live_pen)
        item.setToolTip('Elevation = ' + str(live_element.elevation) + '\nSpeed = ' + str(live_element.speed))

    def live_circle(self):
        """Create a preview of the circle we want to add"""
        radius = self.toolbar_left.spinBox_Circle_Radius.value()
        Speed = self.toolbar_left.spinBox_Speed.value()
        Elevation = self.toolbar_left.spinBox_Elevation.value()
        self.live_list_point = self.list_point[:]
        Pdep = self.live_list_point[-1]
        live_element = plan.Circle_Left(radius, Pdep, Speed, Elevation)
        live_element.pos = len(self.flight_plan.elts)
        live_element.center = self.center_circle(live_element, self.flight_plan.elts, self.live_list_point)[0]
        centre = live_element.center
        p1 = geometry.Point(centre.x, centre.y + live_element.radius * 100)
        p2 = geometry.Point(centre.x, centre.y - live_element.radius * 100)
        p3 = geometry.Point(centre.x + live_element.radius * 100, centre.y)
        p4 = geometry.Point(centre.x - live_element.radius * 100, centre.y)
        if plan.in_grid(p1) and plan.in_grid(p2) and plan.in_grid(p3) and plan.in_grid(p4):
            self.live_element_list = self.flight_plan.elts[:]
            self.live_element_list.append(live_element)
            live_element.color = LIVE_COLOR
            live_element.pos = len(self.live_element_list) - 1
        else:
            print("The circle exceeds the limits of the grid")
            if len(self.live_element_list) == len(self.flight_plan.elts) or self.live_element_list[-1].name == "line":
                return None
            live_element = self.live_element_list[-1]
            self.toolbar_left.spinBox_Circle_Radius.setValue(live_element.radius)
        self.update_scene()
        self.update_elev(self.live_element_list)
        live_path = QtGui.QPainterPath()
        live_path.moveTo(live_element.pdep.x, live_element.pdep.y)
        live_path.addEllipse(self.center_circle(live_element, self.flight_plan.elts, self.list_point)[1],
                             live_element.radius * 100, live_element.radius * 100)
        item = QtWidgets.QGraphicsPathItem(live_path, self.road_group)
        item.setPen(live_pen)
        item.setToolTip('Elevation = ' + str(live_element.elevation) + '\nSpeed = ' + str(live_element.speed))

    def update_live_scene(self):
        """Update the element we are currently adding if we change the speed or height"""
        if self.live_element_list == [] or len(self.live_element_list) == len(self.flight_plan.elts):
            return None
        else:
            if self.live_element_list[-1].name == "line":
                self.live_line()
            else:
                self.live_circle()


def open_manual():
    """This function is used to open the user manual with the shell"""
    if os.uname()[0] == "windows":
        os.startfile("User_Manual.pdf")
    else:
        subprocess.call('open User_Manual.pdf', shell=True)


def draw_grid(pas=50):
    """This function serve to calculate the points used for creating the grid on the top view in add_grid_items"""
    L = []
    for k in range(-250, 251, pas):
        L.append(((k, -250), (k, 250)))
    for i in range(-250, 251, pas):
        L.append(((-250, i), (250, i)))
    return L


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = Flight_Plan_Editor()
    main_window.show()
    app.exec()
