import argparse, logging
from PIL import Image, ImageTk

if __name__ == "__main__":
    ############### Argument parsing
    # Configura l'argomento da linea di comando
    parser = argparse.ArgumentParser(description='Tool manipolazione telefoni')
    parser.add_argument('--debug', action='store_true', help='Attiva la modalità debug.')
    parser.add_argument('--showDP', action='store_true', help='Mostra la colonna "Device Pool" nel report.')
    parser.add_argument('--showUnregistered', action='store_true', help='Aggiunge i telefoni non registrati nel report.')
    parser.add_argument('--cluster', type=str, help='Nome del cluster a cui collegarsi. Può essere [RS|TOP200|MZ]. Se assente, viene chiesto.')
    parser.add_argument('--dpname', type=str, help='Nome del device pool da controllare. Se assente, viene chiesto una porzione del nome da cercare.')
    args = parser.parse_args()
    if args.debug:
        LEVEL=logging.DEBUG
    else:
        LEVEL=logging.INFO
    #################################
    

    import tkinter as tk

    mainWindow = tk.Tk()
    mainWindow.title("Phone Screenshot")


    def handle_button_press(event):
        mainWindow.destroy()

    phoneScreenshot = tk.Frame(mainWindow, width=600, height=500)
    phoneScreenshot.grid(row=0, column=0,padx=20, pady=10)

    frameTasti = tk.Frame(mainWindow, width=600, height=500)
    frameTasti.grid(row=2, column=0,padx=20, pady=10)

    frameTextFields = tk.Frame(mainWindow, width=600, height=500)
    frameTextFields.grid(row=1, column=0,padx=20, pady=10)

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
    label_immagine = tk.Label(phoneScreenshot, image=immagine)
    label_immagine.image = immagine
    label_immagine.pack()

    # Tasto
    button = tk.Button(frameTasti, text="Close.")
    button.bind("event", handle_button_press)
    button.pack()

    # Campi da compilare - Labels
    labelsFrame = tk.Frame(frameTextFields, width=600, height=500)
    labelsFrame.grid(row=0, column=0,padx=20, pady=10)
    inputFrame = tk.Frame(frameTextFields, width=600, height=500)
    inputFrame.grid(row=0, column=1,padx=20, pady=10)

    cucmLBL = tk.Label(labelsFrame, text="CUCM IP/FQDN:")
    cucmLBL.pack()
    userLBL = tk.Label(labelsFrame, text="AXL User:")
    userLBL.pack()
    pwdLBL = tk.Label(labelsFrame, text="AXL Password:")
    pwdLBL.pack()
    # Campi da compilare - input fields
    inputtxt = tk.Text(inputFrame, height = 1, width = 25, bg = "light yellow")
    inputtxt.pack()
    inputtxt = tk.Text(inputFrame, height = 1, width = 25, bg = "light yellow")
    inputtxt.pack()
    inputtxt = tk.Text(inputFrame, height = 1, width = 25, bg = "light yellow")
    inputtxt.pack()

    # Start the event loop.
    mainWindow.mainloop()
else:
    print("This tool is intented to be run from command line :)")


