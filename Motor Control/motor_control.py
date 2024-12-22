import can
import time
from mit_motor_interface import MITMotorInterface

class MotorControl:
    def __init__(self):
        self.bus0 = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=800000)
        self.bus1 = can.interface.Bus(channel='can1', bustype='socketcan', bitrate=800000)
        self.motors = {}

    def initialize_motor(self, can_bus_number, can_id):
        bus = self.bus0 if can_bus_number == 0 else self.bus1
        motor = MITMotorInterface(can_id, bus)
        self.motors[can_id] = motor
        motor.init_motor()
        return motor

    def send_motor_command(self, can_id, position, speed, torque, kp, kd):
        if can_id not in self.motors:
            print(f"Motor with CAN ID {can_id} not initialized")
            return
        
        motor = self.motors[can_id]
        motor.send_motor_cmd(position, speed, torque, kp, kd)

    def read_motor_feedback(self, can_id):
        if can_id not in self.motors:
            print(f"Motor with CAN ID {can_id} not initialized")
            return None
        
        motor = self.motors[can_id]
        motor.read_motor_feedback()
        return {
            "position": motor.get_cur_position(),
            "speed": motor.get_cur_speed(),
            "torque": motor.cur_torque
        }

def control_motor(can_bus_number, can_id, position, speed, torque, kp, kd):
    motor_control = MotorControl()
    motor = motor_control.initialize_motor(can_bus_number, can_id)
    motor_control.send_motor_command(can_id, position, speed, torque, kp, kd)
    return motor_control, can_id

def read_feedback(motor_control, can_id):
    feedback = motor_control.read_motor_feedback(can_id)
    if feedback:
        print(f"Motor {can_id} - Pos: {feedback['position']:.2f}°, "
              f"Speed: {feedback['speed']:.2f}°/s, Torque: {feedback['torque']:.2f}")
    return feedback

# Example usage
if __name__ == "__main__":
    motor_control, can_id = control_motor(
        can_bus_number=1,
        can_id=0x02,
        position=90,
        speed=40,
        torque=0,
        kp=1,
        kd=0.5
    )
