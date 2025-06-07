import pytesseract
from PIL import ImageGrab
import pyautogui
import time
import tkinter as tk
from googletrans import Translator
import threading
import time
import cv2
import numpy as np
import keyboard
import pyperclip

def screen_text_extractor():
    import cv2
    import numpy as np
    import pytesseract
    from PIL import ImageGrab

    print("Select area to extract text. Press Enter after selection.")

    # Let user select a screen region with mouse
    region = pyautogui.screenshot()
    region = cv2.cvtColor(np.array(region), cv2.COLOR_RGB2BGR)

    r = cv2.selectROI("Select Region", region, showCrosshair=True)
    cv2.destroyWindow("Select Region")

    if r == (0, 0, 0, 0):
        print("No region selected.")
        return None

    x, y, w, h = r
    # Capture selected region
    selected_region = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    selected_region_np = np.array(selected_region)

    # Convert to RGB and use pytesseract
    text = pytesseract.image_to_string(selected_region_np)
    print(text.strip())
    return text.strip()

screen_text_extractor()
