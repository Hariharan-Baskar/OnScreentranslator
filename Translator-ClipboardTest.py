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
import shutil

translator = Translator()
hide_timer = None

#remove the overlay after a timer
def hide_overlay_after_delay(delay):
    global hide_timer

    # Cancel previous timer if running
    if hide_timer and hide_timer.is_alive():
        return

    def timer():
        time.sleep(delay)
        overlay.withdraw()  # Hide window

    #start overlay hider thread
    threading.Thread(target=timer, daemon=True).start()

#translate and set overlay text
def update_overlay():
    last_text = ""
    while True:
        #this "current text" is the word that is translated so if made a different method 
        #to scan the text, assign the output to this.
        #(currently: textextractor from windows powertoys)  
        current_text = translator.translate(pyperclip.paste(), src='auto', dest='en').text
        if current_text != last_text and current_text.strip():
            label.config(text=current_text)

            overlay.update_idletasks()

            # Get required width and height for label
            width = label.winfo_reqwidth()
            height = label.winfo_reqheight()

            screen_width = overlay.winfo_screenwidth()
            screen_height = overlay.winfo_screenheight()

            # Position it at the bottom center
            x = (screen_width - width) // 2
            y = screen_height - height - 40
            overlay.geometry(f"{width}x{height}+{x}+{y}")

            overlay.deiconify() #show overlay
            last_text = current_text
            hide_overlay_after_delay(15) #call delay function to close overlay
        time.sleep(0.5)

# Create overlay window
overlay = tk.Tk()
overlay.overrideredirect(True)  # No title bar
overlay.attributes('-topmost', True)
overlay.attributes('-alpha', 0.8)  # Transparency

# # Set overlay size and position (bottom center)
# screen_width = overlay.winfo_screenwidth()
# screen_height = overlay.winfo_screenheight()
# width = 600
# height = 40

# x = (screen_width - width) // 2
# y = screen_height - height - 80  # 40px above taskbar
# overlay.geometry(f"{width}x{height}+{x}+{y}")


# Label to show clipboard text
label = tk.Label(overlay, text="", font=("Arial", 14), bg="black", fg="white")
label.pack(expand=True, fill='both')

print("This program simply translates the last entry in your clipboard into English \n " \
    "This was intended to use alongside windows PowerToys-Text Extractor\n\n"
    )

TStext = "-----TRANSLATION STARTED-----"
columns = shutil.get_terminal_size().columns
print(TStext.center(columns))

# Start clipboard monitoring in background
threading.Thread(target=update_overlay, daemon=True).start()

# Start Tkinter loop
overlay.mainloop()

# translator = Translator()
# text = pyperclip.paste()
# translated = translator.translate(text, src='auto', dest='en').text
# print(translated)



