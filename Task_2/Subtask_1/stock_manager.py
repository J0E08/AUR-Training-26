stock = {}
num = 0
try:
    with open("stock.txt", "r") as f:
        for line in f:
            if line.strip():
                item, quantity = line.strip().split(",")
                stock[item.strip().lower()] = int(quantity.strip())
except (FileNotFoundError, ValueError):
    print("Warning: stock.txt not found or corrupted.")
act = {
    "1" : "Add stock",
    "2" : "Remove stock",
    "3" : "Display stock",
    "4" : "Exit"
    }
def get_item_list():
    return list(stock.keys())
def show_stock():
    item_list = get_item_list()
    for idx, name in enumerate(item_list, start=1):
        print(f"{idx}. {name}: {stock[name]}")
def show_actions():
    for key, value in act.items():
        print(f"{key}. {value}")
def check_key(user_input):
    item_list = get_item_list()
    if user_input.isdigit():
        idx = int(user_input) - 1
        if 0 <= idx < len(item_list):
            return item_list[idx]
    else:
        cleaned = user_input.lower().strip()
        if cleaned in stock:
            return cleaned
    return None
def actions(num):
    while True:
        while True:
            show_actions()
            num = int(input("pls enter a number respective to action required\n"))
            if(num>0 and num<5):
                break
        if num == 1:
            while True:
                show_stock()
                item = input("pls enter the item's name\n").lower().strip()
                quantity = int(input(f"pls enter the quantity of the stock --> {item}\n"))
                if item.isdigit():
                    idx = int(item) - 1
                    item_list = get_item_list()
                    if 0 <= idx < len(item_list):
                        real_key = item_list[idx]
                        print("item already registered!\nquantity value changed\n")
                        stock[real_key] += quantity
                    else:
                        print("Invalid index!\n")
                    print(stock)
                    break
                if item in stock:
                    print("item already registered!\nquantity value changed\n")
                    stock[item] += quantity
                    print(stock)
                    break
                else:
                    stock[item] = quantity
                    print(stock) 
                    break
            continue
        if num == 2:
            show_stock()
            rmv = input("pls enter ID or name of item u wish to remove\n")
            key = check_key(rmv)
            if not key:
                print("item not found\n")
                continue
            qnty = int(input("pls enter the value of quantity u wish to remove\n"))
            if stock[key] - qnty < 0:
                while True:
                    qnty = int(input("quantity value requested for removal is greater than available\npls try again!\n"))
                    if stock[key] - qnty >= 0:
                        break
            stock[key] -= qnty
            continue
        if num == 3:
            show_stock()
            continue
        if num == 4:
            with open("stock.txt", "w") as f:
                for key, val in stock.items():
                    f.write(f"{key},{val}\n")
            print("changes saved!\n")
            break
actions(num)
