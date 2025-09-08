import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from phone_control import CiscoPhoneController

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('Cisco Remote Phone Control')
        self.master.geometry("500x450")
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
        image_frame = tk.Frame(master)
        image_frame.pack()
        self.img_label = tk.Label(image_frame)
        self.img_label.pack(side=tk.LEFT)
        tk.Button(image_frame, text="Refresh", command=self.refresh_screen).pack(side=tk.LEFT, padx=10)
        self.display_image("immagine.png")

        # Frame dinamici dopo connessione
        self.keyboard_frame = None
        self.dpad_frame = None
        self.softkey_frame = None
        self.extra_frame = None
        self.exit_frame = None

    def display_image(self, path):
        img = Image.open(path)
        img = img.resize((375, 250), Image.BICUBIC)
        self.photo = ImageTk.PhotoImage(img)
        self.img_label.configure(image=self.photo)
        self.img_label.image = self.photo
    
    def refresh_screen(self):
        if self.controller:
            try:
                img_path = self.controller.get_screen()
                self.display_image(img_path)
            except Exception as e:
                messagebox.showerror("Errore refresh", str(e))

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
        # Softkey
        if self.softkey_frame:
            self.softkey_frame.destroy()
        self.softkey_frame = tk.Frame(self.master)
        self.softkey_frame.pack(pady=4)
        for idx in range(1,5):
            tk.Button(self.softkey_frame, text=f"Soft{idx}",
                    command=lambda i=idx: self.press_button(f"SoftKey{i}")).pack(side=tk.LEFT, padx=2)

        # Pad direzionale (spostato qui)
        if self.dpad_frame:
            self.dpad_frame.destroy()
        self.dpad_frame = tk.Frame(self.master)
        self.dpad_frame.pack(pady=8)
        
        # Tasto Su (riga 0, colonna 1)
        tk.Button(self.dpad_frame, text="Su", width=8,
                command=lambda: self.press_button("Up")).grid(row=0, column=1, padx=2, pady=2)
        
        # Riga centrale: Sinistra, Select, Destra
        tk.Button(self.dpad_frame, text="Sinistra", width=8,
                command=lambda: self.press_button("Left")).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(self.dpad_frame, text="OK", width=8,
                command=lambda: self.press_button("Select")).grid(row=1, column=1, padx=2, pady=2)
        tk.Button(self.dpad_frame, text="Destra", width=8,
                command=lambda: self.press_button("Right")).grid(row=1, column=2, padx=2, pady=2)
        
        # Tasto Giù (riga 2, colonna 1)
        tk.Button(self.dpad_frame, text="Giù", width=8,
                command=lambda: self.press_button("Down")).grid(row=2, column=1, padx=2, pady=2)

        # Tastiera numerica
        if self.keyboard_frame:
            self.keyboard_frame.destroy()
        self.keyboard_frame = tk.Frame(self.master)
        self.keyboard_frame.pack(pady=8)
        keys = [
            ['1','2','3'], ['4','5','6'], ['7','8','9'], ['*','0','#']
        ]
        for y, row in enumerate(keys):
            for x, key in enumerate(row):
                tk.Button(self.keyboard_frame, text=key, width=5,
                        command=lambda v=key: self.press_button(v)).grid(row=y, column=x)

        # Settings, Directory e Applications
        if self.extra_frame:
            self.extra_frame.destroy()
        self.extra_frame = tk.Frame(self.master)
        self.extra_frame.pack(pady=4)
        tk.Button(self.extra_frame, text="Settings", command=lambda: self.press_button('Settings')).pack(side=tk.LEFT, padx=4)
        tk.Button(self.extra_frame, text="Directory", command=lambda: self.press_button('Directory')).pack(side=tk.LEFT, padx=4)
        tk.Button(self.extra_frame, text="Applications", command=lambda: self.press_button('Applications')).pack(side=tk.LEFT, padx=4)
        
        # Tasto Esci (gestito come gli altri frame)
        if self.exit_frame:  # Oppure crea una nuova variabile self.exit_frame
            self.exit_frame.destroy()
        self.exit_frame = tk.Frame(self.master)
        self.exit_frame.pack(pady=8)
        tk.Button(self.exit_frame, text="Esci", command=self.master.quit).pack()
        
        # Aumenta l'altezza a 750px
        self.master.geometry("500x820")

    def press_button(self, value):
        if self.controller:
            self.controller.send_button(value)
            img_path = self.controller.get_screen()
            self.display_image(img_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()