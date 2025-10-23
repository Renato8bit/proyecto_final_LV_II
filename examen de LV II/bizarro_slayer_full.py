import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import random
import sys
import csv
import os

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title = ("Bizarro Slayer - Menu principal")
        self.root.geometry("500x450")
        ttk.Label(root, text= "Bizarro Slayer", font=("Helvetica",22)).pack(pady=20)
        ttk.Button(root, text= "Nueva Partida", command=self.nueva_partida).pack(pady=8)
        ttk.Button(root, text= "Ver Historal/ Top", command1=self.ver_historial).pack(pady=8)
        ttk.Button(root, text= "Salir", command=self.root.destroy).pack(pady=8)

if __name__ == "__main__" :
    root = tk.Tk()
    MenuApp(root)
    root.mainloop()