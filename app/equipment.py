import tkinter as tk
from tkinter import ttk, filedialog
import json
import random

# Initialiser l'inventaire global
inventory = {}

# Fonction pour générer un identifiant unique pour chaque pièce d'équipement
def generate_id():
    return random.randint(1000, 9999)

# Fonction pour lancer de dés (par exemple "2d4" pour lancer deux dés à quatre faces)
def roll_dice(dice_type):
    number, sides = map(int, dice_type.split('d'))
    return sum(random.randint(1, sides) for _ in range(number))

# Fonction pour ajouter une nouvelle pièce d'équipement à l'inventaire
def add_equipment(name_var, desc_var, image_path, defense_var, inventory_list):
    item_id = generate_id()
    equipment = {
        'id': item_id,
        'name': name_var.get(),
        'description': desc_var.get(),
        'image': image_path,
        'defense': roll_dice(defense_var.get())
    }
    inventory[str(item_id)] = equipment
    update_inventory_list(inventory_list)

# Mettre à jour la liste de l'inventaire dans l'interface utilisateur
def update_inventory_list(inventory_list):
    inventory_list.delete(0, tk.END)
    for item_id, item in inventory.items():
        inventory_list.insert(tk.END, f"{item['name']} (ID: {item_id})")

# Sauvegarder l'inventaire dans un fichier JSON
def save_inventory():
    with open('inventory.json', 'w') as file:
        json.dump(inventory, file, indent=4)

# Charger l'inventaire à partir d'un fichier JSON
def load_inventory(inventory_list):
    try:
        with open('inventory.json', 'r') as file:
            global inventory
            inventory = json.load(file)
            update_inventory_list(inventory_list)
    except FileNotFoundError:
        inventory = {}

# Créer l'interface utilisateur pour les pièces d'équipement
def setup_equipment_interface(root):
    # Créer un onglet ou une nouvelle fenêtre pour les pièces d'équipement
    equipment_frame = ttk.Frame(root)

    # Créer et placer les widgets pour entrer les détails de l'équipement
    name_label = ttk.Label(equipment_frame, text="Nom:")
    name_entry = ttk.Entry(equipment_frame)
    name_label.pack()
    name_entry.pack()

    desc_label = ttk.Label(equipment_frame, text="Description:")
    desc_entry = ttk.Entry(equipment_frame)
    desc_label.pack()
    desc_entry.pack()

    image_label = ttk.Label(equipment_frame, text="Image:")
    image_button = ttk.Button(equipment_frame, text="Choisir une image", command=lambda: select_image(image_path))
    image_label.pack()
    image_button.pack()

    defense_label = ttk.Label(equipment_frame, text="Défense de base (par exemple '2d4'):")
    defense_entry = ttk.Entry(equipment_frame)
    defense_label.pack()
    defense_entry.pack()

    # Bouton pour ajouter l'équipement à l'inventaire
    add_button = ttk.Button(equipment_frame, text="Ajouter l'équipement", command=lambda: add_equipment(name_entry.get(), desc_entry.get(), image_path.get(), defense_entry.get(), inventory_list))
    add_button.pack()

    # Liste pour afficher l'inventaire
    inventory_list = tk.Listbox(root)
    inventory_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    load_inventory(inventory_list)

    return equipment_frame

# Fonction pour choisir une image pour l'équipement
def select_image(image_path):
    file_path = filedialog.askopenfilename()
    if file_path:
        image_path.set(file_path)

# Point d'entrée pour exécuter l'application
def main():
    root = tk.Tk()
    root.title("Gestionnaire d'Inventaire d'Équipement")

    image_path = tk.StringVar()

    equipment_interface = setup_equipment_interface(root)
    equipment_interface.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    root.mainloop()
