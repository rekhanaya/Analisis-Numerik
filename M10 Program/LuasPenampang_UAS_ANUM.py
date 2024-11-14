import numpy as np
import cv2
from tkinter import filedialog, messagebox
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

lebar_latar = 1.6 # meter
tinggi_latar = 1.1 # meter
luas_area = lebar_latar * tinggi_latar
path_labuori = None
path_labu = None

# Proses gambar
def proses_gambar(path_gambar, path_labuori, update_progress):
    # Baca gambar labu dan labu original
    labu = plt.imread(path_gambar)
    labuori = plt.imread(path_labuori)

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

            # Update progress
            progress = ((i * col + j + 1) / total_pixel) * 100
            update_progress(progress)

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
    
# Fungsi untuk mengunggah gambar
def unggah_gambar():
    global panelA, path_labu, label_info
    path = filedialog.askopenfilename(title="Unggah Gambar Labu")

    if len(path) > 0:
        path_labu = path
        gambar_asli = cv2.imread(path)
        gambar_asli_rgb = cv2.cvtColor(gambar_asli, cv2.COLOR_BGR2RGB)
        gambar_asli_rgb = Image.fromarray(gambar_asli_rgb)

        # Resize image to fit in the window
        gambar_asli_rgb.thumbnail((400, 400), Image.Resampling.LANCZOS)
        gambar_asli_rgb = ImageTk.PhotoImage(gambar_asli_rgb)

        if panelA is None:
            panelA = Label(image=gambar_asli_rgb, bg="#F0F8FF")
            panelA.image = gambar_asli_rgb
            panelA.pack(side="left", padx=10, pady=10, expand=True, fill="both")
        else:
            panelA.configure(image=gambar_asli_rgb)
            panelA.image = gambar_asli_rgb

    label_info.config(text="Gambar Labu berhasil diunggah.\nSilakan klik 'Hitung luas penampang gambar' untuk memproses.")

# Fungsi untuk menghitung luas
def hitung_luas():
    global panelB, path_labu, path_labuori, label_luas, progress_var, progress_bar, processing_label
    if path_labu and path_labuori:
        # Menampilkan progress bar dan label pemrosesan
        processing_label.pack(side="top", fill="x", padx=10, pady=10)
        progress_bar.pack(side="top", fill="x", padx=10, pady=10)
        root.update_idletasks()  # Memperbarui tampilan

        # Proses gambar
        def update_progress(progress):
            progress_var.set(f"Memproses gambar... {int(progress)}%")
            progress_bar['value'] = progress
            root.update_idletasks()

        gambar_proses_rgb, luas_dalam_meter = proses_gambar(path_labu, path_labuori, update_progress)
        gambar_proses_rgb = Image.fromarray(gambar_proses_rgb)

        # Resize image to fit in the window
        gambar_proses_rgb.thumbnail((400, 400), Image.Resampling.LANCZOS)
        gambar_proses_rgb = ImageTk.PhotoImage(gambar_proses_rgb)

        if panelB is None:
            panelB = Label(image=gambar_proses_rgb, bg="#F0F8FF")
            panelB.image = gambar_proses_rgb
            panelB.pack(side="right", padx=10, pady=10, expand=True, fill="both")
        else:
            panelB.configure(image=gambar_proses_rgb)
            panelB.image = gambar_proses_rgb

        label_luas.config(text=f"Luas penampang labu kira-kira {luas_dalam_meter:.2f} meter persegi")
        
        # Sembunyikan progress bar dan label pemrosesan setelah selesai
        progress_bar.pack_forget()
        processing_label.pack_forget()
        messagebox.showinfo("Berhasil", "Gambar labu berhasil diproses!")
    else:
        messagebox.showerror("Error", "Silakan unggah gambar labu dan gambar original labu terlebih dahulu.")

# Fungsi untuk mengunggah gambar Labu Original
def unggah_gambar_labuori():
    global path_labuori, label_info
    path_labuori = filedialog.askopenfilename(title="Unggah Gambar Original Labu")
    if path_labuori:
        messagebox.showinfo("Berhasil", "Gambar Original Labu berhasil diunggah!\nSilakan unggah gambar labu untuk diproses.")
        label_info.config(text="Gambar Original Labu berhasil diunggah.\nSilakan unggah gambar labu untuk diproses.")
        
    # Jika kedua gambar sudah diunggah, beri notifikasi kepada pengguna
    if path_labu and path_labuori:
        messagebox.showinfo("Info", "Kedua gambar sudah diunggah. Silakan klik 'Hitung luas penampang gambar' untuk memproses.")
        label_info.config(text="Kedua gambar sudah diunggah. Silakan klik 'Hitung luas penampang gambar' untuk memproses.")

#Membuat jendela GUI
root = Tk()
panelA = None
panelB = None

#Mengatur warna latar belakang jendela
root.configure(bg="#000000")

root.title("Deteksi Luas Penampang Labu")

# MengAtur agar jendela dapat diubah ukurannya
root.resizable(True, True)

btn_unggah_ori = Button(root, text="Unggah Gambar Original Labu", command=unggah_gambar_labuori, bg="#8A2BE2", fg="white", font=("Helvetica", 12, "bold"))
btn_unggah_ori.pack(side="top", fill="x", padx=10, pady=10)

btn_unggah_labu = Button(root, text="Unggah Gambar Labu", command=unggah_gambar, bg="#8A2BE2", fg="white", font=("Helvetica", 12, "bold"))
btn_unggah_labu.pack(side="top", fill="x", padx=10, pady=10)

btn_hitung = Button(root, text="Hitung luas penampang gambar", command=hitung_luas, bg="#8A2BE2", fg="white", font=("Helvetica", 12, "bold"))
btn_hitung.pack(side="top", fill="x", padx=10, pady=10)

progress_var = StringVar()
progress_var.set("Memproses gambar... 0%")
processing_label = Label(root, textvariable=progress_var, bg="#FFD700", fg="black", font=("Helvetica", 12, "bold"))

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")

label_luas = Label(root, text="Luas penampang labu kira-kira 0.00 meter persegi", bg="#8A2BE2", fg="white", font=("Helvetica", 12, "bold"))
label_luas.pack(side="bottom", fill="x", padx=10, pady=10)

root.mainloop()