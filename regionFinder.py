import pyautogui
import time

print("Move your mouse to the top-left corner of the player list and wait 3 seconds...")
time.sleep(5)
x1, y1 = pyautogui.position()
print(f"Top-left corner: {x1}, {y1}")

print("Now move your mouse to the bottom-right corner of the player list and wait 3 seconds...")
time.sleep(3)
x2, y2 = pyautogui.position()
print(f"Bottom-right corner: {x2}, {y2}")

# Calculate region
width = x2 - x1
height = y2 - y1
print(f"Screen region for OCR: ({x1}, {y1}, {width}, {height})")
