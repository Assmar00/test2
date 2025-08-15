import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import queue
import requests
import sys
import os
import shutil
import tempfile
import uuid

KEYS_URL = "https://raw.githubusercontent.com/Assmar00/Assmar00/main/keys.json"

def get_hwid():
    # Holt die HWID des PCs über MAC-Adresse
    return str(uuid.UUID(int=uuid.getnode())).upper()

def check_license():
    class LicenseDialog(tk.Toplevel):
        def __init__(self, parent):
            super().__init__(parent)
            self.configure(bg='#0e0e0e')
            self.resizable(False, False)
            self.grab_set()
            self.key = None
            self.title('Made By Assmar00')
            try:
                self.iconbitmap('icon.ico')
            except Exception:
                pass
            topbar = tk.Frame(self, bg='#0e0e0e', height=32)
            topbar.pack(fill=tk.X, side=tk.TOP)
            self.status_label = tk.Label(self, text='', font=('Arial', 11), bg='#0e0e0e', fg='#ff00aa')
            self.status_label.pack(pady=(5, 0))
            label = tk.Label(self, text='🔑 Please Enter Your License Key', font=('Arial', 14, 'bold'), bg='#0e0e0e', fg='#ff00aa')
            label.pack(padx=20, pady=(10, 10))
            self.entry = tk.Entry(self, font=('Consolas', 12), width=32, bg='#1a1a1a', fg='white', insertbackground='white', bd=2, relief='flat', show='*')
            self.entry.pack(padx=20, pady=10)
            self.entry.focus()
            btn = tk.Button(self, text='Login', font=('Arial', 12, 'bold'), bg='#ff00aa', fg='white', activebackground='#ff33bb', activeforeground='white', command=self.submit)
            btn.pack(pady=(10, 20))
            self.bind('<Return>', lambda event: self.submit())
            self.update_idletasks()
            w = 400
            h = 220
            x = self.winfo_screenwidth() // 2 - w // 2
            y = self.winfo_screenheight() // 2 - h // 2
            self.geometry(f'{w}x{h}+{x}+{y}')

        def submit(self):
            self.key = self.entry.get().strip()
            if not self.key:
                self.status_label.config(text='⚠️ No License Key Entered!', fg='#ff00aa')
                return
            try:
                response = requests.get(KEYS_URL, timeout=10)
                response.raise_for_status()
                keys = response.json()
            except Exception as e:
                self.status_label.config(text=f'❌ Fehler beim Laden der Keys: {e}', fg='#ff00aa')
                return

            hwid = get_hwid()
            key_data = keys.get(self.key)
            if key_data and key_data.get("hwid") in ["NONE", hwid]:
                self.status_label.config(text='✅ License is Successful!', fg='#00ff99')
                self.after(1000, self.destroy)
            else:
                self.status_label.config(text='❌ License Invalid or HWID Mismatch!', fg='#ff00aa')

    root = tk.Tk()
    root.withdraw()
    dialog = LicenseDialog(root)
    root.wait_window(dialog)
    try:
        keys = requests.get(KEYS_URL, timeout=10).json()
        hwid = get_hwid()
        key_data = keys.get(dialog.key)
        if key_data and key_data.get("hwid") in ["NONE", hwid]:
            root.destroy()
            return True
    except:
        pass
    root.destroy()
    sys.exit('Lizenzprüfung fehlgeschlagen.')

check_license()

BG_COLOR = '#0e0e0e'
FG_COLOR = '#ff00aa'
TEXT_COLOR = 'white'

class TriggerbotGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Made By Assmar00')
        try:
            self.root.iconbitmap('icon.ico')
        except Exception:
            pass
        self.root.geometry('800x600')
        self.root.configure(bg=BG_COLOR)
        self.root.protocol('WM_DELETE_WINDOW', self.root.destroy)

        topbar = tk.Frame(self.root, bg=BG_COLOR, height=40)
        topbar.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(topbar, text='Made By Assmar00 (BETA)', bg=BG_COLOR, fg=FG_COLOR, font=('Arial', 20, 'bold'))
        title_label.pack(side=tk.LEFT, padx=10, pady=2)

        close_btn = tk.Button(topbar, text='✕', bg=BG_COLOR, fg=FG_COLOR, borderwidth=0, font=('Arial', 16, 'bold'), activebackground='#1a1a1a', activeforeground=FG_COLOR, command=self.root.destroy)
        close_btn.pack(side=tk.RIGHT, padx=8, pady=2)

        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.execute_button = tk.Button(main_frame, text='🚀 Triggerbot Starten', command=self.execute_script, height=2, font=('Arial', 12, 'bold'), bg=FG_COLOR, fg='white', activebackground='#ff33bb', activeforeground='white')
        self.execute_button.pack(pady=10)

        self.panic_button = tk.Button(main_frame, text='🛑 PANIC BUTTON', command=self.panic, height=2, font=('Arial', 12, 'bold'), bg='red', fg='white', activebackground='#ff4444', activeforeground='white')
        self.panic_button.pack(pady=10)

        self.output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=25, font=('Consolas', 10), bg='#1a1a1a', fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=10)

        self.output_queue = queue.Queue()
        self.process_queue()
        self.process = None

        self.root.mainloop()

    def execute_script(self):
        def run_script():
            try:
                self.output_queue.put('✅ Successfully Injected')
                script_content = r'''
# Hier kommt dein PowerShell Triggerbot Script wie gehabt
'''
                CREATE_NO_WINDOW = 0x08000000
                self.process = subprocess.Popen(
                    ['powershell', '-ExecutionPolicy', 'Bypass', '-Command', script_content],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    bufsize=1,
                    universal_newlines=True,
                    creationflags=CREATE_NO_WINDOW
                )
                while True:
                    output = self.process.stdout.readline()
                    if output == '' and self.process.poll() is not None:
                        break
                    if output:
                        self.output_queue.put(output.strip())
                remaining_output, errors = self.process.communicate()
                if remaining_output:
                    self.output_queue.put(remaining_output.strip())
                if errors:
                    self.output_queue.put(f'Error: {errors.strip()}')
            except Exception as e:
                self.output_queue.put(f'Error: {str(e)}')

        thread = threading.Thread(target=run_script)
        thread.daemon = True
        thread.start()

    def panic(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.output_queue.put('🛑 PANIC BUTTON aktiviert! Triggerbot gestoppt.')

        try:
            current_file = os.path.realpath(__file__)
            os.remove(current_file)
            self.output_queue.put(f'✅ Datei gelöscht: {current_file}')
        except Exception as e:
            self.output_queue.put(f'⚠️ Datei konnte nicht gelöscht werden: {e}')

        try:
            temp_dir = tempfile.gettempdir()
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except:
                    pass
            self.output_queue.put('✅ Temporäre Dateien gelöscht')
        except Exception as e:
            self.output_queue.put(f'⚠️ Temp-Löschen fehlgeschlagen: {e}')

        sys.exit()

    def process_queue(self):
        try:
            while True:
                line = self.output_queue.get_nowait()
                self.output_text.insert(tk.END, line + '\n')
                self.output_text.yview(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

TriggerbotGUI()
