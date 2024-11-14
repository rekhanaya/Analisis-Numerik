import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox


def find_extrema(coefficients):
    # Definisikan polinomial berdasarkan koefisien yang diberikan
    p = np.poly1d(coefficients)
    # Hitung turunan pertama dari polinomial
    dp = np.polyder(p)
    # Cari akar-akar dari turunan pertama (titik-titik kritis)
    critical_points = fsolve(dp, np.linspace(-10, 10, 100))
    # Filter untuk menghapus akar duplikat
    critical_points = np.unique(np.round(critical_points, decimals=5))
    # Hitung turunan kedua dari polinomial
    ddp = np.polyder(dp)
    # Tentukan jenis titik kritis (minima atau maksima)
    minima = []
    maksima = []
    for point in critical_points:
        if ddp(point) > 0:
            minima.append(point)
        elif ddp(point) < 0:
            maksima.append(point)
    return minima, maksima, p


def plot_polynomial(coefficients, minima, maksima):
    p = np.poly1d(coefficients)
    x = np.linspace(-10, 10, 400)
    y = p(x)

    plt.figure()
    plt.plot(x, y, label='Polynomial')
    plt.scatter(minima, p(minima), color='red', label='Minima')
    plt.scatter(maksima, p(maksima), color='green', label='Maksima')
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.title('Polynomial and its Extrema')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def on_calculate():
    coefficients_str = entry_coefficients.get()
    try:
        coefficients = list(map(float, coefficients_str.split()))
        minima, maksima, p = find_extrema(coefficients)
        minima_str = ', '.join([f'{x:.2f}' for x in minima])
        maksima_str = ', '.join([f'{x:.2f}' for x in maksima])
        messagebox.showinfo("Results", f"Minima: {minima_str}\nMaksima: {maksima_str}")
        plot_polynomial(coefficients, minima, maksima)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")


# Setup GUI
root = tk.Tk()
root.title("Polynomial Extrema Finder")

label_instruction = tk.Label(root, text="Enter polynomial coefficients (highest to lowest degree):")
label_instruction.pack()

entry_coefficients = tk.Entry(root, width=50)
entry_coefficients.pack()

button_calculate = tk.Button(root, text="Calculate Extrema", command=on_calculate)
button_calculate.pack()

root.mainloop()
