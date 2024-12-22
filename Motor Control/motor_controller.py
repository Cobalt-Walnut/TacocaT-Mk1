import can
import time
from mit_motor_interface import MITMotorInterface

# Configure the CAN buses
bus0 = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=1000000)
bus1 = can.interface.Bus(channel='can1', bustype='socketcan', bitrate=1000000)

def send_motor_cmd_can0(can_id, pos, vel, kp, kd, torque):
    motor = MITMotorInterface(can_id, bus0)
    motor.send_motor_cmd(pos, vel, torque, kp, kd)
    print(f"Command sent to Motor {can_id} on CAN0")
    time.sleep(0.1)  # Small delay to allow for motor response
    motor.read_motor_feedback()

def send_motor_cmd_can1(can_id, pos, vel, kp, kd, torque):
    motor = MITMotorInterface(can_id, bus1)
    motor.send_motor_cmd(pos, vel, torque, kp, kd)
    print(f"Command sent to Motor {can_id} on CAN1")
    time.sleep(0.1)  # Small delay to allow for motor response
    motor.read_motor_feedback()

def start_motor0(can_id):
	motor = MITMotorInterface(can_id, bus0)
	motor.init_motor()

def start_motor1(can_id):
	motor = MITMotorInterface(can_id, bus1)
	motor.init_motor()

def stop_motor0(can_id):
	motor = MITMotorInterface(can_id, bus0)
	motor.disable_motor_mode()

def stop_motor1(can_id):
	motor = MITMotorInterface(can_id, bus1)
	motor.disable_motor_mode()

def gohome0(can_id):
	motor = MITMotorInterface(can_id, bus0)
	motor.go_home()

def gohome1(can_id):
	motor = MITMotorInterface(can_id, bus1)
	motor.go_home()
# The rest of your MotorControlGUI class and main function can remain the same
'''
# Example usage of the new functions
if __name__ == "__main__":
    # To use the GUI
    # main()

    # To use the functions directly
    send_motor_cmd_can0(0x01, 90.0, 0.0, 1.0, 0.1, 0.0)  # Example command for motor on CAN0
    send_motor_cmd_can1(0x02, 45.0, 0.0, 1.0, 0.1, 0.0)  # Example command for motor on CAN1
'''
