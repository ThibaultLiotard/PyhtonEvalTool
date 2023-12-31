from tkinter import filedialog, Label, Entry, Toplevel, Listbox, Button, Frame
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from enum import Enum
import random
from datetime import datetime
import json

global image_path, name_entry, race_combobox, class_combobox, stat_entries, id_label, image_label, players_listbox


class player_race(Enum): 
    HUMAN = "Human"
    ELF = "Elf"
    ORC = "Orc"

class player_class(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    THIEF = "Thief"


def update_player_listbox():
    global players_listbox
    try:
        with open("characters.json", "r") as file:
            characters = json.load(file)

        players_listbox.delete(0, 'end')  # Clean current list
        for player_id, character in characters.items():
            players_listbox.insert('end', f"{character['name']} (ID: {player_id})")
    except FileNotFoundError:
        print("Character file not found.")


def save_character(name, race, player_class, stats, player_id, image_path):

    character = {
        "id": player_id,
        "name": name,
        "race": race,
        "class": player_class,
        "stats": stats,
        "image": image_path
    }
    try:
        with open("characters.json", "r") as file:
            characters = json.load(file)
    except FileNotFoundError:
        characters = {}

    characters[player_id] = character

    with open("characters.json", "w") as file:
        json.dump(characters, file, indent=4)

    update_player_listbox()


def load_character(player_id):
    
    global name_entry, race_combobox, class_combobox, stat_entries, id_label, image_label, players_listbox
    try:
        with open("characters.json", "r") as file:
            characters = json.load(file)
        character = characters.get(player_id)

        if character:
            name_entry.delete(0, 'end')
            name_entry.insert(0, character["name"])
            race_combobox.set(character["race"])
            class_combobox.set(character["class"])
            id_label.config(text=character["id"])

            for stat_entry, stat_value in zip(stat_entries, character["stats"]):
                stat_entry.config(state='normal')
                stat_entry.delete(0, 'end')
                stat_entry.insert(0, stat_value)
                stat_entry.config(state='readonly')

            image_path = character.get("image")
            if image_path:  # If a path has been chosen
                pil_image = Image.open(image_path)

                # Get the dimensions of the image
                original_width, original_height = pil_image.size

                # Desired size
                max_width, max_height = 300, 500

                # Calculate the correct aspect ratio
                ratio = min(max_width/original_width, max_height/original_height)
                new_width, new_height = int(original_width * ratio), int(original_height * ratio)

                # Resize the image
                resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Convert to PhotoImage
                player_image = ImageTk.PhotoImage(resized_image)

                # Update the label
                image_label.config(image=player_image)
                image_label.image = player_image  # Keep a reference
            else:
                image_label.config(image=None)
                image_label.image = None
    except FileNotFoundError:
        print("Character file not found.")



def on_player_select(event):
    # Get the index of the selected item
    selected_index = event.widget.curselection()
    if not selected_index:
        return

    # Get the player ID from the selected item
    selected_text = event.widget.get(selected_index)
    player_id = selected_text.split(" (ID: ")[-1].rstrip(")")

    # Load the character data
    load_character(player_id)


def delete_character(player_id):
    global players_listbox
    try:
        with open("characters.json", "r") as file:
            characters = json.load(file)

        if player_id in characters:
            del characters[player_id]
            
            with open("characters.json", "w") as file:
                json.dump(characters, file, indent=4)
            update_player_listbox()
            create_new_character()

    except FileNotFoundError:
        print("Character file not found.")


def delete_selected_character():
    global players_listbox
    selection = players_listbox.curselection()

    if not selection:
        return
    
    selected_item = players_listbox.get(selection)
    player_id = selected_item.split(" (ID: ")[-1].rstrip(")")

    delete_character(player_id)


def create_new_character():
    global name_entry, race_combobox, class_combobox, stat_entries, id_label, image_label, image_path, players_listbox
    # Reset input fields
    name_entry.delete(0, 'end')
    race_combobox.set('')
    class_combobox.set('')

    # Clear current image
    image_label.config(image=None)
    image_label.image = None
    image_path = ""

    for entry in stat_entries:
        entry.config(state='normal')
        entry.delete(0, 'end')
        entry.config(state='readonly')

    # Generate a new ID
    new_id = generate_id()
    id_label.config(text=new_id)

    # Reset statistics
    randomize_stats(stat_entries)
    update_player_listbox()



def generate_id():
    """ Generates a unique ID based on the current date and time """
    current_time = datetime.now()
    return current_time.strftime("%Y%m%d%H%M%S%f")

def open_image(player_window):

    # Open dialog box to choose a file
    global image_path, image_label
    image_path = filedialog.askopenfilename()

    # Keep character window in front
    player_window.attributes('-topmost', True)
    player_window.attributes('-topmost', False) 

    if image_path:  # If a path has been chosen
        pil_image = Image.open(image_path)

        # Get the dimensions of the image
        original_width, original_height = pil_image.size

        # Desired size
        max_width, max_height = 300, 500

        # Calculate the correct aspect ratio
        ratio = min(max_width/original_width, max_height/original_height)
        new_width, new_height = int(original_width * ratio), int(original_height * ratio)

        # Resize the image
        resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to PhotoImage
        player_image = ImageTk.PhotoImage(resized_image)

        # Update the label
        image_label.config(image=player_image)
        image_label.image = player_image  # Keep a reference
    

    

def roll_3d6():
    """ Simulates the roll of 3 6-sided dice """
    return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)

def randomize_stats(stat_entries):
     for entry in stat_entries:
        entry.config(state='normal')  # Make the entry editable by the program
        entry.delete(0, 'end')
        entry.insert(0, roll_3d6())
        entry.config(state='readonly')  # Make the entry read-only for the user



def create_new_player(player_window):
    global name_entry, race_combobox, class_combobox, stat_entries, id_label, image_label, players_listbox, image_path
    list_frame = Frame(player_window, width=600, bg='grey')
    list_frame.pack(side='left', fill='y', padx=5, pady=5)

    new_character_button = Button(list_frame, text="New Character", command=lambda: create_new_character())
    new_character_button.pack(pady=5)

    players_listbox = Listbox(list_frame)
    players_listbox.pack(side='top', fill='both', expand=True)
    update_player_listbox()
    players_listbox.bind('<<ListboxSelect>>', lambda event: on_player_select(event))

    delete_button = Button(list_frame, text="Delete", command=lambda: delete_selected_character())
    delete_button.pack(pady=5)

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

    # Générer et afficher l'ID du joueur
    player_id = generate_id()
    Label(details_frame, text="Player ID:").grid(row=3, column=0, sticky='e')
    id_label = Label(details_frame, text=player_id)
    id_label.grid(row=3, column=1, pady=5)

    # Add space between "Class" and "Statistics"
    Label(details_frame, text="").grid(row=4, column=3, pady=10) 
    Label(details_frame, text="").grid(row=4, column=4, pady=10) 

    Label(details_frame, text="statistics :").grid(row=5, column=0, sticky='e')
    

    # Frame for player image
    image_frame = Frame(details_frame, height=400, width=200, bd=2, relief='sunken')
    image_frame.grid(row=0, column=5, rowspan=10, padx=10, pady=5, sticky='nesw')

    image_label = Label(image_frame)
    image_label.pack(side='left',fill='both', expand=True)

    open_image_button = Button(details_frame, text="Open Image", command=lambda: open_image(player_window))
    open_image_button.grid(row=11, column=5, sticky='e')



    stats = ["Force", "Dextérité", "Intelligence", "Chance", "Points de vie"]
    stat_entries = []
    for i, stat in enumerate(stats):
        Label(details_frame, text=f"{stat} :").grid(row=7+i, column=0, sticky='e')
        stat_entry = Entry(details_frame, readonlybackground='white', fg='black')
        stat_entry.grid(row=7+i, column=1, pady=5)
        stat_entry.config(state='readonly')  # Initialize as read-only
        stat_entries.append(stat_entry)

    # Button to randomly generate statistics
    random_button = Button(details_frame, text="Random", command=lambda: randomize_stats(stat_entries))
    random_button.grid(row=5, column=2)


    # Generate random initial statistics
    randomize_stats(stat_entries)

 
    Label(details_frame, text="").grid(row=29, column=2, pady=30)

    # Save button at bottom middle
    #image_path = open_image(image_label, player_window)
    
    save_button = Button(details_frame, text="Save", command=lambda: save_character(name_entry.get(), race_combobox.get(), class_combobox.get(), [entry.get() for entry in stat_entries], id_label.cget("text"),image_path))
    save_button.grid(row=30, column=2)




    
 
    
def open_player_page(window):
    player_window = Toplevel(window)
    player_window.title("Player Page")
    player_window.geometry("800x600")
    player_window.minsize(800, 600)
    create_new_player(player_window)