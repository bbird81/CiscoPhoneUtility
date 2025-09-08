import tkinter as tk
from tkinter import PhotoImage, scrolledtext
from PIL import Image, ImageTk

class InterfacciaGrafica:
    def __init__(self, master):
        self.master = master
        master.title("Interfaccia Grafica")
        master.minsize(600, 220)

        # Prima sezione: Immagine
        self.sezione_immagine = tk.Frame(master, width=600, height=500)
        self.sezione_immagine.grid(row=0, column=0,padx=20, pady=10)
        self.carica_immagine()

        # Seconda sezione: Tasti
        self.sezione_tasti = tk.Frame(master, width=600, height=500)
        self.sezione_tasti.grid(row=1, column=0,padx=20, pady=10)
        self.crea_tasti()

        # Terza sezione: Scorrimento testo
        self.sezione_scorri_testo = tk.Frame(master, width=600, height=1000)
        self.sezione_scorri_testo.grid(row=0, column=1, rowspan=2,padx=20, pady=10)
        self.crea_scorri_testo()

    def carica_immagine(self):
        # Carica l'immagine originale
        immagine_originale = Image.open("immagine.png")

        # Definisci le dimensioni desiderate
        larghezza_desiderata = 400
        altezza_desiderata = 400

        # Calcola le nuove dimensioni mantenendo il rapporto d'aspetto
        larghezza_originale, altezza_originale = immagine_originale.size
        rapporto = min(larghezza_desiderata / larghezza_originale, altezza_desiderata / altezza_originale)
        nuova_larghezza = int(larghezza_originale * rapporto)
        nuova_altezza = int(altezza_originale * rapporto)

        # Ridimensiona l'immagine
        immagine_ridimensionata = immagine_originale.resize((nuova_larghezza, nuova_altezza), Image.BICUBIC)

        # Converte l'immagine per Tkinter
        immagine = ImageTk.PhotoImage(immagine_ridimensionata)

        # Mostra l'immagine nella finestra
        label_immagine = tk.Label(self.sezione_immagine, image=immagine)
        label_immagine.image = immagine
        label_immagine.pack()


    def crea_tasti(self):
        for i in range(4):
            tasto = tk.Button(self.sezione_tasti, text=f"Tasto {i+1}", command=lambda: self.azione_tasto(i+1))
            tasto.pack(pady=5)

    def crea_scorri_testo(self):
        self.scorri_testo = scrolledtext.ScrolledText(self.sezione_scorri_testo, wrap=tk.WORD, width=30, height=25)
        self.scorri_testo.pack()

    def azione_tasto(self, numero_tasto):
        self.scorri_testo.insert(tk.END, f"Premuto Tasto {numero_tasto}\n")

if __name__ == "__main__":
    root = tk.Tk()
    interfaccia = InterfacciaGrafica(root)
    root.mainloop()
