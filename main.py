import sqlite3
from pathlib import Path
import os
import time
from datetime import datetime
import string
import random
import math
import pyqrcode # pip install pyqrcode pypng

current_path = Path(os.path.dirname(os.path.abspath(__file__)))
db_path = Path(current_path / "data.db").absolute()

if not os.path.exists(db_path):
    with open(db_path, 'wb') as f:
        pass

conn = sqlite3.connect(db_path)
cur = conn.cursor()


def create_required_tables():
    """
    Creates the required tables if they do not exist.
    """
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unique_id TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS receipt (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buyer_name TEXT,
            secret_id TEXT,
            date TIMESTAMP,
            total FLOAT,
            description TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS shop (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price FLOAT,
            quantity INTEGER
        )
    """)
create_required_tables()



def generate_unique_id():
    '''Generates a random unique identifier.'''
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

def clear_console():
    '''Clear the console.'''
    os.system('cls' if os.name == 'nt' else 'clear')



def print_info():
    '''Prints the information about the application'''
    clear_console()
    print("""
    ********************************
    **      WELCOME TO PySHOP     **
    ********************************
    **   - Dev: Rudransh Joshi    **    
    ********************************

    ================================
    Select an option:
    ================================
    1. Register a new user.
    2. Show all users.
    3. Delete a user.
    4. Add an item to the shop.
    5. Delete an item from the shop.
    6. Show all items from shop.
    7. Update an item in the shop.
    8. Buy items from the shop.
    9. Show total sales.
    10. Exit.


    """)
    select_option()


def select_option():
    '''Allows user to select an option and call the desired function.'''
    option = int(input('>>> Select an option [1-10]:\t'))
    clear_console()
    if option > 10 or option < 1:
        print("Invalid option. Try again.\n")
        time.sleep(1)
        clear_console()
        print_info()
    if option == 1:
        register_user()
    elif option == 2:
        show_users()
    elif option == 3:
        delete_user()
    elif option == 4:
        add_item()
    elif option == 5:
        delete_item()
    elif option == 6:
        show_items()
    elif option == 7:
        update_item()
    elif option == 8:
        buy_items()
    elif option == 9:
        show_sales()
    elif option == 10:
        exit()


def register_user():
    '''Registers a user in the database.'''
    clear_console()
    print("""
    ================================
    Register a new user.
    ================================
    """)
    name = input("\t>>> Name:\t")
    email = input("\t>>> Email:\t")
    phone = input("\t>>> Phone:\t")
    address = input("\t>>> Address:\t")
    unique_id = generate_unique_id()
    # Keep generating unique_id until it is actually unique and doesn't exists in db already
    while True:
        cur.execute("SELECT * FROM users WHERE unique_id = ?", (unique_id,))
        if not cur.fetchone():
            break
        unique_id = generate_unique_id()

    cur.execute("""
        INSERT INTO users (name, email, phone, address, unique_id)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, phone, address, unique_id))
    conn.commit()
    print(f"\n\tUser registered successfully.\n\tUnique User ID:\t | {unique_id} | <-- You will need to provide this unique ID while shopping with us.\n")
    another = int(input("Register another user?\n>>> Enter 1 for Yes, 2 for No:\t"))
    if another == 1:
        register_user()
    else:
        time.sleep(1)
        print_info()


def show_users():
    '''Shows the users present in the database in a tabular form.'''
    clear_console()
    text = """
    ================================
    Show all users.
    ================================
    """
    print(text)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    records_per_page = 5
    pages = math.ceil(len(users) / records_per_page)
    for page in range(1, pages + 1):
        users_to_show = users[(page-1)*records_per_page: (page-1)*records_per_page+records_per_page]
        print(f"\tPage {page} of {pages}\n\t----------------\n")
        # Printing Header
        print("\tID\tUnique ID\t\tName\t\tEmail\t\t\t\t    Phone\n")
        for i in users_to_show:
            print(f"\t{i[0]}\t{i[1]}\t\t{i[2]}\t\t{i[3]}\t\t\t    {i[4]}")
        
        print("\n\t----------------\n\n")
        another = int(input("1. Next Page\t2. Jump to Page 1\t3. Back to main screen\n>>> Select an option:\t"))
        if another == 1:
            clear_console()
            print(text)
            continue
        elif another == 2:
            show_users()
        elif another == 3:
            break
    
    print_info()


def delete_user():
    '''Deletes a user from the database.'''
    clear_console()
    print("""
    ================================
    Delete a user.
    ================================
    """)
    unique_id = input("\t>>> Enter unique ID of the user you want to delete:\t").upper().strip()
    cur.execute("SELECT * FROM users WHERE unique_id = ?", (unique_id,))
    data = cur.fetchone()
    if data:
        name = data[2]
        cur.execute("DELETE FROM users WHERE unique_id = ?", (unique_id,))
        conn.commit()
        print(f"\n\tUser [{name}] deleted successfully.\n")
    else:
        print(f"\n\tUser with unique id {unique_id} does not exist.\n")
    another = int(input("Delete another user?\n>>> Enter 1 for Yes, 2 for No:\t"))
    if another == 1:
        delete_user()
    else:
        time.sleep(1)
        print_info()


def add_item():
    '''Adds a new item for the shop to the database.'''
    clear_console()
    print("""
    ================================
    Add an item to the shop.
    ================================
    """)
    name = input("\t>>> Name:\t").upper()
    price = float(input("\t>>> Price:\t"))
    quantity = int(input("\t>>> Quantity:\t"))
    cur.execute("""
        INSERT INTO shop (name, price, quantity)
        VALUES (?, ?, ?)
    """, (name, price, quantity))
    conn.commit()
    print(f"\n\tItem [{name}] added successfully.\n")
    another = int(input("Add another item?\n>>> Enter 1 for Yes, 2 for No:\t"))
    if another == 1:
        add_item()
    else:
        time.sleep(1)
        print_info()


def delete_item():
    '''Deletes an item in the shop from the database.'''
    clear_console()
    print("""
    ================================
    Delete an item from the shop.
    ================================
    """)
    item_id = int(input("\t>>> Enter ID of item you want to delete:\t"))
    cur.execute("SELECT * FROM shop WHERE id = ?", (item_id,))
    data = cur.fetchone()
    if data:
        name = data[1]
        cur.execute("DELETE FROM shop WHERE id = ?", (item_id,))
        conn.commit()
        print(f"\n\tItem [{name}] deleted successfully.\n")
    else:
        print(f"\n\tItem with id {item_id} does not exist.\n")
    another = int(input("Delete another item?\n>>> Enter 1 for Yes, 2 for No:\t"))
    if another == 1:
        delete_item()
    else:
        time.sleep(1)
        print_info()
        

def show_items():
    '''Shows the items present in the shop from the database in a tabular form.'''
    clear_console()
    text = """
    ================================
    Show all items.
    ================================
    """
    print(text)
    cur.execute("SELECT * FROM shop")
    items = cur.fetchall()
    records_per_page = 5
    pages = math.ceil(len(items) / records_per_page)
    for page in range(1, pages + 1):
        items_to_show = items[(page-1)*records_per_page: (page-1)*records_per_page+records_per_page]
        print(f"\tPage {page} of {pages}\n\t----------------\n")
        # Printing Header
        print("\tID\tName\t\t\tPrice\t\t\t\tQuantity\n")
        for i in items_to_show:
            print(f"\t{i[0]}\t{i[1]}\t\t\t{i[2]}\t\t\t\t{i[3]}")
        
        print("\n\t----------------\n\n")
        another = int(input("1. Next Page\t2. Jump to Page 1\t3. Back to main screen\n>>> Select an option:\t"))
        if another == 1:
            clear_console()
            print(text)
            continue
        elif another == 2:
            show_items()
        elif another == 3:
            break
    
    print_info()


def update_item():
    '''Updates an item from shop in the database'''
    clear_console()
    print("""
    ================================
    Update an item.
    ================================
    """)
    item_id = int(input("\t>>> Enter ID of item you want to update:\t"))
    cur.execute("SELECT * FROM shop WHERE id = ?", (item_id,))
    data = cur.fetchone()
    if data:
        print(f"\tName: {data[1]}\tPrice: {data[2]}\tQuantity: {data[3]}\n")
        name = data[1]
        price = float(input("\t>>> New Price:\t"))
        quantity = int(input("\t>>> New Quantity:\t"))
        cur.execute("""
            UPDATE shop
            SET price = ?, quantity = ?
            WHERE id = ?
        """, (price, quantity, item_id))
        conn.commit()
        print(f"\n\tItem [{name}] updated successfully.\n")
    else:
        print(f"\n\tItem with id {item_id} does not exist.\n")
    another = int(input("Update another item?\n>>> Enter 1 for Yes, 2 for No:\t"))
    if another == 1:
        update_item()
    else:
        time.sleep(1)
        print_info()


def buy_items():
    '''Allows user to buy items from the shop and generates a receipt of the purchase and a qr code.'''
    clear_console()
    print("""
    ================================
    Buy items from the shop.
    ================================
    """)
    cart = {}
    unique_id = input("\t>>> Enter unique ID of the user:\t").upper()
    cur.execute("SELECT * FROM users WHERE unique_id = ?", (unique_id,))
    if not cur.fetchone():
        print(f"\n\tUser with unique id [{unique_id}] does not exist.\n")
        time.sleep(1)
        print_info()
    else:
        cur.execute("SELECT * FROM users WHERE unique_id = ?", (unique_id,))
        data = cur.fetchone()
        name = data[2]
        address = data[5]
        username = name
        print(f"\n\tUser [{name}] selected.\n")
        cur.execute("SELECT * FROM shop")
        items = cur.fetchall()
        print("\tID\tName\t\t\tPrice\t\t\t\tQuantity\n")
        for i in items:
            print(f"\t{i[0]}\t{i[1]}\t\t\t{i[2]}\t\t\t\t{i[3]}")

        stop = False
        while not stop:
            item_id = int(input("\n\t>>> Enter ID of item you want to buy (Enter '123456' to checkout):\t"))
            cur.execute("SELECT * FROM shop WHERE id = ?", (item_id,))
            data = cur.fetchone()
            if data:
                qty = int(input("\t>>> Enter quantity:\t"))
                name = data[1]
                price = data[2]
                quantity = data[3]
                if quantity > 0 and quantity >= qty:
                    cur.execute("""
                        UPDATE shop
                        SET quantity = ?
                        WHERE id = ?
                    """, (quantity-qty, item_id))
                    conn.commit()
                    print(f"\n\tItem Added To Cart: [{name}] | Quantity: {qty}\n")
                    cart[name] = [price, qty]
                elif quantity < qty:
                    print(f"\n\tNot enough stock available for item [{name}].\n")
                else:
                    print(f"\n\tItem [{name}] is out of stock.\n")
            else:
                print(f"\n\tItem with id {item_id} does not exist.\n")
            
            if item_id == 123456:
                stop = True
                continue 

        purchaseTime = datetime.now()
        receipt = f"""
        PySHOP - Your Pythonic SHOP
        Receipt for user [{unique_id}]: {username}0\n\tAddress: {address}\n\n"""
        total = 0       
        for item, qty in cart.items():
            total += qty[0] * qty[1]
            receipt += f"\tItem: {item} | Quantity: {qty[1]} | Price: {qty[0] * qty[1]}\n"
        receipt += f"\n\tGRAND TOTAL: {total}  |  TIME OF PURCHASE: {purchaseTime}"
        cur.execute("""INSERT INTO receipt (buyer_name, secret_id, date, total, description) VALUES (?, ?, ?, ?, ?)""", (username, unique_id, purchaseTime, total, receipt))
        conn.commit()
        clear_console()
        print(receipt)
        print(f"\n\tPlease pay [{total}] and collect your items.\n\tTHANK YOU FOR SHOPPING WITH US :D\n\tYou can also scan the qr code to get your receipt.")
        code = pyqrcode.create(receipt)
        code.png(Path(current_path / Path("receipt.png")), scale=3)
        input("Press Enter to continue...")
        print_info()


def show_sales():
    '''Shows the total sales of the PySHOP.'''
    clear_console()
    print("""
    ================================
    Show sales.
    ================================
    """)
    cur.execute("SELECT * FROM receipt")
    data = cur.fetchall()
    if data:
        print("\tID\tBuyer Name\t\tDate\t\t\t\tTotal\n")
        for i in data:
            print(f"\t{i[0]}\t{i[1]}\t\t{i[3]}\t\t\t\t{i[4]}\n")
    else:
        print("\n\tNo sales yet.\n")
    input("\n\tPress ENTER to go back to main screen...")
    print_info()


print_info()