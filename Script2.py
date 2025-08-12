import tkinter as tk
import customtkinter as ctk
import random
import threading
import time
import sys
import winsound
import pyautogui
from pynput.mouse import Listener, Button
from ctypes import windll
from PIL import Image, ImageTk
import subprocess
import requests

# --- Globals ---
running = False
alive = True
right_mouse_pressed = False
search_color = 5197761
click_delay = 0.25

user = windll.LoadLibrary('user32.dll')
dc = user.GetDC(0)
gdi = windll.LoadLibrary('gdi32.dll')

# --- Lizenz-Datei online ---
GITHUB_KEYS_URL = "https://raw.githubusercontent.com/Assmar00/Assmar00/refs/heads/main/keys.json"

# --- Funktionen für HWID & Lizenz ---
def get_hwid():
    try:
        # PowerShell-Befehl statt wmic, kompatibel mit Windows 11
        cmd = ['powershell', '-Command', '(Get-CimInstance -ClassName Win32_ComputerSystemProduct).UUID']
        output = subprocess.check_output(cmd, text=True).strip()
        return output
    except Exception as e:
        print("HWID konnte nicht ausgelesen werden:", e)
        return "UNKNOWN_HWID"

def load_keys_online():
    try:
        response = requests.get(GITHUB_KEYS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print("Fehler beim Laden der Keys online:", response.status_code)
            return {}
    except Exception as e:
        print("Fehler beim Laden der Keys online:", e)
        return {}

def check_license_online(key):
    hwid = get_hwid()
    keys = load_keys_online()

    if key not in keys:
        return False, "Key does not exist!"

    if keys[key]['hwid'] == "NONE":
        # Hinweis: HWID kann nur manuell in der GitHub-JSON geändert werden.
        return True, "Key Successful!"

    if keys[key]['hwid'] == hwid:
        return True, "Lizenz gültig!"

    return False, "HWID does not match!"

def on_check_license():
    key = license_entry.get().strip()
    valid, msg = check_license_online(key)
    if valid:
        status_label.configure(text=msg, text_color="green")
        start_button.configure(state="normal")
    else:
        status_label.configure(text=msg, text_color="red")
        start_button.configure(state="disabled")

# --- Starfield Effect ---
class Starfield:
    def __init__(self, canvas, width, height, num_stars=80):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.stars = [{'x': random.randint(0, width),
                       'y': random.randint(0, height),
                       'size': random.randint(1, 3),
                       'speed': random.uniform(0.5, 1.5)} for _ in range(num_stars)]
        self.animate()

    def animate(self):
        self.canvas.delete('star')
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > self.height:
                star['y'] = 0
                star['x'] = random.randint(0, self.width)
            size = star['size']
            self.canvas.create_oval(star['x'], star['y'], star['x'] + size, star['y'] + size,
                                    fill='white', outline='', tags='star')
        self.canvas.after(30, self.animate)

# --- GUI Setup ---
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

app = ctk.CTk()
app.title('Assmar00')
app.geometry('500x480')
app.resizable(False, False)

canvas = tk.Canvas(app, bg='#1e1e1e', highlightthickness=0)
canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

starfield = Starfield(canvas, 500, 480)

# Einfacher Text als Logo-Ersatz
logo_label = tk.Label(app, text="Assmar00", font=("Arial", 24, "bold"), fg="white", bg="#1e1e1e")
logo_label.place(relx=0.5, rely=0.05, anchor='n')

main_frame = ctk.CTkFrame(app, fg_color='transparent')
main_frame.place(relx=0.5, rely=0.5, anchor='center')

status_icon = ctk.CTkLabel(main_frame, text='📶', text_color='red', font=('Arial', 30))
status_icon.pack(pady=(40, 5))

status_label = ctk.CTkLabel(main_frame, text='Inactive', text_color='red', font=('Arial', 16))
status_label.pack(pady=(0, 30))

# Lizenz GUI
license_label = ctk.CTkLabel(main_frame, text="Lizenzkey eingeben:", font=('Arial', 14))
license_label.pack(pady=(20, 5))

license_entry = ctk.CTkEntry(main_frame, width=250)
license_entry.pack(pady=(0, 15))

check_license_button = ctk.CTkButton(main_frame, text="Lizenz prüfen", command=on_check_license)
check_license_button.pack(pady=(0, 15))

delay_label = ctk.CTkLabel(main_frame, text='Verzögerung: 250 ms', font=('Arial', 14))
delay_label.pack(pady=(0, 5))

slider = ctk.CTkSlider(main_frame, from_=0, to=1000, command=lambda v: update_slider_label(v), button_color='white')
slider.set(250)
slider.pack(pady=(0, 25))

start_button = ctk.CTkButton(main_frame, text='Start', fg_color='red', command=lambda: toggle_clicker(), width=150, state='disabled')
start_button.pack(pady=(0, 10))

kill_button = ctk.CTkButton(main_frame, text='Kill', fg_color='#555555', command=lambda: kill_script(), width=150)
kill_button.pack()

made_by_label = ctk.CTkLabel(app, text='Made By Assmar00', text_color='white', font=('Consolas', 14, 'bold'))
made_by_label.place(relx=0.5, y=5, anchor='n')

# --- Funktionen ---
def kill_script():
    global alive
    alive = False
    app.destroy()
    sys.exit()

def get_pixel():
    x = user.GetSystemMetrics(0) // 2
    y = user.GetSystemMetrics(1) // 2
    return gdi.GetPixel(dc, x, y)

def change_pixel_color():
    global search_color
    search_color = get_pixel()
    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)

def check():
    try:
        if get_pixel() == search_color:
            pyautogui.mouseDown()
            time.sleep(random.uniform(0.06, 0.2))
            pyautogui.mouseUp()
        return
    except pyautogui.FailSafeException:
        return None

def on_click(x, y, button, pressed):
    global right_mouse_pressed
    if button == Button.right:
        right_mouse_pressed = pressed
    return None

mouse_listener = Listener(on_click=on_click)
mouse_listener.start()

def run_clicker():
    while alive:
        if running and right_mouse_pressed:
            check()
        time.sleep(click_delay)

def toggle_clicker():
    global running
    running = not running
    status_label.configure(text='Active' if running else 'Inactive',
                           text_color='green' if running else 'red')
    status_icon.configure(text_color='green' if running else 'red')
    start_button.configure(text='Stop' if running else 'Start',
                           fg_color='green' if running else 'red')

def update_slider_label(value):
    global click_delay
    click_delay = float(value) / 1000.0
    delay_label.configure(text=f'Verzögerung: {int(float(value))} ms')

# --- Starte den Clicker-Thread ---
threading.Thread(target=run_clicker, daemon=True).start()
app.mainloop()
