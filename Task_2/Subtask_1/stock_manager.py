def show(dict):
    for idx, (item, qty) in enumerate(dict.items(), 1):
        print(f"{idx}. {item}: {qty}")

def lstock():
    dict = {}
    try:
        with open("stock.txt", "r") as file:
            for line in file:
                parts = line.split(",")
                item = parts[0].strip().lower()
                qty = int(parts[1].strip())
                dict[item] = qty
    except (OSError, ValueError, IndexError):
        print("Error: stock.txt missing or corrupted")
    return dict

def getkey(dict, val):
    keys = list(dict.keys())
    if val.isdigit():
        idx = int(val) - 1
        if 0 <= idx < len(keys):
            return keys[idx]
    return val

def action(choice, dict):
    if choice == "1":
        show(dict)
        inp = input('Enter stock name or id: ').strip().lower()
        key = getkey(dict, inp)
        try:
            amt = int(input(f"Enter amount to add to {key}: "))
            if amt < 0:
                print("Error: amount cannot be negative")
                return
        except ValueError:
            print("Invalid amount")
            return
        if key in dict:
            dict[key] += amt
        else:
            dict[key] = amt
    elif choice == "2":
        show(dict)
        inp = input('Enter stock name or id: ').strip().lower()
        keys = list(dict.keys())
        key = None
        if inp.isdigit():
            idx = int(inp) - 1
            if 0 <= idx < len(keys):
                key = keys[idx]
        elif inp in dict:
            key = inp
        if not key or key not in dict:
            print("Invalid stock item, pls try again")
            return
        try:
            amt = int(input(f"Enter amount to remove from {key}: "))
            if amt < 0:
                print("Error: amount cannot be negative")
                return
        except ValueError:
            print("Invalid amount")
            return
        if dict[key] - amt < 0:
            print("Error: Remaining stock cannot be less than 0")
        elif dict[key] - amt == 0:
            del dict[key]
        else:
            dict[key] -= amt
    elif choice == "3":
        show(dict)
    elif choice == "4":
        with open("stock.txt", "w") as file:
            for item, qty in dict.items():
                file.write(f"{item},{qty}\n")
        print("Changes saved to stock.txt")

dict = lstock()

while True:
    choice = input("pls enter numbers 1 through 4\n1 : ADD STOCK\n2 : REMOVE STOCK\n3 : SHOW CONTENTS\n4 : EXIT\n").strip()
    if choice in ["1", "2", "3", "4"]:
        action(choice, dict)
        if choice == "4":
            break
    else:
        print("Invalid choice, pls select 1, 2, 3, or 4")