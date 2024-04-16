import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def split_file(file_path, max_size, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    part_num = 1
    current_size = 0
    current_file = open(os.path.join(output_dir, f"sql_part{part_num}.sql"), 'w', encoding='utf-8')
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            current_size += len(line.encode('utf-8'))
            current_file.write(line)
            if current_size >= max_size * 1024 * 1024 and line.strip().endswith(';'):
                current_file.close()
                part_num += 1
                current_file = open(os.path.join(output_dir, f"sql_part{part_num}.sql"), 'w', encoding='utf-8')
                current_size = 0
        if not line.strip().endswith(';'):
            current_file.write(';')
    if not current_file.closed:
        current_file.close()

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("SQL files", "*.sql")])
    if filename:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, filename)

def browse_output_dir():
    directory = filedialog.askdirectory()
    if directory:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, directory)

def execute_split():
    file_path = file_path_entry.get()
    output_dir = output_dir_entry.get()
    max_size = int(max_size_var.get())
    try:
        split_file(file_path, max_size, output_dir)
        messagebox.showinfo("Successo", "File diviso con successo.")
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def resource_path(relative_path):
    """ Ottiene il percorso delle risorse inserite nel file eseguibile. """
    try:
        # PyInstaller crea un file temporaneo e ci mette dentro i file di risorse
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.title("Divisore di File SQL")

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', background='#333333', foreground='white', font=('Helvetica', 10, 'bold'))
style.map('TButton', background=[('active', '#333333'), ('pressed', '#555555')], foreground=[('active', 'white'), ('pressed', 'white')])

root.configure(background='#f0f0f0')

# Imposta l'icona della finestra utilizzando il percorso base
icon_path = resource_path('favicon.png')
print(f"Icon path: {icon_path}")  # Debug: Stampa il percorso dell'icona
icon = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon)

# Carica il logo della compagnia utilizzando il percorso base
logo_path = resource_path('logo-wink-sql.png')
print(f"Logo path: {logo_path}")  # Debug: Stampa il percorso del logo
logo_image = tk.PhotoImage(file=logo_path)
logo_label = ttk.Label(root, image=logo_image, background='#f0f0f0')
logo_label.pack(pady=10)

ttk.Label(root, text="Percorso File:", background='#f0f0f0').pack(pady=5)
file_path_entry = ttk.Entry(root, width=50)
file_path_entry.pack(pady=5)
ttk.Button(root, text="Sfoglia...", command=browse_file).pack(pady=5)

ttk.Label(root, text="Directory di Output:", background='#f0f0f0').pack(pady=5)
output_dir_entry = ttk.Entry(root, width=50)
output_dir_entry.pack(pady=5)
ttk.Button(root, text="Sfoglia...", command=browse_output_dir).pack(pady=5)

ttk.Label(root, text="Dimensione Massima File (MB):", background='#f0f0f0').pack(pady=5)
max_size_var = tk.StringVar(root)
max_size_var.set("10")  # Imposta la dimensione predefinita a 10MB
max_size_options = ["5", "10", "20", "50", "100"]
max_size_menu = ttk.OptionMenu(root, max_size_var, max_size_var.get(), *max_size_options)
max_size_menu.pack(pady=5)

ttk.Button(root, text="Esegui Divisione", command=execute_split).pack(pady=10)

root.mainloop()