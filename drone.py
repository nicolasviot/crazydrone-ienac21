
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

DEFAULT_HEIGHT = 0.5
DEFAULT_VELOCITY = 0.1
COUNTER_CLOCKWISE = 1
CLOCKWISE = -1
        
class _Takeoff:
    """
    private class. Define a takeoff
    Optionnal, the drone will takeoff on motion commander initialization
    """
    def __init__(self, height = DEFAULT_HEIGHT, velocity = DEFAULT_VELOCITY):
        self.height = height
        self.velocity = velocity

    def __repr__(self):
        return ("Takeoff at {} m/s up to an height of {} m".format(self.velocity, self.height))

    def update(self, height, velocity):
        self.height = height
        self.velocity = velocity

    def execution(self, mc):
        mc.take_off(self.height, self.velocity)

class _Landing:
    """
    private class. Define a landing
    """
    def __init__(self, velocity = DEFAULT_VELOCITY):
        self.velocity = velocity

    def __repr__(self):
        return ("Landing at {}".format(self.velocity))

    def update(self, velocity):
        self.velocity = velocity

    def execution(self, mc):
        mc.land(self.velocity)


class _Circle:
    """
    private class. Define a Circle
    """
    def __init__(self, radius, direction, velocity = DEFAULT_VELOCITY, angle_degrees = 360.0):
        self.radius = radius
        self.direction = direction
        self.velocity = velocity
        self.angle = angle_degrees


    def __repr__(self):
        if self.direction == COUNTER_CLOCKWISE:
            return("Counter-CLOCKWISE circle of radius {}".format(self.radius))
        elif self.direction == CLOCKWISE:
            return("CLOCKWISE circle of radius {}".format(self.radius))

    def update(self, radius, direction, velocity, angle_degrees):
        self.radius = radius
        self.direction = direction
        self.velocity = velocity
        self.angle = angle_degrees

    def execution(self, mc):
        if self.direction == CLOCKWISE:
            mc.circle_CLOCKWISE(self.radius, self.velocity, self.angle)
        elif self.direction == COUNTER_CLOCKWISE:
            mc.circle_COUNTER_CLOCKWISE(self.radius, self.velocity, self.angle)


class _Segment:
    """
    Private class. Define a 3D segment
    """
    def __init__(self, x_distance, y_distance, z_distance, velocity=DEFAULT_VELOCITY):
        self.x_distance = x_distance
        # go forward for positive values
        self.y_distance = y_distance
        # go CLOCKWISE for positive values
        self.z_distance = z_distance
        # go up for positive values
        self.velocity = velocity

    def __repr__(self):
        return ("(" + str(self.x_distance) + "m, " + str(self.y_distance) + "m, " + str(self.z_distance) + "m)")

    def update(self, x_distance, y_distance, z_distance, velocity):
        self.x_distance = x_distance
        # go forward for positive values
        self.y_distance = y_distance
        # go CLOCKWISE for positive values
        self.z_distance = z_distance
        # go up for positive values
        self.velocity = velocity

    def execution(self, mc):
        mc.move_distance(self.x_distance, self.y_distance, self.z_distance, self.velocity)


class _FlightPlan():
    """
    Private class. Define a container for the drone's intructions
    """

    def __init__(self):

        #We store instructions in a dictionnary.
        self.elts = {}
        self.instructionPointer = 0

    def __repr__(self):
        res = ""
        for key in self.elts.keys():
            res += " {} : {}\n".format(key, self.elts[key])
        return res

    def addElement(self, elt):
        #Add an instruction to the flight plan. Return an identifier for this instruction
        self.elts[self.instructionPointer] = elt
        self.instructionPointer += 1
        return self.instructionPointer - 1

    def removeElement(self, identifier):
        self.elts.pop(identifier)

    def getElement(self, identifier):
        return self.elts[identifier]

    def execution(self, mc):
        for key in self.elts.keys():
            self.elts[key].execution(mc)

        



class Drone:
    """
        Public Class. Exposes Methods for adding, updating or removing instructions from the flight plan
    """

    def __init__(self):
        # Initiate the low level drivers
        cflib.crtp.init_drivers(enable_debug_driver=False)
        self.URI = ''
        self.state = ''
        self.scan()
        self.flightPlan = _FlightPlan()


    def scan(self):
        print('Scanning interfaces for Crazyflies...')
        available = cflib.crtp.scan_interfaces()
        if len(available) == 0:
            raise Exception("No Crazyflies found !")
        else:
            print('Found {} Crazyflies, currently using the Crazyflies w/ URI {}'.format(len(available), available[0][0]))
            self.URI = available[0][0]

    def addTakeoff(self, height = DEFAULT_HEIGHT, velocity = DEFAULT_VELOCITY):
           #Add a Takeoff instruction to this drone object. Returns the Instruction ID
        return self.flightPlan.addElement(_Takeoff(height, velocity))

    def addLanding(self, velocity = DEFAULT_VELOCITY):
        #Add a Landing instruction to this drone object. Returns the Instruction ID
        return self.flightPlan.addElement(_Landing(velocity))

    def addSegment(self, x, y, z, velocity = DEFAULT_VELOCITY):
        #Add a Segment instruction to this drone object. Returns the Instruction ID
        return self.flightPlan.addElement(_Segment(x, y, z, velocity))

    def addCircle(self, radius, direction, velocity = DEFAULT_VELOCITY, angle_degrees = 360.0):
        #Add a Circle instruction to this drone object. Returns the Instruction ID
        return self.flightPlan.addElement(_Circle(radius, direction, velocity, angle_degrees))

    def removeInstruction(self, identifier):
        #remove the instruction with id identifier
        self.flightPlan.removeElement(identifier)

    def updateCircle(self, identifier, new_radius, new_direction, new_velocity = DEFAULT_VELOCITY, new_angle_degrees = 360.0):
        self.flightPlan.getElement(identifier).update(new_radius, new_direction, new_velocity, new_angle_degrees)

    def updateSegment(self, identifier, newX, newY, newZ, velocity = DEFAULT_VELOCITY):
        self.flightPlan.getElement(identifier).update(newX, newY, newZ, velocity)

    def updateLanding(self, identifier, velocity = DEFAULT_VELOCITY):
        self.flightPlan.getElement(identifier).update(velocity)        
    
    def updateTakeoff(self, identifier, height = DEFAULT_HEIGHT, velocity = DEFAULT_VELOCITY):
        self.flightPlan.getElement(identifier).update(height, velocity)
    
    def showFlightPlan(self):
        print(self.flightPlan)

    def go(self):
        with SyncCrazyflie(self.URI, cf=Crazyflie(rw_cache='./cache')) as scf:
            # We take off when the commander is created
            with MotionCommander(scf) as mc:
                self.flightPlan.execution(mc)
        

def main():

    #We create a drone object, it will launch a scan for crazyflies using the crazyradio. 
    #In case no crazyflies are found, raise an exception
    try: 
        myDrone = Drone()
    except Exception as e:
        print(e.args)
        return

    #We add instructions to the drone flight plan and store their identifier (optionnal, for later deletion or modification)
    #Segment are define by 3 cordinate, X (forward, m), Y (left, m), Z (up, m) and an optional velocity
    #Circle are define by a radius (m), a rotation (CLOCKWISE or COUNTER_CLOCKWISE), an optional velocity and an optional arc (angle_degree) for part of circle
    instr1 = myDrone.addSegment(0.5, 0, 0)
    instr2 = myDrone.addSegment(0, 0.5, 0)
    instr3 = myDrone.addSegment(-0.5, -0.5, 0)
    instr4 = myDrone.addCircle(0.5, CLOCKWISE)
    instr5 = myDrone.addCircle(0.5, COUNTER_CLOCKWISE)
    instr6 = myDrone.addLanding()
    #Here is how the flight plan looks like
    myDrone.showFlightPlan()


    #We can remove a specific instruction, using its identifier 
    myDrone.removeInstruction(instr2)
    print("\n\n")
    myDrone.showFlightPlan()


    #We can also update a specific instruction using its identifier
    print("\n\n")
    myDrone.updateSegment(instr3, -0.5, -0.5, 1)
    
    #When we are all set, we can start the crazyflie.
    #It will takeoff then follow every instruction in order
    myDrone.go()

if __name__ == '__main__':
    main()
