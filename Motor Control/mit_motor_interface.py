import can
import struct
import time
from utils import float_to_uint, uint_to_float, deg_to_rad, rad_to_deg

# Motor Constants
P_MIN, P_MAX = -95.5, 95.5
V_MIN, V_MAX = -45.0, 45.0
KP_MIN, KP_MAX = 0.0, 500.0
KD_MIN, KD_MAX = 0.0, 5.0
T_MIN, T_MAX = -18.0, 18.0

class MITMotorInterface:
    def __init__(self, node_id, can_bus):
        self.node_id = node_id
        self.can = can_bus
        self.cur_mot_pos = 0
        self.cur_mot_speed = 0
        self.cur_torque = 0

    def init_motor(self):
        self.disable_motor_mode()
        time.sleep(1)
        self.enable_motor_mode()
        time.sleep(1)
        self.read_motor_feedback()
    
    def update_can_id(self, new_id):
        self.node_id = new_id
    
    def enable_motor_mode(self):
        motor_mode_cmd = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC]
        msg = can.Message(arbitration_id=self.node_id, data=motor_mode_cmd, is_extended_id=False)
        try:
            self.can.send(msg)
            print("Motor Mode Enabled!")
        except can.CanError:
            print("Failed To Enter Motor Mode...")
            print(msg)

    def disable_motor_mode(self):
        motor_mode_cmd = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFD]
        msg = can.Message(arbitration_id=self.node_id, data=motor_mode_cmd, is_extended_id=False)
        try:
            self.can.send(msg)
            print("Motor Mode Disabled!")
        except can.CanError:
            print("Failed To Exit Motor Mode...")
            print(msg)

    def go_home(self):
        home_cmd = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE]
        msg = can.Message(arbitration_id=self.node_id, data=home_cmd, is_extended_id=False)
        try:
            self.can.send(msg)
            print("Home CMD Sent!")
        except can.CanError:
            print("Failed To Send Home CMD...")
            print(msg)

    def send_motor_cmd(self, pos, vel, torque, kp, kd):
    	p_int = float_to_uint(deg_to_rad(pos), P_MIN, P_MAX, 16)
    	v_int = float_to_uint(deg_to_rad(vel), V_MIN, V_MAX, 12)
    	kp_int = float_to_uint(kp, KP_MIN, KP_MAX, 12)
    	kd_int = float_to_uint(kd, KD_MIN, KD_MAX, 12)
    	t_int = float_to_uint(torque, T_MIN, T_MAX, 12)

    	data = [
        	(p_int >> 8) & 0xFF,
        	p_int & 0xFF,
        	(v_int >> 4) & 0xFF,
        	((v_int & 0xF) << 4) | ((kp_int >> 8) & 0xF),
        	kp_int & 0xFF,
        	(kd_int >> 4) & 0xFF,
        	((kd_int & 0xF) << 4) | ((t_int >> 8) & 0xF),
        	t_int & 0xFF
    	]

    	msg = can.Message(arbitration_id=self.node_id, data=data, is_extended_id=False)
    	try:
        	self.can.send(msg)
        	print(f"Motor CMD Sent: ID={self.node_id}, Data={data}")
    	except can.CanError:
        	print("Failed To Send Motor CMD...")
    def read_motor_feedback(self):
        msg = self.can.recv(timeout=1.0)
        if msg is None or len(msg.data) != 6:
            return

        p_int = (msg.data[1] << 8) | msg.data[2]
        v_int = (msg.data[3] << 4) | (msg.data[4] >> 4)
        t_int = ((msg.data[4] & 0x0F) << 8) | msg.data[5]

        self.cur_mot_pos = uint_to_float(p_int, P_MIN, P_MAX, 16)
        self.cur_mot_speed = uint_to_float(v_int, V_MIN, V_MAX, 12)
        self.cur_torque = uint_to_float(t_int, T_MIN, T_MAX, 12)

        print(f"CAN ID: {msg.data[0]} p: {rad_to_deg(self.cur_mot_pos):.2f} [deg] "
              f"v: {rad_to_deg(self.cur_mot_speed):.2f} [deg/s] t: {self.cur_torque:.2f}")

    def get_cur_position(self):
        return rad_to_deg(self.cur_mot_pos)

    def get_cur_speed(self):
        return rad_to_deg(self.cur_mot_speed)
