import logging
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

URI = ''
logging.basicConfig(level=logging.ERROR) 


if __name__ == '__main__':

   cflib.crtp.init_drivers(enable_debug_driver=False)
   with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
      with MotionCommander(scf) as mc:
         time.sleep(3)
         mc.turn_left(0)
         mc.forward(0.5, velocity = 0.8)
         time.sleep(1)
         mc.stop()
         print('Work completed !')
