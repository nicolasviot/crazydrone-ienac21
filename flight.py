from geometry import *
from drone import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsItem , QGraphicsEllipseItem , QGraphicsLineItem

"""Ce module contient une unique classe Flight_plan. Ces attributs sont la liste des points et celle des figures utilisées pour les
tracés. Il y a aussi l'attribut drone_plan qui est la liste contenant les éléments du module drone directement lu par le drone"""

class Flight_plan:

    def __init__(self, drawing_points = [Point(0,0)], drone_plan = [], figures = []):
        self.drawing_points = drawing_points
        self.drone_plan = drone_plan
        self.figures = figures

    def pre_draw(self):
      #Cette méthode remplit la liste figure avec les éléments graphiques, il ne restera plus qu'à les afficher sur la scène.

        self.figures = []
        for i,element in enumerate (self.drone_plan[1:]):

            nb_cercle = 0
            for elt in self.drone_plan[:i+1]:
                if elt.type == "CERCLE":
                    nb_cercle += 1

            if element.type == "CERCLE":
                r = float(element.radius)
                xc = float(element.origine.x)
                yc = float(element.origine.y)
                self.figures.append(QGraphicsEllipseItem(-(yc + r / 2) * 50, -(xc + r / 2) * 50, r * 50, r * 50))   #Création des cercles

            elif element.type =="TRAIT":

                index_retranché = i - nb_cercle
                p1 = self.drawing_points[index_retranché]
                p2 = self.drawing_points[index_retranché +1]
                xd = p1.x
                yd = p1.y
                xa = p2.x
                ya = p2.y
                self.figures.append(QGraphicsLineItem(-yd * 50, -xd * 50, -ya * 50, -xa * 50))  #Création des traits