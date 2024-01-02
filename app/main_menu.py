import tkinter as tk
from app import player
from app import inventory
from app import equipment

def run_main_menu():
    window = tk.Tk()
    window.title("Tool Main Menu")

    # Définir la taille initiale et la taille minimale
    window.geometry("800x600")
    window.minsize(800, 600)  # Taille minimale de la fenêtre

    window.resizable(True, True)  # Rendre la fenêtre redimensionnable

    # Créer un cadre pour centrer les boutons
    button_frame = tk.Frame(window)
    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    player_button = tk.Button(button_frame, text="Player Page", command=lambda: player.open_player_page(window))
    inventory_button = tk.Button(button_frame, text="Inventory Object Page", command=lambda: inventory.open_Inventory_page(window))
    equipment_button = tk.Button(button_frame, text="Equipment Parts Page", command=lambda: equipment.open_Inventory_page(window))

    # Organiser les boutons dans le cadre
    player_button.pack(pady=10)
    inventory_button.pack(pady=10)
    equipment_button.pack(pady=10)

    window.mainloop()
