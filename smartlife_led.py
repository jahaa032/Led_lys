#!/usr/bin/env python3
import sys
import time
from tuya_connector import TuyaOpenAPI

# ----------------- FILL THESE IN -----------------
API_ENDPOINT = "https://openapi.tuyaeu.com"
ACCESS_ID = "8x4j4qpcjc98eyrk9ck5"
ACCESS_KEY = "3f09f59a926e432e9ea8beaba77dcd55"
DEVICE_ID = "bf2d27231845a17a52pkuh"
# -------------------------------------------------

# Connect to Tuya Cloud
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# ---------------- LED CONTROL FUNCTIONS ----------------

def turn_on():
    openapi.post(
        f"/v1.0/devices/{DEVICE_ID}/commands",
        {"commands": [{"code": "switch_led", "value": True}]}
    )
    print("LED turned ON")

def turn_off():
    openapi.post(
        f"/v1.0/devices/{DEVICE_ID}/commands",
        {"commands": [{"code": "switch_led", "value": False}]}
    )
    print("LED turned OFF")

def set_brightness(value: int):
    openapi.post(
        f"/v1.0/devices/{DEVICE_ID}/commands",
        {"commands": [{"code": "bright_value", "value": value}]}
    )
    print(f"Brightness set to {value}")

def set_scene(scene: int):
    openapi.post(
        f"/v1.0/devices/{DEVICE_ID}/commands",
        {"commands": [{"code": "scene_num_data", "value": scene}]}
    )
    print(f"Scene set to {scene}")

def set_hsv(h: int, s: int = 1000, v: int = 1000):
    payload = {
        "commands": [
            {"code": "work_mode", "value": "colour"},
            {"code": "colour_data", "value": f'{{"h":{h},"s":{s},"v":{v}}}'}
        ]
    }
    openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", payload)
    print(f"HSV set → h={h}, s={s}, v={v}")

# ---------------- ANIMATIONS ----------------

def rainbow(speed=0.1, brightness=800, step=10):
    turn_on()
    set_brightness(brightness)
    print("Starting rainbow animation (Ctrl+C to stop)")
    try:
        while True:
            for h in range(0, 360, step):
                set_hsv(h, 1000, brightness)
                time.sleep(speed)
    except KeyboardInterrupt:
        print("\nRainbow stopped")

def animate(speed=0.1, brightness=800, step=5):
    turn_on()
    set_brightness(brightness)
    print("Starting animation (Ctrl+C to stop)")
    try:
        while True:
            for h in range(0, 360, step):
                set_hsv(h, 1000, brightness)
                time.sleep(speed)
    except KeyboardInterrupt:
        print("\nAnimation stopped")

# ---------------- HELP ----------------

def usage():
    print("""
Usage: python3 smartlife_led.py <command> [args]

Commands:
  on
  off
  brightness <value>
  scene <number>
  color <hue> [s] [v]
  rainbow [speed]
  animate [speed] [brightness] [step]
""")

# ---------------- CLI ----------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    match cmd:
        case "on":
            turn_on()

        case "off":
            turn_off()

        case "brightness":
            if not args:
                print("Missing brightness value")
                sys.exit(1)
            set_brightness(int(args[0]))

        case "scene":
            if not args:
                print("Missing scene number")
                sys.exit(1)
            set_scene(int(args[0]))

        case "color":
            if not args:
                print("Missing hue")
                sys.exit(1)
            h = int(args[0])
            s = int(args[1]) if len(args) > 1 else 1000
            v = int(args[2]) if len(args) > 2 else 1000
            set_hsv(h, s, v)

        case "rainbow":
            speed = float(args[0]) if args else 0.1
            rainbow(speed)

        case "animate":
            speed = float(args[0]) if len(args) > 0 else 0.1
            brightness = int(args[1]) if len(args) > 1 else 800
            step = int(args[2]) if len(args) > 2 else 5
            animate(speed, brightness, step)

        case _:
            print(f"Unknown command: {cmd}")
            usage()