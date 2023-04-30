import re
import json
import os
import pyperclip

filename = "deliver_items.json"
data = """
Deliver 3 Junk Scrap
Deliver 5 Gunpowder
Deliver 5 Metal Sheets
Deliver a Silver Coin
Deliver 8 Chemicals
Deliver 3 Transmitters
Deliver 3 Motor Oil cans
Deliver 3 Ration Crates
Deliver 10 Industrial Paper
Deliver 3 Biscuit Tins
Craft and Deliver 5 Folded Commando Backpacks
Deliver the Commando Cap
Craft and Deliver 3 M1 Flak Rigs
Deliver 9 Toolkits
Deliver the Nuclear Material
Deliver 12 Methamphetamine
Deliver 5 Mosin Obrez Pistols
Deliver 3 U.A. Intel Documents
Deliver 1 Gold Bullion
Deliver 3 Medical Crates
"""

def create_items_dict():
    items_to_deliver = {}

    for line in data.splitlines():
        match = re.match(r'(?:Craft and )?Deliver (a|the|(\d+)) (.+)', line)
        if match:
            quantity = match.group(2) if match.group(2) else 1
            item = match.group(3)
            items_to_deliver[item] = {'required': int(quantity), 'current': 0}

    return items_to_deliver

def load_items_from_file():
    with open(filename, "r") as file:
        items_to_deliver = json.load(file)
    return items_to_deliver

def save_items_to_file(items_to_deliver):
    with open(filename, "w") as file:
        json.dump(items_to_deliver, file)

def update_item_quantity(items_to_deliver, item, new_quantity):
    items_to_deliver[item]['current'] = new_quantity
    
def export_needed_items(items_to_deliver):
    needed_items = []
    for item, quantities in items_to_deliver.items():
        if quantities['current'] < quantities['required']:
            needed_items.append(f"{item}: {quantities['current']} / {quantities['required']}")

    needed_items_str = '\n'.join(needed_items)
    pyperclip.copy(needed_items_str)
    print("Needed items have been copied to your clipboard.")

def menu(items_to_deliver):
    while True:
        print("\nMenu:")
        print("1. View items")
        print("2. View needed items")
        print("3. Update item quantity")
        print("4. Export needed items to clipboard")
        print("5. Save and exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            for item, quantities in items_to_deliver.items():
                print(f"{item}: {quantities['current']} / {quantities['required']}")
        elif choice == "2":
            for item, quantities in items_to_deliver.items():
                if quantities['current'] < quantities['required']:
                    print(f"{item}: {quantities['current']} / {quantities['required']}")
                    
        elif choice == "3":
            item = input("Enter the item name: ")
            if item in items_to_deliver:
                new_quantity = int(input(f"Enter the new quantity for {item}: "))
                update_item_quantity(items_to_deliver, item, new_quantity)
                print(f"Updated {item} quantity to {new_quantity}.")
            else:
                print("Invalid item name. Please try again.")
                
        elif choice == "4":
            export_needed_items(items_to_deliver)

        elif choice == "5":
            save_items_to_file(items_to_deliver)
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    if not os.path.exists(filename):
        items_to_deliver = create_items_dict()
        save_items_to_file(items_to_deliver)
    else:
        items_to_deliver = load_items_from_file()

    menu(items_to_deliver)
