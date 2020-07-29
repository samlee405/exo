import os
import pyscreenshot
from PIL import Image
import pytesseract
import cv2
import pyautogui
from pynput import keyboard
import json
import time
import threading
from playsound import playsound
import random


pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Sam\AppData\Local\Tesseract-OCR\tesseract.exe"
root_dir = os.path.dirname(os.path.abspath(__file__))
screen_shot_path = os.path.join(root_dir, "images", "screenshot.png")

items = [
    "warGauntlet"
]

should_stop_maging = False
is_running = False


def take_screen_shot():
    image = pyscreenshot.grab(bbox=(730, 315, 975, 900))
    image.save(screen_shot_path)


def image_preprocessing():
    image = cv2.imread(screen_shot_path)

    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC) # increase image size
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # image to grayscale
    image = cv2.bitwise_not(image) # invert colors (lighter backgrounds seem to lead to better results)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] # increase contrast

    cv2.imwrite(screen_shot_path, image)


def get_text_from_image():
    return pytesseract.image_to_string(Image.open(screen_shot_path))


def get_stats_from_text(raw_text):
    text_list = raw_text.split("\n")
    stats = {}

    for text in text_list:
        text = text.strip()
        if text == "":
            continue

        split_text = text.split(" ")
        value = split_text[0]
        del split_text[0]
        stat = " ".join(split_text)
        if "%" in value:
            value = value.replace("%", "")
            stat = "% " + stat
        stats[stat] = int(value)

    return stats


def mage(stats, item):
    with open("items.json", "r") as file:
        data = json.load(file)
        item_data = data[item]

        is_done = True

        for stat_data in item_data["stats"]:
            stat = stat_data["stat"]
            if stats[stat] <= stat_data["threshold"]:
                pyautogui.moveTo(stat_data["position"]["x"], stat_data["position"]["y"], 0.1)
                pyautogui.doubleClick()
                pyautogui.moveTo(1010, 240, 0.2)
                pyautogui.dragTo(1010, 240, button = 'left')
                pyautogui.click(1010, 240)
                is_done = False
                break

        return is_done


def run_maging_script(item):
    global should_stop_maging
    global is_running
    is_done = False
    while not is_done and not should_stop_maging:
        take_screen_shot()
        image_preprocessing()
        raw_text = get_text_from_image()
        stats = get_stats_from_text(raw_text)
        is_done = mage(stats, item)

        time.sleep(0.5)

    if is_done:
        should_stop_maging = True
        is_running = False
        sounds = [f for f in os.listdir(os.path.join(root_dir, "sounds"))]
        file_path = os.path.join(root_dir, "sounds", sounds[random.randint(0, len(sounds) - 1)])
        playsound(file_path)

def main(item):
    def on_press(key):
        global should_stop_maging
        global is_running
        if key == keyboard.Key.f11 and not is_running:
            print("Starting mage")
            should_stop_maging = False
            is_running = True
            script_thread = threading.Thread(target=run_maging_script, args=(item, ))
            script_thread.start()
        elif key == keyboard.Key.f12 and is_running:
            print("Early exit detected, stopping mage")
            should_stop_maging = True
            is_running = False
        elif key == keyboard.Key.end:
            print("Stopping script")
            return False

    print("Please bring up your game window with your item ready to begin maging. "
        "When ready, press F11 to start maging. If at any time you'd like to "
        "pause execution, press F12. To exit the script altogether, press End")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main("warGauntlet")
