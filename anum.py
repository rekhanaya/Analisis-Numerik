import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Pendefinisian fungsi
def f(x):
    a = 0.2
    b = 1.4
    c = -8
    d = -23
    return a * x ** 3 + b * x ** 2 + c * x + d

# Turunan pertama dari fungsi
def df(x):
    return 3 * 0.2 * x ** 2 + 2 * 1.4 * x - 8

# -- Metode Numerik --
def numeric_method(f, x_awal, x_akhir, dx, err_m):
    roots = []
    x_values = np.arange(x_awal, x_akhir, dx)  # Membuat serangkaian nilai x dengan interval dx

    # Loop untuk memeriksa setiap subinterval dari x_values
    for i in range(len(x_values) - 1):
        if df(x_values[i]) * df(x_values[i + 1]) < 0:  # Memeriksa perpotongan turunan pertama di dalam subinterval
            xl = x_values[i]
            xu = x_values[i + 1]
            xr = (xl + xu) / 2  # Tebakan awal menggunakan metode bisection

            # Iterasi metode bisection untuk mencari titik ekstremum dengan akurasi yang diinginkan (err_m)
            while abs(df(xr)) > err_m:
                if df(xl) * df(xr) < 0:  # Jika perpotongan terjadi di antara xl dan xr
                    xu = xr
                else:  # Jika perpotongan terjadi di antara xr dan xu
                    xl = xr
                xr = (xl + xu) / 2  # Perbarui tebakan xr untuk iterasi berikutnya

            roots.append(xr)

    return roots

# -- Metode False Position --
def false_position(xl, xu, err_m):
    xr = xu - (f(xu) * (xu - xl)) / (f(xu) - f(xl))
    while abs(f(xr)) > err_m:
        if f(xl) * f(xr) < 0:  # Menentukan jika lokasi berada diantara f(xl) dan f(xr)
            xu = xr
        else:
            xl = xr
        xr = xu - (f(xu) * (xu - xl)) / (f(xu) - f(xl))
    return xr

# -- Penyelesaian --
# Fungsi untuk menampilkan hasil perhitungan
def show_results(roots_numeric, roots_false_position):
    # Membuat teks untuk ditampilkan di message box
    message = "Titik ekstremum:\n"
    for root in roots_numeric:
        message += f"x = {root}, y = {f(root)}\n"

    message += "\nAkar-akar fungsi dalam interval menggunakan metode false position:\n"
    for root in roots_false_position:
        message += f"x = {root}, y = {f(root)}\n"

    # Membuat message box dan menampilkan hasil
    messagebox.showinfo("Hasil Perhitungan", message)

# Fungsi untuk menangani tombol "Hitung"
def calculate():
    # Pengaturan parameter
    x_awal = float(entry_x_awal.get())
    x_akhir = float(entry_x_akhir.get())
    err_m = float(entry_err_m.get())
    dx = float(entry_dx.get())

    # Metode Newton-Raphson untuk mencari titik ekstremum
    roots_numeric = numeric_method(df, x_awal, x_akhir, dx, err_m)

    # Metode False Position untuk mencari akar
    roots_false_position = []
    x = np.arange(x_awal, x_akhir, dx)
    for i in range(len(x) - 1):
        if f(x[i]) * f(x[i + 1]) < 0:
            root = false_position(x[i], x[i + 1], err_m)
            roots_false_position.append(root)

    # Menampilkan hasil menggunakan message box
    show_results(roots_numeric, roots_false_position)

    # Update plot
    ax.clear()
    x_plot = np.linspace(x_awal, x_akhir, 10000)
    ax.plot(x_plot, f(x_plot), '-g', label='y')

    # Menambahkan scatter plot untuk titik ekstremum
    ax.scatter(roots_numeric, [f(root) for root in roots_numeric], color='blue', label='Ymaks-Ymin')

    # Menambahkan scatter plot untuk akar
    ax.scatter(roots_false_position, [f(root) for root in roots_false_position], color='red', label='Akar')

    # Menambahkan garis putus-putus
    min_y = min(f(x_plot))
    max_y = max(f(x_plot))
    for root in roots_numeric:
        ax.vlines(root, min_y, max_y, linestyles='dashed', colors='green')  # Warna untuk akar
    for root in roots_false_position:
        ax.vlines(root, min_y, max_y, linestyles='dashed', colors='purple')  # Warna untuk akar

    # Menambahkan garis untuk sumbu x di (0,0)
    ax.axhline(0, color='black', linestyle='-')

    ax.legend(loc='upper left')
    ax.grid()
    canvas.draw()


# Membuat GUI
root = tk.Tk()
root.title("Kalkulator Fungsi")

# Membuat label dan entry untuk setiap parameter
tk.Label(root, text="Nilai x_awal:").grid(row=0, column=0)
entry_x_awal = tk.Entry(root)
entry_x_awal.grid(row=0, column=1)

tk.Label(root, text="Nilai x_akhir:").grid(row=1, column=0)
entry_x_akhir = tk.Entry(root)
entry_x_akhir.grid(row=1, column=1)

tk.Label(root, text="Nilai err_m:").grid(row=2, column=0)
entry_err_m = tk.Entry(root)
entry_err_m.grid(row=2, column=1)

tk.Label(root, text="Nilai dx:").grid(row=3, column=0)
entry_dx = tk.Entry(root)
entry_dx.grid(row=3, column=1)

# Tombol untuk melakukan perhitungan
btn_calculate = tk.Button(root, text="Hitung", command=calculate)
btn_calculate.grid(row=4, columnspan=2)

# Membuat area untuk menampilkan grafik
fig, ax = plt.subplots(figsize=(6, 6.5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=5, columnspan=2)


root.mainloop()
