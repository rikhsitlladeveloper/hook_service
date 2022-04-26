#!/usr/bin/env python3
from operator import imod
import rospy
from geometry_msgs.msg import Twist
from rospy.core import rospyerr, rospywarn
import math
import time
from hook_service.srv import Hook_status
from ethernet_remote_io_module.msg import WriteCoil, WriteCoils, ReadDigitalInputs
from docking_msgs.msg import DockingResult
class HookServer:
    def __init__(self):
        self.digital_input = rospy.Subscriber("/camel_amr_1000_001/common/read_digital_inputs", ReadDigitalInputs)
        self.digital_output = rospy.Publisher("/camel_amr_1000_001/common/write_coil", WriteCoil, queue_size=10)
        self._as = rospy.Service('Hook_server', Hook_status, handler=self.on_goal)
        self.rate = rospy.Rate(10)    
        self.result = DockingResult()
    
    
    def read(data):
        digital_input = rospy.Subscriber("/camel_amr_1000_001/common/read_digital_inputs", ReadDigitalInputs)
        
        self.din_1 = digital_input.din_1
        self.din_2 = digital_input.din_2
        self.din_3 = digital_input.din_3
        self.din_4 = digital_input.din_4
        
    def on_goal(self, goal):
        self.hook = goal.hook
        if(self.hook == True):
            print("Hooking up is starting")
            while(self.digital_input.din_1 == False):
                address =0
                value= True
                self.digital_output.publish(address,value)    
            address =0
            value= False
            self.digital_output.publish(address,value)    
            
            self.result.result = "Hooked up"
        else:
            print("Hooking down is starting")
            while(self.din_2 == False):
                address =0
                value= True
                self.digital_output.publish(address,value)    
            address =0
            value= False
            self.digital_output.publish(address,value)    
            
            self.result.result = "Hooked down"

        
        return self.result.result   
if __name__ == '__main__':
    rospy.init_node('Hook_service')

    server = HookServer()

    rospy.spin()
