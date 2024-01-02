import tkinter as tk
from tkinter import ttk, Label, Entry, Button, Toplevel, Frame, Listbox, filedialog, messagebox
from tkinter.ttk import Combobox
import json
import random
from PIL import Image, ImageTk
from datetime import datetime
from enum import Enum

# Global variables for managing inventory items
global image_path, equipment_listbox, image_label

# Make sure these variables are defined globally or in the same namespace as the load_item_details function
global weapon_name_var, weapon_description_var, weapon_image_var, weapon_power_var, weapon_effect_var, weapon_type_var, weapon_id_label
global armor_name_var, armor_description_var, armor_image_var, armor_defense_var, armor_resistance_var, armor_id_label
global shield_name_var, shield_description_var, shield_image_var, shield_defense_var, shield_id_label


# Enumerations for weapon effects and types
class WeaponEffect(Enum):
    NONE = "None"
    FIRE = "Fire"
    POISON = "Poison"

class WeaponType(Enum):
    MELEE = "Melee"
    RANGED = "Ranged"

# Global variables for managing inventory items
inventory = {
    'Weapons': {},
    'Armor': {},
    'Shield': {}
}
current_image_path = {
    'Weapons': '',
    'Armor': '',
    'Shield': ''
}
current_category = 'Weapons'





# Function to generate a unique identifier for each piece of equipment
def generate_id():
    """Generate a unique identifier for a new item."""
    current_time = datetime.now()
    return current_time.strftime("%Y%m%d%H%M%S%f")

# Function for rolling dice (e.g. "2d4" to roll two four-sided dice)
def roll_dice(dice_type):
    """Roll a dice of the specified type (e.g., '3d4' for three four-sided dice)."""
    number, sides = map(int, dice_type.split('d'))
    return sum(random.randint(1, sides) for _ in range(number))



# Update equipment list in UI
def update_equipment_list(equipment_list):
    equipment_list.delete(0, tk.END)
    for item_id, item in inventory.items():
        equipment_list.insert(tk.END, f"{item['name']} (ID: {item_id})")


# Save Equipment in a json file
def save_equipment():
    try:
        with open("equipment.json", "w") as file:
            json.dump(inventory, file, indent=4)
    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred: {e}")


def load_equipment():
    """Load the entire inventory from the JSON file."""
    global inventory
    try:
        with open("equipment.json", "r") as file:
            inventory = json.load(file)
        update_equipment_listbox(current_category)
    except FileNotFoundError:
        inventory = {'Weapons': {}, 'Armor': {}, 'Shield': {}}
        messagebox.showerror("Load Error", "The inventory file was not found.")

def load_equipment_at_start():
    """Load the inventory from the JSON file at the start of the application."""
    global inventory
    try:
        with open("equipment.json", "r") as file:
            inventory = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, initialize the inventory with empty dictionaries
        inventory = {'Weapons': {}, 'Armor': {}, 'Shield': {}}
    except json.JSONDecodeError:
        # In case of JSON decoding error, show an error and initialize inventory with empty dictionaries
        messagebox.showerror("Load Error", "The inventory file is corrupt or invalid.")
        inventory = {'Weapons': {}, 'Armor': {}, 'Shield': {}}




def update_equipment_listbox(category):
    global equipment_listbox
    equipment_listbox.delete(0, tk.END)
    for item_id, item_info in inventory[category].items():
        equipment_listbox.insert(tk.END, f"{item_info['name']} (ID: {item_id})")

def on_listbox_select(event):
    global inventory, current_category
    global weapon_name_var, weapon_description_var, weapon_image_var, weapon_power_var, weapon_effect_var, weapon_type_var
    global armor_name_var, armor_description_var, armor_image_var, armor_defense_var, armor_resistance_var
    global shield_name_var, shield_description_var, shield_image_var, shield_defense_var, shield_id_label

    if not event.widget.curselection():
        return
    
    item_id = event.widget.get(event.widget.curselection()).split(" (ID: ")[-1].rstrip(")")
    item_details = inventory[current_category].get(item_id, {})

    if current_category == 'Weapons':
        weapon_name_var.set(item_details.get('name', ''))
        weapon_description_var.set(item_details.get('description', ''))
        weapon_image_var.set(item_details.get('image', ''))
        weapon_power_var.set(item_details.get('power', ''))
        weapon_effect_var.set(item_details.get('effect', ''))
        weapon_type_var.set(item_details.get('type', ''))
        weapon_id_label.config(text=item_id)
        update_image_for_selected_tab(current_category)

    elif current_category == 'Armor':
        armor_name_var.set(item_details.get('name', ''))
        armor_description_var.set(item_details.get('description', ''))
        armor_image_var.set(item_details.get('image', ''))
        armor_defense_var.set(item_details.get('defense', ''))
        armor_resistance_var.set(item_details.get('resistance', ''))
        armor_id_label.config(text=item_id)
        update_image_for_selected_tab(current_category)

    elif current_category == 'Potions':
        shield_name_var.set(item_details.get('name', ''))
        shield_description_var.set(item_details.get('description', ''))
        shield_image_var.set(item_details.get('image', ''))
        shield_defense_var.set(item_details.get('defense', ''))
        shield_id_label.config(text=item_id)
        update_image_for_selected_tab(current_category)





def open_image(image_var, image_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        image_var.set(file_path)
        load_image(file_path, image_label)


def load_image(file_path, image_label):
    image = Image.open(file_path)
    image.thumbnail((200, 200))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo  # Keep a reference.


def update_image_for_selected_tab(category):
    # Make sure the variables for image paths are initialized for each category
    global image_label
    image_path = ''
    if category == 'Weapons' and weapon_image_var.get():
        image_path = weapon_image_var.get()
    elif category == 'Armor' and armor_image_var.get():
        image_path = armor_image_var.get()
    elif category == 'Shield' and shield_image_var.get():
        image_path = shield_image_var.get()

    # Load image if path exists
    if image_path:
        load_image(image_path, image_label)
    else:
        # Clear the image if no path is provided
        image_label.config(image=None)
        image_label.image = None




def on_tab_change(event):
    global current_category, tab_control, image_label, current_image_path
    current_category = tab_control.tab(tab_control.select(), "text")
    update_equipment_listbox(current_category)
    update_image_for_selected_tab(current_category)

def add_item_to_inventory(category):
    item_details = get_item_details_from_ui(category)
    if item_details:
        item_id = item_details['id']
        inventory[category][item_id] = item_details
        update_equipment_listbox(category)
        save_equipment()



def get_item_details_from_ui(category):
    global weapon_name_var, weapon_description_var, weapon_image_var, weapon_power_var, weapon_effect_var, weapon_type_var, weapon_id_label
    # Dictionary to return details based on category
    if category == 'Weapons':
        item_details = {
            'name': weapon_name_var.get(),
            'description': weapon_description_var.get(),
            'image': weapon_image_var.get(),
            'power': weapon_power_var.get(),
            'effect': weapon_effect_var.get(),
            'type': weapon_type_var.get(),
            'id': weapon_id_label.cget("text"),
        }
    elif category == 'Armor':
        item_details = {
            'name': armor_name_var.get(),
            'description': armor_description_var.get(),
            'image': armor_image_var.get(),
            'defense': armor_defense_var.get(),
            'resistance': armor_resistance_var.get(),
            'id': armor_id_label.cget("text"),
        }
    elif category == 'Shield':
        item_details = {
            'name': shield_name_var.get(),
            'description': shield_description_var.get(),
            'image': shield_image_var.get(),
            'defense': shield_defense_var.get(),
            'id': shield_id_label.cget("text"),
        }
    return item_details






# Equipment UI functions
def setup_weapon_tab(tab, equipment_list, image_label):
    global weapon_name_var, weapon_description_var, weapon_image_var, weapon_power_var, weapon_effect_var, weapon_type_var, weapon_id_label
    # Weapon Name
    weapon_name_var = tk.StringVar()
    Label(tab, text='Name').grid(row=0, column=0, sticky='e')
    Entry(tab, textvariable=weapon_name_var).grid(row=0, column=1)

    # Weapon Description
    weapon_description_var = tk.StringVar()
    Label(tab, text='Description').grid(row=1, column=0, sticky='e')
    Entry(tab, textvariable=weapon_description_var).grid(row=1, column=1)

     # Image path
    weapon_image_var = tk.StringVar()
    Label(tab, text='Image Path').grid(row=2, column=0, sticky='e')
    Entry(tab, textvariable=weapon_image_var).grid(row=2, column=1)

    # Open Image Button
    open_image_button = Button(tab, text="Open Image", command=lambda: open_image(weapon_image_var, image_label))
    open_image_button.grid(row=2, column=2)

    # Weapon Base Power
    weapon_power_var = tk.StringVar()
    Label(tab, text='Base Power').grid(row=3, column=0, sticky='e')
    Entry(tab, textvariable=weapon_power_var).grid(row=3, column=1)

    # Button to randomize weapon power
    Button(tab, text='Random', command=lambda: weapon_power_var.set(roll_dice('3d4'))).grid(row=3, column=2)

    # Weapon Effect
    weapon_effect_var = tk.StringVar()
    Label(tab, text='Effect').grid(row=4, column=0, sticky='e')
    Combobox(tab, textvariable=weapon_effect_var, values=[e.value for e in WeaponEffect]).grid(row=4, column=1)

    # Weapon Type
    weapon_type_var = tk.StringVar()
    Label(tab, text='Type').grid(row=5, column=0, sticky='e')
    Combobox(tab, textvariable=weapon_type_var, values=[t.value for t in WeaponType]).grid(row=5, column=1)

    Label(tab, text="").grid(row=6, column=1, pady=3)

    # Weapon ID
    weapon_id_label = Label(tab, text=generate_id())
    Label(tab, text='ID').grid(row=7, column=0, sticky='e')
    weapon_id_label.grid(row=7, column=1)

    Label(tab, text="").grid(row=8, column=1, pady=10)

    # Save Weapon Button
    save_weapon_button = Button(tab, text='Save Weapon', command=lambda: add_item_to_inventory('Weapons'))
    save_weapon_button.grid(row=9, column=1, sticky='e')

def setup_armor_tab(tab, equipment_list, image_label):
    global armor_name_var, armor_description_var, armor_image_var, armor_defense_var, armor_resistance_var, armor_id_label
    # Armor Name
    armor_name_var = tk.StringVar()
    Label(tab, text='Name').grid(row=1, column=0, sticky='e')
    Entry(tab, textvariable=armor_name_var).grid(row=1, column=1, sticky='e')

    # Armor Description
    armor_description_var = tk.StringVar()
    Label(tab, text='Description').grid(row=2, column=0, sticky='e')
    Entry(tab, textvariable=armor_description_var).grid(row=2, column=1, sticky='e')

    # Armor Image Path
    armor_image_var = tk.StringVar()
    Label(tab, text='Image Path').grid(row=3, column=0, sticky='e')
    Entry(tab, textvariable=armor_image_var).grid(row=3, column=1, sticky='e')
    
    # Open Image Button
    open_image_button = Button(tab, text="Open Image", command=lambda: open_image(armor_image_var, image_label))
    open_image_button.grid(row=3, column=2)

    # Armor Base Defense (Random 2D4)
    armor_defense_var = tk.StringVar()
    Label(tab, text='Base Defense').grid(row=4, column=0, sticky='e')
    Entry(tab, textvariable=armor_defense_var).grid(row=4, column=1, sticky='e')
    
    # Button to randomize weapon power
    Button(tab, text='Random', command=lambda: armor_defense_var.set(roll_dice('2d4'))).grid(row=4, column=2)
    

    # Armor Resistance Options
    armor_resistance_var = tk.StringVar()
    Label(tab, text='Resistance').grid(row=5, column=0, sticky='e')
    ttk.Combobox(tab, textvariable=armor_resistance_var, values=['None', 'Fire', 'Poison']).grid(row=5, column=1, sticky='e')


    Label(tab, text="").grid(row=6, column=1, pady=3)

    # Armor ID
    armor_id_label = Label(tab, text=generate_id())
    Label(tab, text='ID').grid(row=7, column=0, sticky='e')
    armor_id_label.grid(row=7, column=1)

    Label(tab, text="").grid(row=8, column=1, pady=10)

    # Save Armor Button
    save_armor_button = Button(tab, text='Save Armor',command=lambda: add_item_to_inventory('Armor'))
    save_armor_button.grid(row=9, column=1, sticky='e')

def setup_shield_tab(tab, equipment_list, image_label):
    global shield_name_var, shield_description_var, shield_image_var, shield_defense_var, shield_id_label
    shield_name_var = tk.StringVar()
    Label(tab, text='Name').grid(row=1, column=0, sticky='e')
    Entry(tab, textvariable=shield_name_var).grid(row=1, column=1, sticky='e')

    # Armor Description
    shield_description_var = tk.StringVar()
    Label(tab, text='Description').grid(row=2, column=0, sticky='e')
    Entry(tab, textvariable=shield_description_var).grid(row=2, column=1, sticky='e')

    # Armor Image Path
    shield_image_var = tk.StringVar()
    Label(tab, text='Image Path').grid(row=3, column=0, sticky='e')
    Entry(tab, textvariable=shield_image_var).grid(row=3, column=1, sticky='e')
    
    # Open Image Button
    open_image_button = Button(tab, text="Open Image", command=lambda: open_image(shield_image_var, image_label))
    open_image_button.grid(row=3, column=2)

    # Shield Base Defense (Random 2D4)
    shield_defense_var = tk.StringVar()
    Label(tab, text='Base Defense').grid(row=4, column=0, sticky='e')
    Entry(tab, textvariable=shield_defense_var).grid(row=4, column=1, sticky='e')
    
    # Button to randomize weapon power
    Button(tab, text='Random', command=lambda: shield_defense_var.set(roll_dice('2d4'))).grid(row=4, column=2)
    
    Label(tab, text="").grid(row=6, column=1, pady=3)

    # Weapon ID
    shield_id_label = Label(tab, text=generate_id())
    Label(tab, text='ID').grid(row=7, column=0, sticky='e')
    shield_id_label.grid(row=7, column=1)

    Label(tab, text="").grid(row=8, column=1, pady=10)

    # Save shield Button
    save_shield_button = Button(tab, text='Save shield', command=lambda: add_item_to_inventory('Shield'))
    save_shield_button.grid(row=9, column=1, sticky='e')

def create_new_item():
    global current_category
    global weapon_name_var, weapon_description_var, weapon_image_var, weapon_power_var, weapon_effect_var, weapon_type_var, weapon_id_label
    global armor_name_var, armor_description_var, armor_image_var, armor_defense_var, armor_resistance_var, armor_id_label
    global shield_name_var, shield_description_var, shield_image_var, shield_defense_var, shield_id_label
    
    # Reset fields based on current category
    if current_category == 'Weapons':
        weapon_name_var.set('')
        weapon_description_var.set('')
        weapon_image_var.set('')
        weapon_power_var.set('')
        weapon_effect_var.set('')
        weapon_type_var.set('')
        weapon_id_label.config(text=generate_id())

    elif current_category == 'Armor':
        armor_name_var.set('')
        armor_description_var.set('')
        armor_image_var.set('')
        armor_defense_var.set('')
        armor_resistance_var.set('')
        armor_id_label.config(text=generate_id())

    elif current_category == 'Shield':
        shield_name_var.set('')
        shield_description_var.set('')
        shield_image_var.set('')
        shield_defense_var.set('')
        shield_id_label.config(text=generate_id())

    # Clear displayed image
    image_label.config(image=None)
    image_label.image = None

# Create Equipment UI
def create_equipment_ui(root):
    load_equipment_at_start()
    global equipment_listbox, tab_control, image_label
    # Main frame for the equipment interface
    main_frame = Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Frame for the list and buttons, with adjusted width
    list_frame = Frame(main_frame, width=200, bg='grey')
    list_frame.pack(side='left', fill='y', padx=8, pady=10)

    new_item_button = tk.Button(list_frame, text='Create New Item', command=create_new_item)
    new_item_button.pack(side='top', pady=5)   

    equipment_listbox = tk.Listbox(list_frame, width=30)
    equipment_listbox.pack(side='top', fill='both', expand=True)
    equipment_listbox.bind('<<ListboxSelect>>', on_listbox_select)


    # Delete button
    delete_button = Button(list_frame, text='Delete', command=delete_selected_item)
    delete_button.pack(side='bottom', pady=10)

    # Area for the tabs for configuring items
    tab_control = ttk.Notebook(main_frame)
    tab_control.pack(side='left', fill='both', expand=True, padx=10, pady=10)
    tab_control.bind('<<NotebookTabChanged>>', on_tab_change)

    # Image label
    image_label_frame = Frame(main_frame, width=200, height=400)
    image_label_frame.pack(side='right', fill='both', expand=True)

    image_label = Label(image_label_frame)
    image_label.pack(fill='both', expand=True)

    weapon_tab = Frame(tab_control)
    armor_tab = Frame(tab_control)
    shield_tab = Frame(tab_control)
    
    setup_weapon_tab(weapon_tab, equipment_listbox, image_label)
    setup_armor_tab(armor_tab, equipment_listbox, image_label)
    setup_shield_tab(shield_tab, equipment_listbox, image_label)

    tab_control.add(weapon_tab, text='Weapons')
    tab_control.add(armor_tab, text='Armor')
    tab_control.add(shield_tab, text='Shield')




# Adjust the delete_selected_item function to handle the current category
def delete_selected_item():
    global equipment_listbox, current_category
    selection = equipment_listbox.curselection()
    if not selection:
        return
    selected_item = equipment_listbox.get(selection)
    item_id = selected_item.split(" (ID: ")[-1].rstrip(")")

    if item_id in inventory[current_category]:
        del inventory[current_category][item_id]
        update_equipment_listbox(current_category)


def open_Inventory_page(window):
    equipment_window = Toplevel(window)
    equipment_window.title("Equipment Creation")
    equipment_window.geometry("800x600")
    create_equipment_ui(equipment_window)
    equipment_window.mainloop()
