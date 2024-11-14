import numpy as np
import cv2
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# Konstanta
lebar_latar = 1.6  # meter
tinggi_latar = 1.1  # meter
luas_area = lebar_latar * tinggi_latar

def proses_gambar(path_gambar, path_labuori):
    # Baca gambar labu dan labu original
    labu = cv2.imread(path_gambar)
    labu = cv2.cvtColor(labu, cv2.COLOR_BGR2RGB)
    labuori = cv2.imread(path_labuori)
    labuori = cv2.cvtColor(labuori, cv2.COLOR_BGR2RGB)

    # Ubah ukuran gambar labuori agar sesuai dengan gambar labu
    if labu.shape != labuori.shape:
        labuori = cv2.resize(labuori, (labu.shape[1], labu.shape[0]))

    # Buat salinan gambar labu
    labu_copy = np.copy(labu)

    # Mengambil row dan col dari gambar
    row, col = labu_copy.shape[0], labu_copy.shape[1]

    # Menghitung total pixel
    total_pixel = row * col

    # Menghitung total pixel hitam
    total_black_pixel = 0

    # Penghitungan labu copy
    koordinat = []
    for i in range(row):
        for j in range(col):
            r, g, b = labu_copy[i, j]
            # Mengambil rgb dari labu ori
            r1, g2, b2 = labuori[i, j]
            if (np.float32(r) + np.float32(g) + np.float32(b)) >= 250:
                # Mengganti latar putih menjadi latar original labuori
                labu_copy[i, j] = r1, g2, b2
            if (np.float32(r) + np.float32(g) + np.float32(b)) < 10:
                koordinat.append((i, j))
                total_black_pixel += 1

    if koordinat:
        # Mencari min max untuk i
        min_i = min(koordinat, key=lambda x: x[0])[0]
        max_i = max(koordinat, key=lambda x: x[0])[0]

        # Menghitamkan semua piksel dari min sampai max
        for i in range(min_i, max_i + 1):
            # Mencari min_j dan max_j yang dinamis untuk setiap baris i
            j_koordinat = [k[1] for k in koordinat if k[0] == i]
            if j_koordinat:
                min_j = min(j_koordinat)
                max_j = max(j_koordinat)
                for j in range(min_j, max_j + 1):
                    labu_copy[i, j] = [0, 0, 0]

        # Menghitung luas objek
        luas_objek = (total_black_pixel / total_pixel) * luas_area
    else:
        luas_objek = 0

    return labu_copy, luas_objek

def unggah_gambar():
    global panelA, panelB, path_labuori
    path = filedialog.askopenfilename()
    
    if len(path) > 0:
        path_labuori = filedialog.askopenfilename(title="Unggah Gambar Original Labu")
        if len(path_labuori) > 0:
            gambar_asli = cv2.imread(path)
            gambar_asli_rgb = cv2.cvtColor(gambar_asli, cv2.COLOR_BGR2RGB)
            gambar_asli_rgb = Image.fromarray(gambar_asli_rgb)
            gambar_asli_rgb = ImageTk.PhotoImage(gambar_asli_rgb)

            gambar_proses_rgb, luas_dalam_meter = proses_gambar(path, path_labuori)
            gambar_proses_rgb = Image.fromarray(gambar_proses_rgb)
            gambar_proses_rgb = ImageTk.PhotoImage(gambar_proses_rgb)

            if panelA is None or panelB is None:
                panelA = Label(image=gambar_asli_rgb, bg="lightblue")
                panelA.image = gambar_asli_rgb
                panelA.pack(side="left", padx=10, pady=10)
                
                panelB = Label(image=gambar_proses_rgb, bg="lightblue")
                panelB.image = gambar_proses_rgb
                panelB.pack(side="right", padx=10, pady=10)
            else:
                panelA.configure(image=gambar_asli_rgb)
                panelB.configure(image=gambar_proses_rgb)
                panelA.image = gambar_asli_rgb
                panelB.image = gambar_proses_rgb

            label_luas.config(text=f"Luas penampang labu kira-kira {luas_dalam_meter:.2f} meter persegi")

# Membuat jendela GUI
root = Tk()
panelA = None
panelB = None

# Mengatur warna latar belakang jendela
root.configure(bg="#D10363")

root.title("Deteksi Luas Penampang Labu")

btn = Button(root, text="Unggah Gambar", command=unggah_gambar, bg="#E49BFF")
btn.pack(side="top", fill="both", expand="yes", padx=10, pady=10)

label_luas = Label(root, text="Luas penampang labu kira-kira 0.00 meter persegi", bg="#C738BD")
label_luas.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

root.mainloop()
