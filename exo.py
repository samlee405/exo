import os
import pyscreenshot
from PIL import Image
import pytesseract
import cv2
import timeit

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Sam\AppData\Local\Tesseract-OCR\tesseract.exe"
root_dir = os.path.dirname(os.path.abspath(__file__))
screen_shot_path = os.path.join(root_dir, "images", "screenshot.png")

def take_screen_shot():
    image = pyscreenshot.grab(bbox=(730, 315, 975, 900))
    image.save(screen_shot_path)


def image_preprocessing():
    image = cv2.imread(screen_shot_path)

    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC) # resize
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # image to grayscale
    image = cv2.bitwise_not(image) # invert colors (lighter backgrounds seem to lead to better results)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] # increase contrast
    # image = cv2.GaussianBlur(image, (5, 5), 0) # smooth edges

    cv2.imwrite(screen_shot_path, image)


def get_text_from_image():
    return pytesseract.image_to_string(Image.open(screen_shot_path))


def get_values_from_text(raw_text):
    text = raw_text.split("\n")
    for line in text:
        print(line)


def exo():
    start = timeit.default_timer()

    take_screen_shot()
    image_preprocessing()
    raw_text = get_text_from_image()
    values = get_values_from_text(raw_text)

    stop = timeit.default_timer()
    print('Time: ', stop - start)


if __name__ == "__main__":
    exo()
