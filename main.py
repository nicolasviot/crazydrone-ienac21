from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
from drone import *
from flight import Flight_plan
from geometry import Point
from files import *
import pyqtgraph as pg


#----------------------------------------------------------------------------------------------------------------------#

                                                #FENETRE PRINCIPALE

#----------------------------------------------------------------------------------------------------------------------#


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):  # Initialise l'ensemble des widgets

        self.fp = Flight_plan()  # On crée le plan de vol dès le départ car il est utilisé dès la création de widgets (voir l.142 / 143)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1090, 865)
        MainWindow.setMinimumSize(QtCore.QSize(1090, 865))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setIconSize(QtCore.QSize(150, 112))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView = QtWidgets.QGraphicsView(self.scene, self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(144, 20, 921, 521))
        self.graphicsView.setObjectName("graphicsView")
        self.clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(954, 20, 111, 31))
        self.clear_button.setObjectName("clear_button")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(13, 270, 121, 20))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 300, 104, 174))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.start_button = QtWidgets.QPushButton(self.layoutWidget)
        self.start_button.setMaximumSize(QtCore.QSize(102, 76))
        self.start_button.setObjectName("start_button")
        self.verticalLayout_2.addWidget(self.start_button)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(992, 510, 61, 20))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(1050, 460, 3, 61))
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(3)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setObjectName("line_3")
        self.y_label = QtWidgets.QLabel(self.centralwidget)
        self.y_label.setGeometry(QtCore.QRect(980, 512, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.y_label.setFont(font)
        self.y_label.setObjectName("y_label")
        self.x_label = QtWidgets.QLabel(self.centralwidget)
        self.x_label.setGeometry(QtCore.QRect(1047, 441, 16, 16))
        self.x_label.setFont(font)
        self.x_label.setObjectName("x_label")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 80, 104, 174))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.trait_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.trait_button.setMaximumSize(QtCore.QSize(102, 76))
        self.trait_button.setText("")
        icon_trait = QtGui.QIcon()
        icon_trait.addPixmap(QtGui.QPixmap("images/bouton_droite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.trait_button.setIcon(icon_trait)
        self.trait_button.setIconSize(QtCore.QSize(90, 68))
        self.trait_button.setObjectName("trait_button")
        self.verticalLayout.addWidget(self.trait_button)
        self.cercle_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.cercle_button.setMaximumSize(QtCore.QSize(102, 76))
        self.cercle_button.setText("")
        icon_cercle = QtGui.QIcon()
        icon_cercle.addPixmap(QtGui.QPixmap("images/bouton_rond.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cercle_button.setIcon(icon_cercle)
        self.cercle_button.setIconSize(QtCore.QSize(90, 68))
        self.cercle_button.setObjectName("cercle_button")
        self.verticalLayout.addWidget(self.cercle_button)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(70, 610, 300, 101))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(80)
        self.gridLayout.setObjectName("gridLayout")
        self.dx_label = QtWidgets.QLabel(self.layoutWidget2)
        self.dx_label.setFont(font)
        self.dx_label.setObjectName("dx_label")
        self.gridLayout.addWidget(self.dx_label, 0, 0, 1, 1)
        self.dx_spinbox = QtWidgets.QDoubleSpinBox(self.layoutWidget2)
        self.dx_spinbox.setObjectName("dx_spinbox")
        self.gridLayout.addWidget(self.dx_spinbox, 0, 1, 1, 1)
        self.dy_spinbox = QtWidgets.QDoubleSpinBox(self.layoutWidget2)
        self.dy_spinbox.setObjectName("dy_spinbox")
        self.gridLayout.addWidget(self.dy_spinbox, 1, 1, 1, 1)
        self.dy_label = QtWidgets.QLabel(self.layoutWidget2)
        self.dy_label.setFont(font)
        self.dy_label.setObjectName("dy_label")
        self.gridLayout.addWidget(self.dy_label, 1, 0, 1, 1)
        self.dz_label = QtWidgets.QLabel(self.layoutWidget2)
        self.dz_label.setFont(font)
        self.dz_label.setObjectName("dz_label")
        self.gridLayout.addWidget(self.dz_label, 2, 0, 1, 1)
        self.dz_spinbox = QtWidgets.QDoubleSpinBox(self.layoutWidget2)
        self.dz_spinbox.setObjectName("dz_spinbox")
        self.gridLayout.addWidget(self.dz_spinbox, 2, 1, 1, 1)
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 560, 350, 32))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.selectorLayout = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.selectorLayout.setContentsMargins(0, 0, 0, 0)
        self.selectorLayout.setSpacing(75)
        self.selectorLayout.setObjectName("selectorLayout")
        self.traj_label = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.traj_label.setFont(font)
        self.traj_label.setObjectName("traj_label")
        self.selectorLayout.addWidget(self.traj_label)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget3)
        self.comboBox.setObjectName("comboBox")
        self.fp.drone_plan.append(Take_Off(0.5,0.1))  # On initialise la combobox et donc le plan de vol par la même occasion avec le Take_Off
        self.comboBox.addItem("Décollage", self.fp.drone_plan[0])
        self.selectorLayout.addWidget(self.comboBox)
        self.direction_combo = QtWidgets.QComboBox(self.centralwidget)
        self.direction_combo.setGeometry(QtCore.QRect(220, 660, 91, 26))
        self.direction_combo.setObjectName("direction_combo")
        self.direction_combo.addItem("Droite", "Droite")
        self.direction_combo.addItem("Gauche", "Gauche")
        self.layoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(70, 720, 300, 24))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.speedLayout = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.speedLayout.setContentsMargins(0, 0, 0, 0)
        self.speedLayout.setSpacing(30)
        self.speedLayout.setObjectName("speedLayout")
        self.speed_label = QtWidgets.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.speed_label.setFont(font)
        self.speed_label.setObjectName("speed_label")
        self.speedLayout.addWidget(self.speed_label)
        self.speed_Slider = QtWidgets.QSlider(self.layoutWidget4)
        self.speed_Slider.setMaximum(500)
        self.speed_Slider.setSingleStep(10)
        self.speed_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.speed_Slider.setObjectName("speed_Slider")
        self.speedLayout.addWidget(self.speed_Slider)
        self.speed_spinBox = QtWidgets.QSpinBox(self.layoutWidget4)
        self.speed_spinBox.setMaximum(500)
        self.speed_spinBox.setSingleStep(10)
        self.speed_spinBox.setObjectName("speed_spinBox")
        self.speedLayout.addWidget(self.speed_spinBox)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(960, 60, 99, 43))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.load_button = QtWidgets.QPushButton(self.widget)
        self.load_button.setMinimumSize(QtCore.QSize(41, 41))
        self.load_button.setMaximumSize(QtCore.QSize(41, 41))
        self.load_button.setText("")
        icon_load = QtGui.QIcon()
        icon_load.addPixmap(QtGui.QPixmap("images/download_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.load_button.setIcon(icon_load)
        self.load_button.setIconSize(QtCore.QSize(32, 32))
        self.load_button.setObjectName("load_button")
        self.horizontalLayout.addWidget(self.load_button)
        self.save_button = QtWidgets.QPushButton(self.widget)
        self.save_button.setMinimumSize(QtCore.QSize(41, 41))
        self.save_button.setMaximumSize(QtCore.QSize(41, 41))
        self.save_button.setText("")
        icon_save = QtGui.QIcon()
        icon_save.addPixmap(QtGui.QPixmap("images/save_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_button.setIcon(icon_save)
        self.save_button.setIconSize(QtCore.QSize(26, 26))
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1090, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.speed_Slider.valueChanged['int'].connect(self.speed_spinBox.setValue)
        self.speed_spinBox.valueChanged['int'].connect(self.speed_Slider.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        "l.214 à 222 : La scène graphique change suivant l'élement selectionné (trait,cercle,etc.) et doit donc être initialisé pour le Take_Off"

        self.direction_combo.hide()
        self.dx_spinbox.hide()
        self.dx_label.hide()
        self.dy_spinbox.hide()
        self.dy_label.hide()
        self.dz_label.setText("Hauteur (m)")
        data_elt = self.comboBox.itemData(0)
        self.speed_spinBox.setValue(int(data_elt.velocity * 100))
        self.dz_spinbox.setValue(data_elt.distance)

        "l.226 à 237 : On connecte l'ensemble des boutons à leur méthode correpondante définie plus bas"

        self.clear_button.clicked.connect(self.clear_scene)
        self.comboBox.activated.connect(self.handleActivated)
        self.trait_button.clicked.connect(self.add_trait)
        self.dx_spinbox.valueChanged.connect(self.dx_modif)
        self.dy_spinbox.valueChanged.connect(self.dy_modif)
        self.dz_spinbox.valueChanged.connect(self.dz_modif)
        self.speed_spinBox.valueChanged.connect(self.vitesse_modif)
        self.direction_combo.activated.connect(self.direction_modif)
        self.cercle_button.clicked.connect(self.add_cercles)
        self.start_button.clicked.connect(self.creation_du_plan)
        self.save_button.clicked.connect(self.save_plan)
        self.load_button.clicked.connect(self.load_plan)

        self.pen_in_evidence = QPen(Qt.blue)
        self.comboBox.activated.connect(self.draw)  #Permet de mettre en surbrillance le segment sélectionné
        self.comboBox.activated.connect(self.create_graphic)

########################################################################################################################
        """Les lignes suivantes ainsi que les 2 méthodes qui suivent permettent la création du graphe d'altitude."""
########################################################################################################################

        self.graphWidget = pg.PlotWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(450, 550, 600, 300))
        self.graphWidget.setTitle("Altitude")
        self.graphWidget.setLabel('left', 'Hauteur (m)')
        self.graphWidget.setLabel('bottom', 'Actions')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setBackground((236, 236, 236))
        self.pen1 = pg.mkPen(color=(0, 0, 0), width=2.5)
        self.pen2 = pg.mkPen(color=(0, 0, 255), width=2.5)
        self.graphWidget.setXRange(0, 3, padding=0.5)
        self.graphWidget.plot([0], [0.5], pen=self.pen1, symbol='+', symbolSize=15)
        self.trait_button.clicked.connect(self.create_graphic)
        self.cercle_button.clicked.connect(self.create_graphic)

    def create_graphic(self, index=0):
        h0 = float(self.fp.drone_plan[0].distance)
        abscissa1, ordinate = [0], [h0]
        current_altitude = h0
        for (i, move) in enumerate(self.fp.drone_plan[:]):      #ordinate[i] est l'altitude de la i-ème étape
            abscissa1.append(i)
            if type(self.fp.drone_plan[i]) is Move_Distance:
                current_altitude += float(self.fp.drone_plan[i].z_distance)
                ordinate.append(current_altitude)
            else:
                ordinate.append(current_altitude)
        self.graphWidget.clear()

        if index != 0 and type(index) is int:                   #Lorsqu'une portion de trajectoire est sélectionnée ou modifiée, on met en évidence cette portion en utilisant un 2ème graphe
            abscissa_1_left, ordinate_1_left = abscissa1[:index + 1], ordinate[:index + 1]
            abscissa_1_right, ordinate_1_right = abscissa1[index + 1:], ordinate[index + 1:]
            self.graphWidget.plot(abscissa_1_left, ordinate_1_left, pen=self.pen1, symbol='+', symbolSize=15)
            self.graphWidget.plot(abscissa_1_right, ordinate_1_right, pen=self.pen1, symbol='+', symbolSize=15)
            abscissa2 = [index - 1, index]
            ordinate2 = [ordinate[index], ordinate[index + 1]]
            self.graphWidget.plot(abscissa2, ordinate2, pen=self.pen2)

        else:
            self.graphWidget.plot(abscissa1, ordinate, pen=self.pen1, symbol='+', symbolSize=15)


    def retranslateUi(self, MainWindow):  # Cette méthode initialise les noms des différents labels utilisés
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Editeur de trajectoire"))
        self.clear_button.setText(_translate("MainWindow", "CLEAR"))
        self.start_button.setText(_translate("MainWindow", "Démarrage"))
        self.y_label.setText(_translate("MainWindow", "Y"))
        self.x_label.setText(_translate("MainWindow", "X"))
        self.dx_label.setText(_translate("MainWindow", "Distance selon X (m)"))
        self.dy_label.setText(_translate("MainWindow", "Distance selon Y (m)"))
        self.dz_label.setText(_translate("MainWindow", "Distance selon Z (m)"))
        self.traj_label.setText(_translate("MainWindow", "Portion de trajectoire :"))
        self.speed_label.setText(_translate("MainWindow", "Vitesse (cm/s)"))

    def clear_scene(self):  #Cette méthode réinitialise la scène graphique, le graphe d'altitude, ainsi que le plan de vol qui contient désormais uniquement le Take_Off
        self.fp.drone_plan = []
        self.comboBox.clear()
        self.fp.drone_plan.append(Take_Off(0.5, 0.1))
        self.comboBox.addItem("Décollage", self.fp.drone_plan[0])
        self.fp.drawing_points[1:] = []
        self.scene.clear()
        data_elt = self.comboBox.itemData(0)
        self.dx_spinbox.hide()
        self.dx_label.hide()
        self.dy_spinbox.hide()
        self.dy_label.hide()
        self.direction_combo.hide()
        self.dz_spinbox.show()
        self.dz_label.show()
        self.dz_label.setText("Hauteur (m)")
        self.dz_spinbox.setValue(data_elt.distance)
        self.speed_spinBox.setValue(int(data_elt.velocity * 100))
        self.graphWidget.clear()
        self.graphWidget.plot([0], [0.5], pen=self.pen1, symbol='+', symbolSize=15)

########################################################################################################################
    """La méthode suivante est appelée à chaque fois qu'un élément de trajectoire est selectionné par l'utilisateur ;
    elle met à jour l'interface suivant le type de celui-ci"""
########################################################################################################################

    def handleActivated(self, index):
        data_elt = self.comboBox.itemData(index)

        if data_elt.type == "TRAIT":
            self.direction_combo.hide()
            self.dx_label.show()
            self.dx_spinbox.show()
            self.dy_label.show()
            self.dy_spinbox.show()
            self.dz_label.show()
            self.dz_spinbox.show()
            self.dx_label.setText("Distance selon X (m)")
            self.dy_label.setText("Distance selon Y (m)")
            self.dz_label.setText("Distance selon Z (m)")
            self.dx_spinbox.setMinimum(-10)
            self.dx_spinbox.setMaximum(10)
            self.dy_spinbox.setMinimum(-10)
            self.dy_spinbox.setMaximum(10)
            self.dz_spinbox.setMinimum(-10)
            self.dz_spinbox.setMaximum(10)
            self.dx_spinbox.setValue(float(data_elt.x_distance))
            self.dy_spinbox.setValue(float(data_elt.y_distance))
            self.dz_spinbox.setValue(float(data_elt.z_distance))
            self.speed_spinBox.setValue(int(float(data_elt.velocity) * 100))

        elif data_elt.type == "CERCLE":
            self.dx_spinbox.show()
            self.dx_label.show()
            self.dy_spinbox.hide()
            self.dy_label.show()
            self.dz_spinbox.hide()
            self.dz_label.hide()
            self.direction_combo.show()
            self.dx_label.setText("Rayon (m)")
            self.dy_label.setText("Direction")
            self.dx_spinbox.setValue(float(data_elt.radius))
            self.speed_spinBox.setValue(int(float(data_elt.velocity) * 100))

        elif data_elt.type == "Take_off":
            self.direction_combo.hide()
            self.dx_spinbox.hide()
            self.dx_label.hide()
            self.dy_spinbox.hide()
            self.dy_label.hide()
            self.dz_spinbox.show()
            self.dz_label.show()
            self.dz_label.setText("Hauteur (m)")
            self.dz_spinbox.setValue(float(data_elt.distance))
            self.speed_spinBox.setValue(int(float(data_elt.velocity) * 100))

########################################################################################################################
    """Les deux méthodes suivantes ajoutent des traits ou des cercles à la scène graphique et au plan de vol. Le menu
    déroulant (comboBox) et le plan de vol (drone_plan) sont identiques."""
########################################################################################################################

    def add_trait(self):

        # A chaque nouveau trait, on ajoute un point (initialisé à (0,0)) pour les tracés ainsi qu'un élément de vol initialisé avec des distances de 0m dans toutes les directions

        i = len(self.fp.drone_plan)
        self.fp.drone_plan.append(Move_Distance(0, 0, 0))
        self.comboBox.addItem("Trait " + str(i), self.fp.drone_plan[i])
        self.fp.drawing_points.append(Point(0, 0))

    def add_cercles(self):

        """A chaque nouveau cercle, on ajoute l'élément de vol correspondant au menu déroulant et au plan de vol initialisé avec un radius de 0m.
        En revanche son origine doit être initialisée avec la bonne valeur : pour se faire, il faut calculer le nombre de cercle totale (nb_cercle)
        et le retrancher à l'indice pour connaître le point d'origine du cercle. En effet les listes drawing_points et drone_plan ne sont pas
        identiques car un cercle ne rajoute pas de point pour le tracé, d'où la nécéssité d'un indice retranché"""

        i = len(self.fp.drone_plan)
        self.fp.drone_plan.append(Circle(0, "Droite"))
        self.comboBox.addItem("Cercle " + str(i), self.fp.drone_plan[i])
        nb_cercle = 0
        for j in range(0, len(self.fp.drawing_points)):
            nb_cercle += self.fp.drawing_points[j].nbcercle
        index_retranché = i - nb_cercle
        self.fp.drawing_points[index_retranché - 1].nbcercle += 1

        index = self.comboBox.currentIndex()
        data = self.comboBox.itemData(index + 1)

        data.origine = self.fp.drawing_points[index_retranché - 1]

########################################################################################################################
    """L'ensemble des méthodes suivantes sont appelées dès que l'utilisateur modifie une caractéristique d'un élément,
    elles mettent à jour les tracés ainsi que le plan de vol"""
########################################################################################################################

    def vitesse_modif(self):

        # Pour un élément quelconque, lorsque le slider ou la spinbox vitesse change de valeur, on met à jour l'élement correspondant

        index = self.comboBox.currentIndex()
        data = self.comboBox.itemData(index)
        data.velocity = self.speed_spinBox.value() / 100

    def dx_modif(self):
        index = self.comboBox.currentIndex()
        data = self.comboBox.itemData(index)

        if data.type == "TRAIT":

            # Ce compteur calcule le nombre de cercle AVANT le point où nous sommes situés

            nb_cercle = 0
            for elt in self.fp.drone_plan[:index]:
                if elt.type == "CERCLE":
                    nb_cercle += 1
            index_retranché = index - nb_cercle

            # Cette partie calcule la modification apportée en comparant l'ancienne version du point avec la nouvelle

            data.x_distance = self.dx_spinbox.value()
            x = self.fp.drawing_points[index_retranché].x
            self.fp.drawing_points[index_retranché].x = self.fp.drawing_points[index_retranché - 1].x + self.dx_spinbox.value()
            dif = self.fp.drawing_points[index_retranché].x - x

            # Enfin on ajoute cette modification à l'ensemble des points situés après le point en question

            for j in range(index_retranché + 1, len(self.fp.drawing_points)):
                self.fp.drawing_points[j].x += dif

        elif data.type == "CERCLE":

            # Seul le radius a besoin d'être mis à jour dans ce cas, il est indépendant des autres éléments
            data.radius = self.dx_spinbox.value()

        self.draw(index)  # On retrace l'ensemble de la trajectoire avec les modifications prises en compte.
        self.create_graphic(index)

    def dy_modif(self):  # Veuillez vous référer à dx_modif pour les commentaires, les 2 méthodes étant pratiquement identiques

        index = self.comboBox.currentIndex()
        data = self.comboBox.itemData(index)

        if data.type == "TRAIT":

            nb_cercle = 0
            for elt in self.fp.drone_plan[:index]:
                if elt.type == "CERCLE":
                    nb_cercle += 1
            index_retranché = index - nb_cercle

            data.y_distance = self.dy_spinbox.value()
            y = self.fp.drawing_points[index_retranché].y
            self.fp.drawing_points[index_retranché].y = self.fp.drawing_points[index_retranché - 1].y + self.dy_spinbox.value()
            dif = self.fp.drawing_points[index_retranché].y - y
            for j in range(index_retranché + 1, len(self.fp.drawing_points)):
                self.fp.drawing_points[j].y += dif

        self.draw(index)
        self.create_graphic(index)

    def dz_modif(self):

        index = self.comboBox.currentIndex()
        data = self.comboBox.itemData(index)

        if data.type == "TRAIT":  # La distance selon z est mise à jour comme pour x et y
            data.z_distance = self.dz_spinbox.value()

        #Il y a ce cas supplémentaire car dans le cadre du take_off, c'est la dz_spinbox qui est utilisée pour recueillir la hauteur
        elif data.type == "Take_off":
            data.distance = self.dz_spinbox.value()

        self.create_graphic(index)

    def direction_modif(self):

        # Modification de la direction du cercle (s'il part sur la droite ou sur la gauche)

        index_elt = self.comboBox.currentIndex()
        data_elt = self.comboBox.itemData(index_elt)
        index_dir = self.direction_combo.currentIndex()
        data_dir = self.direction_combo.itemData(index_dir)

        data_elt.direction = data_dir

########################################################################################################################
    """La méthode suivante s'occupe de tracer l'ensemble des figures, elle est appelée à chaque fois qu'une quelconque
    modification est faite, hormis sur l'altitude, la vitesse ou la direction d'un cercle. En effet ces caractéristiques
    ne se voient pas sur le graphique qui est une vue du dessus. Pour plus d'information sur les dessins, allez voir la
    fonction pre_draw du module flight."""
########################################################################################################################

    def draw(self, index=0):
        self.scene.clear()
        self.fp.pre_draw()
        if index == 0:
            for f in self.fp.figures:
                self.scene.addItem(f)
            self.create_graphic(index)
        else:
            for (i, f) in enumerate(self.fp.figures):
                if i == index - 1:
                    f.setPen(self.pen_in_evidence)
                self.scene.addItem(f)

########################################################################################################################
    """Cette méthode est appelée lors de l'appui du bouton démarrage, elle lance la fonction play_flight_plan du module
    drone avec en argument le plan de vol après avoir ajouté l'étape de l'atterrissage. Voir le module drone pour plus
    d'information"""
########################################################################################################################

    def creation_du_plan(self):
        self.fp.drone_plan.append(Land())
        play_flight_plan(self.fp.drone_plan)

########################################################################################################################
    """Ces deux dernières méthodes sont appelées lors des appuis des boutons pour sauvegarder ou importer un document."""
########################################################################################################################

    def save_plan(self):  # Cela ouvre une nouvelle fenêtre de sauvegarde : voir Fenetre de sauvegarde
        self.save_Form = QtGui.QWidget()
        self.uisave = Ui_Form_Save()
        self.uisave.setupUi(self.save_Form)
        self.save_Form.show()

    def load_plan(self):  # Cela ouvre une nouvelle fenêtre d'import : voir d'import
        self.import_Form = QtGui.QWidget()
        self.uiimport = Ui_Form_Import()
        self.uiimport.setupUi(self.import_Form)
        self.import_Form.show()


#----------------------------------------------------------------------------------------------------------------------#

                                                #FENETRE DE SAUVEGARDE

#----------------------------------------------------------------------------------------------------------------------#


class Ui_Form_Save(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(388, 237)
        Form.setMinimumSize(QtCore.QSize(450, 237))
        Form.setMaximumSize(QtCore.QSize(450, 237))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(51, 41, 360, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(51, 69, 360, 26))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(51, 110, 281, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.save_Button = QtWidgets.QPushButton(Form)
        self.save_Button.setGeometry(QtCore.QRect(140, 150, 100, 40))
        self.save_Button.setMinimumSize(QtCore.QSize(100, 40))
        self.save_Button.setMaximumSize(QtCore.QSize(100, 40))
        self.save_Button.setObjectName("save_Button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.save_Button.clicked.connect(self.save)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Sauvegarde"))
        self.label.setText(_translate("Form", "Veuillez renseigner le nom du fichier (sans espace):"))
        self.label_2.setText(_translate("Form", "Il sera enregistré dans le dossier \"Trajectoires enregistrées\" \n"
                                                "du répertoire de l\'application"))
        self.save_Button.setText(_translate("Form", "Enregistrer"))

    """La méthode save est appelée lors de l'appui du bouton Enregistrer, elle récupère seulement le nom indiqué par
    l'utilisateur et le transmet à la méthode save du module files l.599"""

    def save(self):
        name = self.lineEdit.text()
        save(ui.fp.drone_plan, name)  #Cette méthode save provient du module files
        self.label.hide()
        self.label_2.setText("Trajectoire enregistrée \nVous pouvez fermer cette fenêtre")


#----------------------------------------------------------------------------------------------------------------------#

                                                #FENETRE D'IMPORT

#----------------------------------------------------------------------------------------------------------------------#


class Ui_Form_Import(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(388, 237)
        Form.setMinimumSize(QtCore.QSize(450, 237))
        Form.setMaximumSize(QtCore.QSize(450, 237))
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(51, 41, 360, 30))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(51, 69, 360, 26))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(51, 110, 281, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.import_Button = QtWidgets.QPushButton(Form)
        self.import_Button.setGeometry(QtCore.QRect(140, 150, 100, 40))
        self.import_Button.setMinimumSize(QtCore.QSize(100, 40))
        self.import_Button.setMaximumSize(QtCore.QSize(100, 40))
        self.import_Button.setObjectName("import_Button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.import_Button.clicked.connect(self.load)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Importation"))
        self.label_2.setText(_translate("Form", "Il doit être situé dans le dossier \"Trajectoires enregistrées\" \n"
                                                "du répertoire de l\'application"))
        self.label.setText(_translate("Form", "Veuillez renseigner le nom du fichier (sans espace):"))
        self.import_Button.setText(_translate("Form", "Importer"))

    """La méthode load est appelée lors de l'appui du bouton Importer, elle récupère le nom indiqué par
        l'utilisateur et le transmet à la méthode load du module files l.651. De plus, elle remplie
        le menu déroulant (comboBox) avec les éléments importés (l.653 à 661) et les trace (l.663 et 664)"""

    def load(self):
        ui.comboBox.clear()
        ui.fp.drawing_points, ui.fp.drone_plan = load(self.lineEdit.text())  #load provient du module files

        n = 0
        for elt in ui.fp.drone_plan:
            if n == 0:
                ui.comboBox.addItem("Take off", elt)
            elif elt.type == "TRAIT":
                ui.comboBox.addItem("Trait " + str(n), elt)
            elif elt.type == "CERCLE":
                ui.comboBox.addItem("Cercle " + str(n), elt)
            n += 1

            ui.draw()
            ui.create_graphic()

        self.label.hide()
        self.label_2.setText("Trajectoire chargée \nVous pouvez fermer cette fenêtre")


########################################################################################################################

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())