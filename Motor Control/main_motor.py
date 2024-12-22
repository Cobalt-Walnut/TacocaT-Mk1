from motor_controller import send_motor_cmd_can0, send_motor_cmd_can1, start_motor0, start_motor1, stop_motor0, stop_motor1, gohome0, gohome1
import time

#Motor Control code here
#Example:
#Function(CAN_ID)
start_motor0(0x02)
send_motor_cmd_can0(0x02)
stop_motor0(0x02)
#All functions can be viewed in the 'motor_controller.py' file.
#Function format:

#def Function_name can_line(parameters):
#  stuff in the function

#Example:

#Function_name Can_line
#def start_motor0(can_id):
