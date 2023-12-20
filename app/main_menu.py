import tkinter as tk
from app import player
from app import inventory
from app import equipment


def run_main_menu():
    window = tk.Tk()
    window.title("Tool Main Menu")
    window.minsize(800,600)
    window.resizable = True

    player_button = tk.Button(window, text="Player Page", command=lambda:player.open_player_page(window))
    inventory_button = tk.Button(window, text="Inventory Object Page", command= inventory.open_inventory_page)
    equipment_button = tk.Button(window, text="Equipment Parts Page", command= equipment.open_equipment_page)

    #player_button.pack(pady=10)
    #inventory_button.pack(pady=10)
    #equipment_button.pack(pady=10)


    window.mainloop()