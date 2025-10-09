import asyncio
import csv
import time
import atexit
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3
from pynput import keyboard
from belief import SensorFusion

# ----------------------------
# Robot Initialization
# ----------------------------
robot = Create3(Bluetooth())

# ----------------------------
# Sensor Fusion Initialization
# ----------------------------
sf = SensorFusion(cpt_dir="CPTs")

# ----------------------------
# CSV Logging setup
# ----------------------------
CSV_FILENAME = "real_time_belief_log.csv"
csv_file = open(CSV_FILENAME, "w", newline="")
csv_writer = csv.writer(csv_file)

headers = ["timestamp", "command", "left_speed", "right_speed"] + \
          [f"IR{i+1}" for i in range(7)] + \
          ["Wall", "Door_Start", "Door", "Door_Passed"]

csv_writer.writerow(headers)
csv_file.flush()

def cleanup():
    csv_file.close()
    print("✅ Data collection completed. CSV closed:", CSV_FILENAME)

atexit.register(cleanup)

# ----------------------------
# Global state
# ----------------------------
left_speed = 0
right_speed = 0
current_cmd = "Stop"
start_time = time.time()

# ----------------------------
# Keyboard control
# ----------------------------
def on_press(key):
    global left_speed, right_speed, current_cmd
    try:
        if key.char == 'w':
            left_speed, right_speed = 10, 10
            current_cmd = "Forward"
        elif key.char == 's':
            left_speed, right_speed = -10, -10
            current_cmd = "Backward"
        elif key.char == 'a':
            left_speed, right_speed = -5, 5
            current_cmd = "Left"
        elif key.char == 'd':
            left_speed, right_speed = 5, -5
            current_cmd = "Right"
        elif key.char == ' ':
            left_speed, right_speed = 0, 0
            current_cmd = "Stop"
    except AttributeError:
        pass

keyboard.Listener(on_press=on_press).start()

# ----------------------------
# Control + Logging Loop
# ----------------------------
@event(robot.when_play)
async def play(robot_event):
    print("🤖 Manual control (WASD + SPACE)")
    print("🟢 Logging sensor readings + live belief maps every 0.1s...\n")

    global left_speed, right_speed, current_cmd

    while True:
        await asyncio.sleep(0.1)

        # Set wheel speeds
        await robot.set_wheel_speeds(left_speed, right_speed)

        # Read IR sensors
        ir_data = await robot.get_ir_proximity()
        ir_values = [s for s in ir_data.sensors] if ir_data and ir_data.sensors else [0]*7

        # Compute belief map
        ir_dict = {f"IR{i+1}": val for i, val in enumerate(ir_values)}
        posterior = sf.belief(ir_dict)

        # Log everything
        timestamp = round(time.time() - start_time, 2)
        row = [timestamp, current_cmd, left_speed, right_speed] + \
              ir_values + \
              [posterior.get(label, 0) for label in ["Wall","Door_Start","Door","Door_Passed"]]
        csv_writer.writerow(row)
        csv_file.flush()

        # Debug print
        print(f"[{timestamp:.2f}s] Cmd={current_cmd} | IR={ir_values} | Belief={posterior}")

# ----------------------------
# Run
# ----------------------------
robot.play()
