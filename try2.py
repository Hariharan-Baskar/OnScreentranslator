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

#global flag to turn on/off
RUNNING = False;

# Set up translator
translator = Translator()

# OCR language
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  



def get_word_under_mouse():
    # Capture full screen
    screen = np.array(ImageGrab.grab())
    screen_rgb = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

    # Get mouse position
    mouse_x, mouse_y = pyautogui.position()

    # Use pytesseract to get word boxes
    data = pytesseract.image_to_data(screen_rgb, output_type=pytesseract.Output.DICT, lang='chi_sim')

    for i in range(len(data['text'])):
        word = data['text'][i]
        if word.strip() == "":
            continue
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

        if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
            return word  # Found the word under mouse

    return None  # No word under cursor

# def get_word_under_mouse():
#     # Get current mouse position
#     x, y = pyautogui.position()

#     # Define a horizontal slice (wide and short)
#     region = (x - 150, y - 15, x + 150, y + 15)
#     img = ImageGrab.grab(bbox=region)

#     # OCR with Chinese + English support
#     text_line = pytesseract.image_to_string(img, lang='chi_sim').strip()

#     return text_line if text_line else None

# Create tkinter overlay window
class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.7)
        self.label = tk.Label(self.root, text="", font=("Arial", 12), bg="yellow")
        self.label.pack()

    def show_text(self, text, x, y):
        self.label.config(text=text)
        self.root.geometry(f"+{x}+{y}")
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()

overlay = Overlay()

def live_translate():
    global RUNNING
    while True:
        # if RUNNING:
        try:
            x, y = pyautogui.position()
            # Capture region under cursor
            region = (x - 100, y - 20, x + 100, y + 20)
            img = ImageGrab.grab(bbox=region)
            # text = pytesseract.image_to_string(img).strip()
            text = get_word_under_mouse()

            if text:
                translated = translator.translate(text, src='auto', dest='en').text
                overlay.show_text(translated, x + 20, y + 20)
            else:
                overlay.hide()
        except Exception as e:
            print(f"Error: {e}")
            overlay.hide()

        # else:
        #     overlay.hide()
        
        time.sleep(0.5)

# def TempOffButton():
#     global RUNNING
#     print("Press 1 to START, 2 to STOP")

#     while True:
#         if keyboard.is_pressed('1') and not RUNNING:
#             print("Started")
#             RUNNING = True
#             time.sleep(0.05)  # debounce
#         elif keyboard.is_pressed('2') and RUNNING:
#             print("Stopped")
#             RUNNING = False
#             overlay.hide()
#             time.sleep(0.05)  # debounce


# Run in a background thread so the Tkinter loop can run
threading.Thread(target=live_translate, daemon=True).start()
# threading.Thread(target=TempOffButton, daemon=True).start()

#MAIN LOOP

overlay.root.mainloop()

