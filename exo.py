import os
import pyscreenshot
from PIL import Image
import pytesseract
import timeit

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Sam\AppData\Local\Tesseract-OCR\tesseract.exe"
root_dir = os.path.dirname(os.path.abspath(__file__))

def take_screen_shot():
    image = pyscreenshot.grab(bbox=(730, 315, 975, 900))
    image.save(os.path.join(root_dir, "images", "screenshot.png"))


def get_text_from_image():
    image_path = os.path.join(root_dir, "images", "screenshot.png")
    return pytesseract.image_to_string(Image.open(image_path))


def exo():
    start = timeit.default_timer()
    take_screen_shot()
    text = get_text_from_image()
    print(text)

    stop = timeit.default_timer()
    print('Time: ', stop - start)

if __name__ == "__main__":
    exo()
