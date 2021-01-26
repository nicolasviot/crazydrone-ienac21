import logging
import time
from geometry import *
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

URI = 'radio://0/80/2M'
DEFAULT_HEIGHT = 0.5
DEFAULT_VELOCITY = 0.1

logging.basicConfig(level=logging.ERROR)


"""Ce module contient les 4 classes d'objet directement lues par le drone, à savoir le décollage (Take_Off), l'attérrissage
(Land), le cercle (Circle) et la ligne droite (Move_Distance). Toutes ces classes possèdent des attributs différents 
mais au moins un en commun : le "type" pour pouvoir les reconnaître rapidement dans le plan de vol.
Elles ont également la même méthode go_move qui permet la communication avec le drone via la bibliothèque crazyflie"""

class Take_Off:
    #La distance correspond ici à la hauteur atteinte à la fin du décollage

    def __init__(self, distance, velocity, type = "Take_off"):
        self.distance = distance
        self.velocity = velocity
        self.type = type

    def __repr__(self):
        return ("Take off")

    def go_move(self, mc):
        mc.take_off(self.distance, self.velocity)


class Land:

    def __init__(self, velocity = DEFAULT_VELOCITY):
        self.velocity = velocity

    def __repr__(self):
        return ("Land")

    def go_move(self, mc):
        mc.land(self.velocity)


class Circle:

    def __init__(self, radius, direction, origine = Point(0,0), type = "CERCLE", velocity = DEFAULT_VELOCITY, angle_degrees = 360.0):
        self.radius = radius
        self.direction = direction
        self.type = type
        self.velocity = velocity
        self.angle = angle_degrees
        self.origine = origine

        #L'origine n'est pas nécessaire en soi pour le mouvement du drone qui la considère à son emplacement actuel
        #On en a besoin pour les tracés de la scène graphique


    def __repr__(self):
        return("Circle on the " + str(self.direction) + " of " + str(self.radius) + "m radius")


    def go_move(self, mc):
        if self.direction == "Gauche":
            mc.circle_left(self.radius, self.velocity, self.angle)
        else:
            mc.circle_right(self.radius, self.velocity, self.angle)


class Move_Distance:

    def __init__(self, x_distance, y_distance, z_distance, type = "TRAIT", velocity=DEFAULT_VELOCITY):
        self.x_distance = x_distance
        # go forward for positive values
        self.y_distance = y_distance
        # go left for positive values
        self.z_distance = z_distance
        # go up for positive values
        self.velocity = velocity
        self.type = type

    def __repr__(self):
        return ("(" + str(self.x_distance) + "m, " + str(self.y_distance) + "m, " + str(self.z_distance) + "m)")

    def go_move(self, mc):
        mc.move_distance(self.x_distance, self.y_distance, self.z_distance, self.velocity)


#Cette dernière fonction est appelée lors de l'appui du bouton démarrage : elle lance un à un les éléments de trajectoires.

def play_flight_plan(plan_de_vol):
    "Launch the motion scene"
    cflib.crtp.init_drivers(enable_debug_driver=False)
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        mc = MotionCommander(scf, default_height=DEFAULT_HEIGHT)  # with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc
        for move in plan_de_vol:
            move.go_move(mc)