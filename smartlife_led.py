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

def rainbow(speed=0.1, brightness=800, step=10):
    """
    Animate a rainbow cycle across your LED strip.
    speed: delay between steps (seconds)
    brightness: 0-1000
    step: hue increment per iteration (smaller = smoother)
    """
    turn_on()
    set_brightness(brightness)
    print(f"Starting rainbow animation with speed {speed}s per step...")

    try:
        while True:  # infinite loop until Ctrl+C
            for h in range(0, 360, step):
                set_hsv(h, s=1000, v=brightness)
                time.sleep(speed)
    except KeyboardInterrupt:
        print("\nRainbow animation stopped.")


# ---------------- LED CONTROL FUNCTIONS ----------------
def turn_on():
    response = openapi.post(
        f"/v1.0/devices/{DEVICE_ID}/commands",
        {"commands": [{"code": "switch_led", "value": True}]}
    )
    print("Turn ON response:", response)

def turn_off():
    response = openapi.post(
        f"/v1.0/devices/{DEVICE_ID}/commands",
        {"commands": [{"code": "switch_led", "value": False}]}
    )
    print("Turn OFF response:", response)

def set_brightness(value):
    """value: 10 - 1000"""
    response = openapi.post(
        f"/v1.0/devices/{DEVICE_ID}/commands",
        {"commands": [{"code": "bright_value", "value": value}]}
    )
    print(f"Set brightness to {value} response:", response)

def set_scene(scene_number):
    """Set preset scene by number"""
    response = openapi.post(
        f"/v1.0/devices/{DEVICE_ID}/commands",
        {"commands": [{"code": "scene_num_data", "value": scene_number}]}
    )
    print(f"Set scene number {scene_number} response:", response)

def animate()
    print(f"Starting animation: speed={speed}, brightness={brightness}, step={step}")
        try:
            while True:
                for h in range(0,360,steps):
                    set_hsv(h, s=1000, v=brightness)
                    time.sleep(speed)
        except KeyboardInterrupt
        print("/nAnimation Stoped")

def usage():
    print("Usage: python3 smartlife_led.py <command> [args]")


def set_hsv(h, s=1000, v=1000):
    """
    Set custom color using HSV
    h: 0-359 (hue)
    s: 0-1000 (saturation)
    v: 0-1000 (brightness)
    """
    payload = { 
        "commands": [
            {"code": "work_mode", "value": "colour"},
            {"code": "colour_data", "value": f'{{"h":{h},"s":{s},"v":{v}}}'}
        ]
    }
    response = openapi.post(
        f"/v1.0/devices/{DEVICE_ID}/commands",
        payload
    )
    print(f"Sent HSV: h={h}, s={s}, v={v}")
    print("Response:", response)


# ---------------- COMMAND-LINE INTERFACE ----------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 smartlife_led.py <command> [args]")
        print("Commands:")
        print("  on                  Turn LED on")
        print("  off                 Turn LED off")
        print("  brightness <value>  Set brightness 10-1000")
        print("  scene <number>      Set preset scene")
        print("  color <hue> [s] [v]  Set custom HSV color")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    match cmd:
        case "on":
            turn_on()

        case "off":
            turn_off()

        case "brightness":
            if len(sys.argv) < 1:
                sys.exit(1)
            set_brightness(int(sys.argv[2]))

        case "scene":
            if len(sys.argv) < 1:
                print("Please provide scene number")
                sys.exit(1)
            set_scene(int(sys.argv[2]))

        case "color":
            if len(sys.argv) < 1:
                print("Please provide hue (0-359)")
                sys.exit(1)
                h = int(argv[0])
                s = int(argv[1]) if len(sys.argv) >= 4 else 1000
                v = int(argv[2]) if len(sys.argv) >= 5 else 1000
            set_hsv(h, s, v)

        case "rainbow":
            speed = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
            rainbow(speed)

        case "animate":
            speed = float(args[0]) if len(args) > 0 else 0.1
            brightness = int(args[1]) if len(args) > 1 else 800
            step = int(args[2]) if len(args) > 2 else 5
            animate(speed, brightness, step)
            
        case _:
            print(f"Unkown command: {cmd}")
            usage()
