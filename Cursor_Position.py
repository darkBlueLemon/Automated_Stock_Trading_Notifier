import pyautogui
import time

def continuously_output_cursor_coordinates():
    try:
        while True:
            x, y = pyautogui.position()
            print(f"Cursor coordinates: ({x}, {y})")
            time.sleep(0.1)  # Add a 0.5-second delay
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    continuously_output_cursor_coordinates()
