import tkinter as tk
from tkinter import Toplevel

def open_equipment_page(window):
    player_window = Toplevel(window)
    player_window.title("Equipment Parts Page")
    tk.Label(player_window, text="Bienvenue sur la page du joueur").pack()
