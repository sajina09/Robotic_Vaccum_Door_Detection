
import asyncio
import csv
import atexit
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3
from pynput import keyboard

# ======================================================
# Robot Initialization
# ======================================================
robot = Create3(Bluetooth())

# ======================================================
# CSV Setup
# ======================================================
CSV_FILENAME = "robot_sensor_data.csv"
csv_file = open(CSV_FILENAME, "w", newline="")
csv_writer = csv.writer(csv_file)

# Columns: label + 3 IR sensors + bumpers
headers = ["label", "IR5", "IR6", "IR7", "BumpLeft", "BumpRight"]
csv_writer.writerow(headers)
csv_file.flush()

def cleanup():
    csv_file.close()
    print("Data collection completed. File saved:", CSV_FILENAME)

atexit.register(cleanup)

# ======================================================
# Global State
# ======================================================
left_speed = 0
right_speed = 0
current_cmd = "Stop"
current_label = "Wall"  # Default label

# ======================================================
# Keyboard Control (Movement + Labeling)
# ======================================================
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

        # Manual labeling keys (3 labels)
        elif key.char == '1':
            current_label = "Wall"
            print("Label set: Wall")
        elif key.char == '2':
            current_label = "Door"
            print("Label set: Door")
        elif key.char == '3':
            current_label = "Door_Passed"
            print("Label set: Door_Passed")

    except AttributeError:
        pass  # Handles special keys

keyboard.Listener(on_press=on_press).start()

# ======================================================
# Control Loop + Logging
# ======================================================
@event(robot.when_play)
async def play(robot_event):
    print("Manual Control (WASD + SPACE)")
    print("Set labels with keys: 1=Wall, 2=Door, 3=Door_Passed\n")
    print("Collecting IR5, IR6, IR7, and bumper data every 0.1s...")

    while True:
        await asyncio.sleep(0.1)

        # Set wheel speeds
        await robot.set_wheel_speeds(left_speed, right_speed)

        # Read IR Proximity and Bumpers
        ir_data = await robot.get_ir_proximity()
        bump_data = await robot.get_bumpers()

        # Extract sensors
        ir5 = ir_data.sensors[4] if ir_data and len(ir_data.sensors) > 4 else None
        ir6 = ir_data.sensors[5] if ir_data and len(ir_data.sensors) > 5 else None
        ir7 = ir_data.sensors[6] if ir_data and len(ir_data.sensors) > 6 else None

        bump_left, bump_right = bump_data if bump_data else (False, False)

        # Log to CSV
        row = [current_label, ir5, ir6, ir7, bump_left, bump_right]
        csv_writer.writerow(row)
        csv_file.flush()

        # Console feedback
        print(f"Label={current_label} | IR5={ir5} IR6={ir6} IR7={ir7} | Bump(L={bump_left},R={bump_right})")

# ======================================================
# Run
# ======================================================
robot.play()
