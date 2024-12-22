import tkinter as tk
from tkinter import ttk
import can
import time
from mit_motor_interface import MITMotorInterface

class MotorControlGUI:
    def __init__(self, master):
        self.master = master
        master.title("Motor Control Interface")
        
        self.entries = {}
        self.feedback_labels = {}
        self.can_id_entries = {}
        
        can_interface = 'can0'
        self.bus0 = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=1000000)
        self.bus1 = can.interface.Bus(channel='can1', bustype='socketcan', bitrate=1000000)
        
        self.motor1 = MITMotorInterface(0x02, self.bus1)
        self.motor2 = MITMotorInterface(0x02, self.bus0)

        self.create_widgets()

    def create_widgets(self):
        self.frame1 = ttk.LabelFrame(self.master, text="Motor 1")
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.create_motor_controls(self.frame1, self.motor1, 1)

        self.frame2 = ttk.LabelFrame(self.master, text="Motor 2")
        self.frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.create_motor_controls(self.frame2, self.motor2, 2)

    def create_motor_controls(self, frame, motor, motor_num):
        enable_button = ttk.Button(frame, text="Enable Motor Mode", command=lambda: self.enable_motor_mode(motor, motor_num))
        enable_button.grid(row=0, column=0, padx=5, pady=5)
        
        disable_button = ttk.Button(frame, text="Disable Motor Mode", command=lambda: self.disable_motor_mode(motor, motor_num))
        disable_button.grid(row=0, column=1, padx=5, pady=5)

        labels = ["Position", "Speed", "Torque", "Kp", "Kd"]
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(frame, width=10)
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            self.entries[f"{label.lower()}{motor_num}"] = entry

        ttk.Button(frame, text="Send Command", command=lambda: self.send_motor_cmd(motor, motor_num)).grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

        self.feedback_labels[motor_num] = ttk.Label(frame, text="Feedback: ")
        self.feedback_labels[motor_num].grid(row=len(labels)+2, column=0, columnspan=2, pady=5)

        ttk.Label(frame, text="CAN ID:").grid(row=len(labels)+3, column=0, padx=5, pady=5, sticky="e")
        can_id_entry = ttk.Entry(frame, width=10)
        can_id_entry.grid(row=len(labels)+3, column=1, padx=5, pady=5)
        can_id_entry.insert(0, f"{motor.node_id:02X}")  # Set initial value
        self.can_id_entries[motor_num] = can_id_entry
        ttk.Button(frame, text="Update CAN ID", command=lambda: self.update_can_id(motor, motor_num, enable_button, disable_button)).grid(row=len(labels)+4, column=0, columnspan=2, pady=5)

    def enable_motor_mode(self, motor, motor_num):
        motor.enable_motor_mode()
        print(f"Motor {motor_num} mode enabled (CAN ID: 0x{motor.node_id:02X})")

    def disable_motor_mode(self, motor, motor_num):
        motor.disable_motor_mode()
        print(f"Motor {motor_num} mode disabled (CAN ID: 0x{motor.node_id:02X})")

    def send_motor_cmd(self, motor, motor_num):
        try:
            pos = float(self.entries[f"position{motor_num}"].get())
            speed = float(self.entries[f"speed{motor_num}"].get())
            torque = float(self.entries[f"torque{motor_num}"].get())
            kp = float(self.entries[f"kp{motor_num}"].get())
            kd = float(self.entries[f"kd{motor_num}"].get())

            motor.send_motor_cmd(pos, speed, torque, kp, kd)
            print(f"Command sent to Motor {motor_num} (CAN ID: 0x{motor.node_id:02X})")
            self.read_motor_feedback(motor, motor_num)
        except ValueError:
            print("Invalid input. Please enter numeric values.")

    def read_motor_feedback(self, motor, motor_num):
        motor.read_motor_feedback()
        feedback = f"Pos: {motor.get_cur_position():.2f}°, Speed: {motor.get_cur_speed():.2f}°/s"
        self.feedback_labels[motor_num].config(text=f"Feedback: {feedback}")

    def update_can_id(self, motor, motor_num, enable_button, disable_button):
        try:
            new_can_id = int(self.can_id_entries[motor_num].get(), 16)  # Convert hex string to int
            motor.update_can_id(new_can_id)
            print(f"CAN ID for Motor {motor_num} updated to: 0x{new_can_id:02X}")
            
            # Update enable and disable button commands
            enable_button.config(command=lambda: self.enable_motor_mode(motor, motor_num))
            disable_button.config(command=lambda: self.disable_motor_mode(motor, motor_num))
        except ValueError:
            print(f"Invalid CAN ID for Motor {motor_num}. Please enter a valid hexadecimal value.")

def main():
    root = tk.Tk()
    app = MotorControlGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

#Tip: If you want to go at a specific velocity, the Kd should be higher than the Kd
