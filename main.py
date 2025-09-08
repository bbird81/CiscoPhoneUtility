import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from phone_control import CiscoPhoneController

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('Cisco Remote Phone Control')
        self.master.geometry("500x650")
        self.controller = None

        # Sezione credenziali
        self.user_var = tk.StringVar()
        self.pwd_var = tk.StringVar()
        self.ip_var = tk.StringVar()

        tk.Label(master, text="User:").pack()
        tk.Entry(master, textvariable=self.user_var).pack()
        tk.Label(master, text="Password:").pack()
        tk.Entry(master, textvariable=self.pwd_var, show="*").pack()
        tk.Label(master, text="IP/FQDN:").pack()
        tk.Entry(master, textvariable=self.ip_var).pack()
        tk.Button(master, text="Collegati", command=self.connect).pack(pady=8)

        # Spazio per immagine display telefono
        self.img_label = tk.Label(master)
        self.img_label.pack()
        self.display_image("immagine.png")

        # Frame dinamici dopo connessione
        self.keyboard_frame = None
        self.dpad_frame = None
        self.softkey_frame = None
        self.extra_frame = None

    def display_image(self, path):
        img = Image.open(path)
        img = img.resize((300, 200), Image.BICUBIC)
        self.photo = ImageTk.PhotoImage(img)
        self.img_label.configure(image=self.photo)
        self.img_label.image = self.photo

    def connect(self):
        user = self.user_var.get()
        pwd = self.pwd_var.get()
        ip = self.ip_var.get()
        try:
            self.controller = CiscoPhoneController(ip, user, pwd)
            img_path = self.controller.get_screen()
            self.display_image(img_path)
            self.draw_controls()
        except Exception as e:
            messagebox.showerror("Connessione fallita", str(e))

    def draw_controls(self):
        # Tastiera numerica
        if self.keyboard_frame:
            self.keyboard_frame.destroy()
        self.keyboard_frame = tk.Frame(self.master)
        self.keyboard_frame.pack()
        keys = [
            ['1','2','3'], ['4','5','6'], ['7','8','9'], ['*','0','#']
        ]
        for y, row in enumerate(keys):
            for x, key in enumerate(row):
                tk.Button(self.keyboard_frame, text=key, width=5,
                          command=lambda v=key: self.press_button(v)).grid(row=y, column=x)

        # Pad direzionale
        if self.dpad_frame:
            self.dpad_frame.destroy()
        self.dpad_frame = tk.Frame(self.master)
        self.dpad_frame.pack(pady=4)
        self.dpad_buttons = [
            ("Su", "Up"), ("Giù", "Down"), ("Sinistra", "Left"), ("Destra", "Right"), ("OK", "Select")
        ]
        for label, cmd in self.dpad_buttons:
            tk.Button(self.dpad_frame, text=label, width=8,
                      command=lambda c=cmd: self.press_button(c)).pack(side=tk.LEFT, padx=2)

        # Softkey
        if self.softkey_frame:
            self.softkey_frame.destroy()
        self.softkey_frame = tk.Frame(self.master)
        self.softkey_frame.pack(pady=4)
        for idx in range(1,5):
            tk.Button(self.softkey_frame, text=f"Soft{idx}",
                      command=lambda i=idx: self.press_button(f"SoftKey{i}")).pack(side=tk.LEFT, padx=2)

        # Settings e Directory
        if self.extra_frame:
            self.extra_frame.destroy()
        self.extra_frame = tk.Frame(self.master)
        self.extra_frame.pack(pady=4)
        tk.Button(self.extra_frame, text="Settings", command=lambda: self.press_button('Settings')).pack(side=tk.LEFT, padx=4)
        tk.Button(self.extra_frame, text="Directory", command=lambda: self.press_button('Directory')).pack(side=tk.LEFT, padx=4)

    def press_button(self, value):
        if self.controller:
            self.controller.send_button(value)
            img_path = self.controller.get_screen()
            self.display_image(img_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()