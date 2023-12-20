import tkinter as tk
from tkinter import Toplevel

def open_player_page(window):
    player_window = Toplevel(window)
    player_window.title("Player Page")
    tk.Label(player_window, text="Bienvenue sur la page du joueur").pack()
