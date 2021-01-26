
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

DEFAULT_HEIGHT = 0.5
DEFAULT_VELOCITY = 0.1

class Takeoff:
    #La distance correspond ici à la hauteur atteinte à la fin du décollage

    def __init__(self, height = DEFAULT_HEIGHT, velocity = DEFAULT_VELOCITY):
        self.height = height
        self.velocity = velocity

    def __repr__(self):
        return ("Takeoff at {} m/s up to an height of {} m".format(self.velocity, self.height))

    def exec(self, mc):
        mc.take_off(self.height, self.velocity)


class Landing:

    def __init__(self, velocity = DEFAULT_VELOCITY):
        self.velocity = velocity

    def __repr__(self):
        return ("Landing at {}".format(self.velocity))

    def exec(self, mc):
        mc.land(self.velocity)


class Circle:

    def __init__(self, radius, direction, velocity = DEFAULT_VELOCITY, angle_degrees = 360.0):
        self.radius = radius
        self.direction = direction
        self.type = type
        self.velocity = velocity
        self.angle = angle_degrees


    def __repr__(self):
        return("Circle on the " + str(self.direction) + " of " + str(self.radius) + "m radius")


    def exec(self, mc):
        if self.direction == "LEFT":
            mc.circle_left(self.radius, self.velocity, self.angle)
        elif self.direction == "RIGHT":
            mc.circle_right(self.radius, self.velocity, self.angle)


class Segment:
    def __init__(self, x_distance, y_distance, z_distance, velocity=DEFAULT_VELOCITY):
        self.x_distance = x_distance
        # go forward for positive values
        self.y_distance = y_distance
        # go left for positive values
        self.z_distance = z_distance
        # go up for positive values
        self.velocity = velocity

    def __repr__(self):
        return ("(" + str(self.x_distance) + "m, " + str(self.y_distance) + "m, " + str(self.z_distance) + "m)")

    def exec(self, mc):
        mc.move_distance(self.x_distance, self.y_distance, self.z_distance, self.velocity)


class FlightPlan():
    def __init__(self):
        self.elts = []


    def addElement(self, elt):
        self.elts.append(elt)

    def __repr__(self):
        res = ""
        for elt in self.elts:
            res += "{}\n".format(elt)
        return res

    def exec(self, mc):
        for elt in self.elts:
            elt.exec(mc)

        



class Drone:

    def __init__(self):
        # Initiate the low level drivers
        cflib.crtp.init_drivers(enable_debug_driver=False)
        self.URI = ''
        self.state = ''
        self.scan()
        self.flightPlan = FlightPlan()


    def scan(self):
        print('Scanning interfaces for Crazyflies...')
        available = cflib.crtp.scan_interfaces()
        print(available)
        if len(available) == 0:
            print('No Crazyflies were found !')
        else:
            print('Found {} Crazyflies, currently using the Crazyflies w/ URI {}'.format(len(available), available[0][0]))
            self.URI = available[0][0]

    def addTakeoff(self, height = DEFAULT_HEIGHT, velocity = DEFAULT_VELOCITY):
        self.flightPlan.addElement(Takeoff(height, velocity))

    def addLanding(self, velocity = DEFAULT_VELOCITY):
        self.flightPlan.addElement(Landing(velocity))

    def addSegment(self, x, y, z, velocity = DEFAULT_VELOCITY):
        self.flightPlan.addElement(Segment(x, y, z, velocity))

    def addCircle(self, radius, direction, velocity = DEFAULT_VELOCITY, angle_degrees = 360.0):
        self.flightPlan.addElement(Circle(radius, direction, velocity, angle_degrees))

    def go(self):
        with SyncCrazyflie(self.URI, cf=Crazyflie(rw_cache='./cache')) as scf:
            # We take off when the commander is created
            with MotionCommander(scf) as mc:
                self.flightPlan.exec(mc)
def main():
    myDrone = Drone()
    #myDrone.addTakeoff()
    myDrone.addSegment(0.5, 0, 0)
    myDrone.addSegment(0, 0.5, 0)
    myDrone.addSegment(-0.5, -0.5, 0)
    myDrone.addCircle(0.5, "RIGHT")
    myDrone.addCircle(0.5, "LEFT")
    myDrone.addLanding()
    print(myDrone.flightPlan)
    myDrone.go()





if __name__ == '__main__':
    main()