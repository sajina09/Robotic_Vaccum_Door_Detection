import asyncio
import csv
import time
import atexit
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3
from pynput import keyboard

# ----------------------------
# Robot Initialization
# ----------------------------
robot = Create3(Bluetooth("00:16:A4:64:D9:C6"))

# ----------------------------
# CSV Logging setup
# ----------------------------
CSV_FILENAME = "robot_sensor_data_labeled.csv"
csv_file = open(CSV_FILENAME, "w", newline="")
csv_writer = csv.writer(csv_file)

headers = ["timestamp", "command", "left_speed", "right_speed",
           "Location"] + [f"IR{i+1}" for i in range(7)] + ["BumpLeft", "BumpRight"]

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
current_label = "Wall"  # default label
start_time = time.time()

# ----------------------------
# Keyboard control
# ----------------------------
def on_press(key):
    global left_speed, right_speed, current_cmd, current_label
    try:
        # Movement keys
        if key.char == 'w':   # forward
            left_speed, right_speed = 10, 10
            current_cmd = "Forward"
        elif key.char == 's': # backward
            left_speed, right_speed = -10, -10
            current_cmd = "Backward"
        elif key.char == 'a': # left turn
            left_speed, right_speed = -5, 5
            current_cmd = "Left"
        elif key.char == 'd': # right turn
            left_speed, right_speed = 5, -5
            current_cmd = "Right"
        elif key.char == ' ': # stop
            left_speed, right_speed = 0, 0
            current_cmd = "Stop"

        # Manual labeling keys
        elif key.char == '1':
            current_label = "Wall"
            print("🟢 Label updated → Wall")
        elif key.char == '2':
            current_label = "Door_Start"
            print("🟡 Label updated → Door_Start")
        elif key.char == '3':
            current_label = "Door"
            print("🟠 Label updated → Door")
        elif key.char == '4':
            current_label = "Door_Passed"
            print("🔵 Label updated → Door_Passed")

    except AttributeError:
        pass

keyboard.Listener(on_press=on_press).start()

# ----------------------------
# Control + Logging Loop
# ----------------------------
@event(robot.when_play)
async def play(robot_event):
    print("🤖 Manual control (WASD + SPACE) | Label with keys [1–4]:")
    print("    1=Wall, 2=Door_Start, 3=Door, 4=Door_Passed")
    print("🟢 Data is being logged automatically every 0.1s...\n")

    global left_speed, right_speed, current_cmd, current_label

    while True:
        await asyncio.sleep(0.1)

        # Set wheel speeds
        await robot.set_wheel_speeds(left_speed, right_speed)

        # Read IR + bump sensors
        ir_data = await robot.get_ir_proximity()
        bump_data = await robot.get_bumpers()

        if ir_data and ir_data.sensors:
            ir_values = [s for s in ir_data.sensors]
        else:
            ir_values = [None] * 7

        if bump_data:
            bump_left, bump_right = bump_data
        else:
            bump_left, bump_right = False, False

        # Log data
        timestamp = round(time.time() - start_time, 2)
        row = [timestamp, current_cmd, left_speed, right_speed,
               current_label] + ir_values + [bump_left, bump_right]
        csv_writer.writerow(row)
        csv_file.flush()

        # Debug print
        print(f"[{timestamp:.2f}] {current_cmd} ({current_label}) | "
              f"Speeds=({left_speed},{right_speed}) | "
              f"IR={ir_values} | Bump(L={bump_left},R={bump_right})")

# ----------------------------
# Run
# ----------------------------
robot.play()
