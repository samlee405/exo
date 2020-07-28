import os
import pyscreenshot
from PIL import Image
import pytesseract
import cv2
import re
import timeit


pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Sam\AppData\Local\Tesseract-OCR\tesseract.exe"
root_dir = os.path.dirname(os.path.abspath(__file__))
screen_shot_path = os.path.join(root_dir, "images", "screenshot.png")

stats = [
    "Vitality",
    "AP",
    "MP",
    "Initiative",
    "Prospecting",
    "Range",
    "Summons",
    "Wisdom",
    "Strength",
    "Intelligence",
    "Chance",
    "Agility",
    "AP Parry",
    "AP Reduction",
    "MP Parry",
    "MP Reduction",
    "Critical",
    "Heals",
    "Lock",
    "Dodge",
    "Power",
    "Damage",
    "Critical Damage",
    "Neutral Damage",
    "Earth Damage",
    "Fire Damage",
    "Water Damage",
    "Air Damage",
    "Reflect",
    "Trap Damage",
    "Power \(traps\)",
    "Pushback Damage",
    "Spell Damage",
    "Weapon Damage",
    "Ranged Damage",
    "Melee Damage",
    "Neutral Resistance",
    "Earth Resistance",
    "Fire Resistance",
    "Water Resistance",
    "Air Resistance",
    "Critical Resistance",
    "Pushback Resistance",
    "Ranged Resistance",
    "Melee Resistance",
    "pods",
]


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
        stats[stat] = value

        print((stat, value))

    return stats


def exo():
    start = timeit.default_timer()

    take_screen_shot()
    image_preprocessing()
    raw_text = get_text_from_image()
    stats = get_stats_from_text(raw_text)

    stop = timeit.default_timer()
    print('\nTime: ', stop - start)


if __name__ == "__main__":
    exo()
