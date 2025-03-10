import pytesseract
import pyautogui
import time
import sys
from PIL import ImageGrab, Image, ImageEnhance

# Configure pytesseract path (only needed on Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define screen regions for both columns
LEFT_COLUMN_REGION = (657, 325, 300, 479)
RIGHT_COLUMN_REGION = (961, 333, 303, 470)

def find_player_and_act(target_player, action):
    print(action + " " + target_player)

    def search_column(region):
        screenshot = pyautogui.screenshot(region=region)
        text_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

        for i, text in enumerate(text_data['text']):
            if target_player.lower() in text.lower():
                x, y, w, h = text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i]

                pyautogui.moveTo(region[0] + x + w // 2, region[1] + y + h // 2)

                pyautogui.mouseDown(button='right')
                time.sleep(0.1)
                pyautogui.mouseUp(button='right')
                cursor_x, cursor_y = pyautogui.position()

                menu_region = (
                    max(0, cursor_x - 1),
                    max(0, cursor_y - 1),
                    min(cursor_x + 135, pyautogui.size()[0]),
                    min(cursor_y + 250, pyautogui.size()[1])
                )

                pyautogui.moveRel(-50, 0)

                if action.lower() == 'kick':
                    if select_menu_option("Profile", menu_region):
                        print(f"{target_player} has been kicked.")
                        return True
                elif action.lower() == 'ban':
                    if select_menu_option("Profile", menu_region):
                        print(f"{target_player} has been banned.")
                        return True

        return False

    scroll_attempts = 0
    max_scrolls = 5

    while scroll_attempts < max_scrolls:
        if search_column(LEFT_COLUMN_REGION) or search_column(RIGHT_COLUMN_REGION):
            return True

        # Scroll both columns if not found
        pyautogui.moveTo(
            LEFT_COLUMN_REGION[0] + LEFT_COLUMN_REGION[2] // 2,
            LEFT_COLUMN_REGION[1] + LEFT_COLUMN_REGION[3] // 2
        )
        pyautogui.scroll(-500)
        time.sleep(0.5)
        pyautogui.moveTo(
            RIGHT_COLUMN_REGION[0] + RIGHT_COLUMN_REGION[2] // 2,
            RIGHT_COLUMN_REGION[1] + RIGHT_COLUMN_REGION[3] // 2
        )
        pyautogui.scroll(-500)
        scroll_attempts += 1

    print(f"Player '{target_player}' not found after {scroll_attempts} scroll attempts.")
    return False

def select_menu_option(option_text, menu_region):
    menu_screenshot = ImageGrab.grab(bbox=menu_region).convert('L')
    enhancer = ImageEnhance.Contrast(menu_screenshot)
    menu_screenshot = enhancer.enhance(2.0)
    menu_screenshot.save("menu_debug.png")

    text_data = pytesseract.image_to_data(menu_screenshot, config='--psm 6', output_type=pytesseract.Output.DICT)

    for i, text in enumerate(text_data['text']):
        if option_text.lower() in text.lower():
            menu_x = menu_region[0] + text_data['left'][i] + text_data['width'][i] // 2
            menu_y = menu_region[1] + text_data['top'][i] + text_data['height'][i] // 2

            pyautogui.moveTo(menu_x, menu_y)
            pyautogui.mouseDown(button='left')
            time.sleep(0.1)
            pyautogui.mouseUp(button='left')
            print(f"Selected menu option: {option_text}")
            return True

    print(f"Menu option '{option_text}' not found.")
    return False

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Error: Missing arguments.")
        sys.exit(1)

    if sys.argv[1] == "admin" and sys.argv[2] == "start":
        pyautogui.moveTo(961, 966)
        pyautogui.mouseDown(button='left')
        time.sleep(0.2)
        pyautogui.mouseUp(button='left')
        time.sleep(1)

        pyautogui.moveTo(1655, 873)
        pyautogui.mouseDown(button='left')
        time.sleep(0.2)
        pyautogui.mouseUp(button='left')

        time.sleep(1)

        pyautogui.mouseDown(button='left')
        time.sleep(0.1)
        pyautogui.mouseUp(button='left')

        time.sleep(30)

        pyautogui.moveTo(229, 1038)
        pyautogui.mouseDown(button='left')
        time.sleep(0.2)
        pyautogui.mouseUp(button='left')

        print("SUCCESS")
        sys.exit(1)

    target_player = sys.argv[1]
    action = sys.argv[2]

    pyautogui.moveTo(
        LEFT_COLUMN_REGION[0] + LEFT_COLUMN_REGION[2] // 2,
        LEFT_COLUMN_REGION[1] + LEFT_COLUMN_REGION[3] // 2
    )
    pyautogui.scroll(1500)
    time.sleep(0.5)
    pyautogui.moveTo(
        RIGHT_COLUMN_REGION[0] + RIGHT_COLUMN_REGION[2] // 2,
        RIGHT_COLUMN_REGION[1] + RIGHT_COLUMN_REGION[3] // 2
    )
    pyautogui.scroll(1500)

    if find_player_and_act(target_player, action):
        print("SUCCESS")
    else:
        print("FAILED")

    sys.stdout.flush()
