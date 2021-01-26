"""Plan module
It allows to create the flight plan in connection with the graphical interface"""

import cflib.crtp
import geometry
import subprocess
import os

# color of the road
ROAD_COLOR = "blue"

# velocity
V = "0.5"

# space
esp = "   "


# functions that write instructions for the drone

def sleep(time):
    return "time.sleep({0})".format(str(time))


def forward(dist, velocity):
    return "mc.forward({0}, velocity = {1})".format(str(dist), str(velocity))


def back(dist, velocity):
    return "mc.back({0}, velocity = {1})".format(str(dist), str(velocity))


def up(dist):
    return "mc.up({0}, velocity = {1})".format(str(dist), V)


def down(dist):
    return "mc.down({0}, velocity = {1})".format(str(dist), V)


def right(dist):
    return "mc.right({0}, velocity = {1})".format(str(dist), V)


def left(dist):
    return "mc.left({0}, velocity = {1})".format(str(dist), V)


def circle_right(rayon, velocity, angle):
    return "mc.circle_right({0}, velocity = {1}, angle_degrees={2})".format(str(rayon), str(velocity), str(angle))


def circle_left(rayon, velocity, angle):
    return "mc.circle_left({0}, velocity = {1}, angle_degrees={2})".format(str(rayon), str(velocity), str(angle))


def turn_left(angle):
    return "mc.turn_left({0})".format(str(angle))


def turn_right(angle):
    return "mc.turn_right({0})".format(str(angle))


# function that will write the URI of the drone in scan.txt file

def w_scan():
    """Scans the drone's ID and writes it in the scan.txt file."""
    L = ""
    cflib.crtp.init_drivers(enable_debug_driver=False)
    for i in cflib.crtp.scan_interfaces():
        L = L + str(i[0])
    with open("scan.txt", 'w') as file:
        file.write(L)


# functions that will be written in the instruction.py file

def w_begin():
    """Writes the beginning of the instruction.py file in the begin.txt file.
    This allows a single connection to the drone."""
    SCAN = ""
    try:
        w_scan()
        with open("scan.txt", 'r') as file:
            for line in file:
                SCAN = str(line)
    except IndexError:
        print("Drone's ID not found. Please close the interface and turn on the drone.")

    with open('begin.txt', 'w') as file:
        file.write(
            "import logging\nimport time\nimport cflib.crtp\nfrom cflib.crazyflie import Crazyflie\nfrom cflib.crazyflie.syncCrazyflie import SyncCrazyflie\nfrom cflib.positioning.motion_commander import MotionCommander\n\n")
        file.write("URI = ")
        file.write("'" + SCAN + "'" + "\n")
        file.write("logging.basicConfig(level=logging.ERROR) \n\n\n")
        file.write("if __name__ == '__main__':\n\n")
        file.write(esp + "cflib.crtp.init_drivers(enable_debug_driver=False)\n")
        file.write(esp + "with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:\n")
        file.write(esp + esp + "with MotionCommander(scf) as mc:\n")
        file.write(esp + esp + esp + "time.sleep(3)\n")


def w_end():
    """Writes the end of the instruction.py file."""
    with open('instruction.py', 'a') as instr_file:
        instr_file.write(esp + esp + esp + "mc.stop()\n")
        instr_file.write(esp + esp + esp + "print('Work completed !')\n")


def w_elevation(diff):
    """Writes up and down instruction on the instruction.py file."""
    with open('instruction.py', 'a') as instr_file:
        if diff > 0:
            instr_file.write(esp + esp + esp + up(diff) + "\n")
        else:
            instr_file.write(esp + esp + esp + down(abs(diff)) + "\n")
        instr_file.write(esp + esp + esp + sleep(2) + "\n")


# Objects for the flight plan

class Line:
    """The objective is to create "line" objects that will be added to the flight plan"""

    def __init__(self, length, angle, pdep, speed, elevation, real_angle=0, pos=0):
        self.name = "line"
        self.length = length
        self.angle = angle
        self.pdep = pdep
        self.color = ROAD_COLOR
        self.speed = speed
        self.elevation = elevation
        self.real_angle = real_angle
        self.pos = pos

    def write(self):
        with open('instruction.py', 'a') as instr_file:
            if self.real_angle > 0:
                instr_file.write(esp + esp + esp + turn_right(self.real_angle) + "\n")
            else:
                instr_file.write(esp + esp + esp + turn_left(abs(self.real_angle)) + "\n")
            instr_file.write(esp + esp + esp + forward(self.length, self.speed) + "\n")
            instr_file.write(esp + esp + esp + sleep(1) + "\n")


class Circle_Right:
    """The objective is to create "circle right" objects that will be added to the flight plan"""

    def __init__(self, radius, pdep, speed, elevation, pos=0, center=geometry.Point(0, 0)):
        self.name = "circle right"
        self.radius = radius
        self.pdep = pdep
        self.pos = pos
        self.color = ROAD_COLOR
        self.speed = speed
        self.elevation = elevation
        self.center = center

    def write(self):
        with open('instruction.py', 'a') as instr_file:
            instr_file.write(esp + esp + esp + circle_right(self.radius, self.speed, 360) + "\n")
            instr_file.write(esp + esp + esp + sleep(1) + "\n")


class Circle_Left:
    """The objective is to create "circle left" objects that will be added to the flight plan"""

    def __init__(self, radius, pdep, speed, elevation, pos=0, center=geometry.Point(0, 0)):
        self.name = "circle left"
        self.radius = radius
        self.pdep = pdep
        self.pos = pos
        self.color = ROAD_COLOR
        self.speed = speed
        self.elevation = elevation
        self.center = center

    def write(self):
        with open('instruction.py', 'a') as instr_file:
            instr_file.write(esp + esp + esp + circle_left(self.radius, self.speed, 360) + "\n")
            instr_file.write(esp + esp + esp + sleep(1) + "\n")


class FlightPlan:
    """Object FlightPlan is created in the module Interface.
    Allows you to create a list of previously defined objects.
    This list will represent the flight plan and can be modified
    during the use of the interface."""

    def __init__(self, angle=0):
        self.elts = []
        self.last_position = geometry.Point(0, 0)
        self.angle = angle

    def __repr__(self):
        L = []
        for elt in self.elts:
            if elt.name == "line":
                L.append((str(elt.name), str(elt.length), str(elt.angle)))
            elif elt.name == "circle right":
                L.append((str(elt.name), str(elt.radius)))
            elif elt.name == "circle left":
                L.append((str(elt.name), str(elt.radius)))
        return L

    def addElement(self, elt):
        """"Adds an object to the flight plan list by checking that it does not go beyond the grid"""
        if elt.name == "line":
            Parr = elt.pdep.scale_line(elt.angle, elt.length)
            if in_grid(Parr):
                self.elts.append(elt)
            else:
                print("The line exceeds the limits of the grid")
        else:
            centre = elt.center
            p1 = geometry.Point(centre.x, centre.y + elt.radius * 100)
            p2 = geometry.Point(centre.x, centre.y - elt.radius * 100)
            p3 = geometry.Point(centre.x + elt.radius * 100, centre.y)
            p4 = geometry.Point(centre.x - elt.radius * 100, centre.y)
            if in_grid(p1) and in_grid(p2) and in_grid(p3) and in_grid(p4):
                self.elts.append(elt)
            else:
                print("The circle exceeds the limits of the grid")

    def remove_Last_Element(self):
        """Deletes the last object from the flight plan list"""
        self.elts.pop()

    def exportPython(self):
        """It writes in the instruction.py file the instructions for the drone from the list of flight plan elements.
        It also launches the instruction.py file. This function is called by using the "go" button."""
        with open('instruction.py', "w") as instr_file:
            instr_file.write("")
        with open('begin.txt', "r") as file:
            with open('instruction.py', "a") as instr_file:
                for line in file:
                    instr_file.write(line)
        for i in range(len(self.elts)):
            if i == 0 and self.elts[i].elevation != 0.3:
                w_elevation(self.elts[i].elevation - 0.3)
            elif i > 0 and self.elts[i].elevation != self.elts[i - 1].elevation:
                w_elevation(self.elts[i].elevation - self.elts[i - 1].elevation)
            self.elts[i].write()
        w_end()
        path = os.path.realpath(__file__).split('/')
        del path[-1]
        path = '/'.join(path)
        subprocess.call('python3 ' + str(path) + '/instruction.py &', shell=True)


def in_grid(point):
    """Checks that a point is in the predefined grid"""
    if (-250 <= point.x <= 250) and (-250 <= point.y <= 250):
        return True
    return False


def kill_process():
    """For the emergency stop button"""
    subprocess.call('pkill -f instruction.py', shell=True)
