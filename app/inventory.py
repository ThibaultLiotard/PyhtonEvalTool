import tkinter as tk
from tkinter import ttk, Label, Entry, Button, Toplevel, Frame, Listbox, filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import random
from datetime import datetime
from enum import Enum

# Enumerations for weapon effects and types
class WeaponEffect(Enum):
    NONE = "None"
    FIRE = "Fire"
    POISON = "Poison"

class WeaponType(Enum):
    MELEE = "Melee"
    RANGED = "Ranged"

# Utility functions
def generate_id():
    """Generate a unique identifier for a new item."""
    current_time = datetime.now()
    return current_time.strftime("%Y%m%d%H%M%S%f")

def roll_dice(dice_type):
    """Roll a dice of the specified type (e.g., '3d4' for three four-sided dice)."""
    number, sides = map(int, dice_type.split('d'))
    return sum(random.randint(1, sides) for _ in range(number))



# Equipment UI functions
def setup_weapon_tab(tab, equipment_list, image_label):
    # Weapon Name
    weapon_name_var = tk.StringVar()
    Label(tab, text='Name :').grid(row=0, column=0, sticky='e')
    Entry(tab, textvariable=weapon_name_var).grid(row=0, column=1)

    # Weapon Description
    weapon_description_var = tk.StringVar()
    Label(tab, text='Description :').grid(row=1, column=0, sticky='e')
    Entry(tab, textvariable=weapon_description_var).grid(row=1, column=1)

    # Weapon ID
    weapon_id_label = Label(tab, text=generate_id())
    Label(tab, text='ID :').grid(row=2, column=0, sticky='e')
    weapon_id_label.grid(row=2, column=1)

    # Weapon Base Power
    weapon_power_var = tk.StringVar()
    Label(tab, text='Base Power :').grid(row=3, column=0, sticky='e')
    Entry(tab, textvariable=weapon_power_var).grid(row=3, column=1)

    # Button to randomize weapon power
    Button(tab, text='Random', command=lambda: weapon_power_var.set(roll_dice('3d4'))).grid(row=3, column=2)

    # Weapon Effect
    weapon_effect_var = tk.StringVar()
    Label(tab, text='Effect :').grid(row=4, column=0, sticky='e')
    Combobox(tab, textvariable=weapon_effect_var, values=[e.value for e in WeaponEffect]).grid(row=4, column=1)

    # Weapon Type
    weapon_type_var = tk.StringVar()
    Label(tab, text='Type :').grid(row=5, column=0, sticky='e')
    Combobox(tab, textvariable=weapon_type_var, values=[t.value for t in WeaponType]).grid(row=5, column=1)

    # Add Weapon Button
    add_weapon_button = Button(tab, text='Add Weapon', command=lambda: add_weapon(
        weapon_name_var, weapon_description_var, weapon_id_label.cget("text"),
        weapon_power_var, weapon_effect_var, weapon_type_var, equipment_list))
    add_weapon_button.grid(row=6, column=1, sticky='e')

    # Image path
    weapon_image_var = tk.StringVar()
    Label(tab, text='Image Path :').grid(row=7, column=0, sticky='e')
    Entry(tab, textvariable=weapon_image_var).grid(row=7, column=1)

    # Open Image Button
    open_image_button = Button(tab, text="Open Image", command=lambda: open_image(weapon_image_var, image_label))
    open_image_button.grid(row=7, column=2)

# Equipment UI functions
def setup_tab(tab, equipment_list, tab_name, fields):
    for i, (field_name, dice_type) in enumerate(fields.items()):
        var = tk.StringVar()
        Label(tab, text=field_name).grid(row=i, column=0, sticky='e')
        Entry(tab, textvariable=var).grid(row=i, column=1, sticky='w')
        if dice_type:
            var.set(dice_type)  # Preset the dice type if provided

    # Add item button
    add_item_button = Button(tab, text=f'Add {tab_name}', command=lambda: add_item(tab_name, fields, equipment_list))
    add_item_button.grid(row=len(fields), column=0, columnspan=2)

def setup_armor_tab(tab, equipment_list):
    # Armor Name
    armor_name_var = tk.StringVar()
    Label(tab, text='Name :').grid(row=1, column=0, sticky='e')
    Entry(tab, textvariable=armor_name_var).grid(row=1, column=1, sticky='e')

    # Armor Description
    armor_description_var = tk.StringVar()
    Label(tab, text='Description :').grid(row=2, column=0, sticky='e')
    Entry(tab, textvariable=armor_description_var).grid(row=2, column=1, sticky='e')

    # Armor Image Path
    armor_image_var = tk.StringVar()
    Label(tab, text='Image Path :').grid(row=3, column=0, sticky='e')
    Entry(tab, textvariable=armor_image_var).grid(row=3, column=1, sticky='e')

    # Armor Base Defense (Random 2D4)
    armor_defense_var = tk.StringVar()
    Label(tab, text='Base Defense :').grid(row=4, column=0, sticky='e')
    Entry(tab, textvariable=armor_defense_var).grid(row=4, column=1, sticky='e')

    # Armor Resistance Options
    armor_resistance_var = tk.StringVar()
    Label(tab, text='Resistance :').grid(row=5, column=0, sticky='e')
    ttk.Combobox(tab, textvariable=armor_resistance_var, values=['None', 'Fire', 'Poison']).grid(row=5, column=1, sticky='e')

    # Add Armor Button
    add_armor_button = Button(tab, text='Add Armor', #command=lambda: add_armor(
        #armor_name_var, armor_description_var, armor_image_var, armor_defense_var, armor_resistance_var, equipment_list)
    )
    add_armor_button.grid(row=6, column=0, sticky='e')


def setup_potion_tab(tab, equipment_list):
    # Potion Name
    potion_name_var = tk.StringVar()
    Label(tab, text='Name').grid(row=1, column=0, sticky='e')
    Entry(tab, textvariable=potion_name_var).grid(row=1, column=1, sticky='e')

    # Potion Description
    potion_description_var = tk.StringVar()
    Label(tab, text='Description').grid(row=2, column=0, sticky='e')
    Entry(tab, textvariable=potion_description_var).grid(row=2, column=1, sticky='e')

    # Potion Image Path
    potion_image_var = tk.StringVar()
    Label(tab, text='Image Path').grid(row=3, column=0, sticky='e')
    Entry(tab, textvariable=potion_image_var).grid(row=3, column=1, sticky='e')

    # Potion Power (Random 1D6)
    potion_power_var = tk.StringVar()
    Label(tab, text='Power').grid(row=4, column=0, sticky='e')
    Entry(tab, textvariable=potion_power_var).grid(row=4, column=1, sticky='e')

    # Potion Effect Options
    potion_effect_var = tk.StringVar()
    Label(tab, text='Effect  ').grid(row=5, column=0, sticky='e')
    ttk.Combobox(tab, textvariable=potion_effect_var, values=['None', 'Heal', 'Fire', 'Poison']).grid(row=5, column=1, sticky='e')

    # Add Potion Button
    add_potion_button = Button(tab, text='Add Potion', #command=lambda: add_potion(
        #potion_name_var, potion_description_var, potion_image_var, potion_power_var, potion_effect_var, equipment_list)
                               )
    add_potion_button.grid(row=6, column=1, sticky='e')


def setup_special_item_tab(tab, equipment_list):
    # Special Item Name
    special_item_name_var = tk.StringVar()
    Label(tab, text='Name').grid(row=1, column=0, sticky='e')
    Entry(tab, textvariable=special_item_name_var).grid(row=1, column=1)

    # Special Item Description
    special_item_description_var = tk.StringVar()
    Label(tab, text='Description').grid(row=2, column=0, sticky='e')
    Entry(tab, textvariable=special_item_description_var).grid(row=2, column=1)

    # Special Item Image Path
    special_item_image_var = tk.StringVar()
    Label(tab, text='Image Path').grid(row=3, column=0, sticky='e')
    Entry(tab, textvariable=special_item_image_var).grid(row=3, column=1)

    # Weapon ID
    weapon_id_label = Label(tab, text=generate_id())
    Label(tab, text='ID').grid(row=4, column=0, sticky='e')
    weapon_id_label.grid(row=4, column=1)

    # Add Special Item Button
    add_special_item_button = Button(tab, text='Add Special Item', #command=lambda: add_special_item(
        #special_item_name_var, special_item_description_var, special_item_image_var, equipment_list)
                                     )
    add_special_item_button.grid(row=6, column=1, sticky='e')



def add_weapon(name_var, description_var, weapon_id, power_var, effect_var, type_var, equipment_list):
    item_id = weapon_id
    weapon = {
        'id': item_id,
        'name': name_var.get(),
        'description': description_var.get(),
        'power': power_var.get(),
        'effect': effect_var.get(),
        'type': type_var.get()
    }
    # Logic to add the weapon to the inventory and update the list goes here

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

def create_equipment_ui(root):
    # Main frame for the equipment interface
    main_frame = Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Frame for the list and buttons, with adjusted width
    list_frame = Frame(main_frame, width=200, bg='grey')
    list_frame.pack(side='left', fill='y', padx=8, pady=10)

    # Button to add a new item
    add_button = Button(list_frame, text='New Character')
    add_button.pack(side='top', pady=10)

    # List of equipment, with adjusted width
    equipment_list = Listbox(list_frame, width=30)
    equipment_list.pack(side='top', fill='both', expand=True)

    # Delete button
    delete_button = Button(list_frame, text='Delete')
    delete_button.pack(side='bottom', pady=10)

    # Area for the tabs for configuring items
    tab_control = ttk.Notebook(main_frame)
    tab_control.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    # Image label
    image_label_frame = Frame(main_frame, width=200, height=400)
    image_label_frame.pack(side='right', fill='both', expand=True)

    image_label = Label(image_label_frame)
    image_label.pack(fill='both', expand=True)

    # Tabs for different item categories
    weapon_tab = Frame(tab_control)


    weapon_tab = Frame(tab_control)
    armor_tab = Frame(tab_control)
    potion_tab = Frame(tab_control)
    special_item_tab = Frame(tab_control)

    setup_weapon_tab(weapon_tab, equipment_list, image_label)
    setup_armor_tab(armor_tab, equipment_list)
    setup_potion_tab(potion_tab, equipment_list)
    setup_special_item_tab(special_item_tab, equipment_list)

    tab_control.add(weapon_tab, text='Weapons')
    tab_control.add(armor_tab, text='Armor')
    tab_control.add(potion_tab, text='Potion')
    tab_control.add(special_item_tab, text='Special Item')
    # Continue adding tabs for armor, consumables, and special items

def open_equipment_page(window):
    equipment_window = Toplevel(window)
    equipment_window.title("Equipment Creation")
    equipment_window.geometry("800x600")

    create_equipment_ui(equipment_window)

    equipment_window.mainloop()
