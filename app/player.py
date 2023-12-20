from tkinter import Label, Entry, Toplevel, Listbox, Button, Frame, Canvas
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from enum import Enum

class player_race(Enum): 
    HUMAN = "Human"
    ELF = "Elf"
    ORC = "Orc"

class player_class(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    THIEF = "Thief"

def open_player_page(window):
    player_window = Toplevel(window)
    player_window.title("Player Page")
    player_window.minsize(800, 600)

    list_frame = Frame(player_window, width=200, bg='grey')
    list_frame.pack(side='left', fill='y', padx=5, pady=5)

    players_listbox = Listbox(list_frame)
    players_listbox.pack(side='top', fill='both', expand=True)

    # Add name to player for test
    players_listbox.insert('end', 'Player 1')
    players_listbox.insert('end', 'Player 2')
    players_listbox.insert('end', 'Player 3')

    details_frame = Frame(player_window)
    details_frame.pack(side='right', expand=True, fill='both', padx=5, pady=5)

    # Set Player Name
    Label(details_frame, text="Name :").grid(row=0, column=0, sticky='e')
    name_entry = Entry(details_frame)
    name_entry.grid(row=0, column=1, pady=5)

    # Set Player Race
    Label(details_frame, text="Race :").grid(row=1, column=0, sticky='e')
    race_combobox = Combobox(details_frame, values=[race.value for race in player_race])
    race_combobox.grid(row=1, column=1, pady=5)
    
    # Set Player Class
    Label(details_frame, text="Class :").grid(row=2, column=0, sticky='e')
    class_combobox = Combobox(details_frame, values=[classe.value for classe in player_class])
    class_combobox.grid(row=2, column=1, pady=5)

    # Frame for player image
    image_frame = Frame(details_frame, height=200, width=100, bd=2, relief='sunken')
    image_frame.grid(row=0, column=2, rowspan=10, padx=10, pady=5, sticky='ns')

    
    image_path = 'path_to_player_image.jpg'
    pil_image = Image.open(image_path)
    player_image = ImageTk.PhotoImage(pil_image)
    image_label = Label(image_frame, image=player_image)
    image_label.image = player_image  # keep a ref
    image_label.pack(fill='both', expand=True)
