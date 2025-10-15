import asyncio
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import Create3, event
from belief import belief, load_CPTs

# ===============================
# CONFIGURATION
# ===============================
BASE_SPEED = 25
TARGET_DISTANCE_CM = 6.0
TARGET_DISTANCE_AFTER_DOOR_CM = 10.0
SAMPLE_TIME = 0.1
KP = 0.8
KI = 0.02
KD = 0.1

# ===============================
# LOAD CPT
# ===============================
CPTs = load_CPTs("CPTs")

# ===============================
# PID CONTROLLER
# ===============================
class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0.0
        self.integral = 0.0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error
        return output

pid = PIDController(KP, KI, KD)

# ===============================
# Robot Initialization
# ===============================
robot = Create3(Bluetooth())

# ===============================
# IR7 to distance
# ===============================
def ir7_to_distance(ir7_value):
    if ir7_value <= 0:
        return 30.0
    return max(1.0, min(30.0, 200 / ir7_value))

# ===============================
# WALL FOLLOWING LOOP (event-driven)
# ===============================
door_passed_detected = False
distance_after_door = 0.0

@event(robot.when_play)
async def wall_following(robot_event):
    global door_passed_detected, distance_after_door
    print("Robot starting right-wall following using IR7 with PID...")

    while True:
        await asyncio.sleep(SAMPLE_TIME)  # <-- fixed, use asyncio.sleep()

        # Read IR7
        ir_data = await robot.get_ir_proximity()
        ir7 = ir_data.sensors[6] if ir_data and len(ir_data.sensors) > 6 else 0

        # Compute belief
        sensor_readings = {"IR7": ir7}
        b = belief(sensor_readings, CPTs)
        door_prob = b["Door"]
        door_passed_prob = b["Door_Passed"]

        # PID control for wall following
        current_distance = ir7_to_distance(ir7)
        error = TARGET_DISTANCE_CM - current_distance
        correction = pid.update(error, SAMPLE_TIME)

        # Right-wall following: left/right speed correction
        left_speed = BASE_SPEED + correction
        right_speed = BASE_SPEED - correction
        left_speed = max(0, min(50, left_speed))
        right_speed = max(0, min(50, right_speed))

        # Door passed logic
        if door_passed_prob > 0.8 and not door_passed_detected:
            print(f"Door passed detected! IR7={ir7}")
            door_passed_detected = True
            distance_after_door = 0.0

        if door_passed_detected:
            distance_after_door += current_distance * SAMPLE_TIME
            if distance_after_door >= TARGET_DISTANCE_AFTER_DOOR_CM:
                left_speed = 0
                right_speed = 0
                print("Stopped 10cm after passing the door.")
                await robot.set_wheel_speeds(left_speed, right_speed)
                break

        # Apply wheel speeds
        await robot.set_wheel_speeds(left_speed, right_speed)

        # Debug
        print(f"IR7={ir7} | Door={door_prob:.2f} Door_Passed={door_passed_prob:.2f} | L={left_speed:.1f} R={right_speed:.1f}")

# ===============================
# START
# ===============================
if __name__ == "__main__":
    robot.play() 