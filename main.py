import sqlite3
from pathlib import Path
import os
import time
import datetime
import string
import random
import math

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
            name TEXT
            price FLOAT,
            quantity INTEGER
        )
    """)
create_required_tables()

def generate_unique_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

def register_user():
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

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_info():
    clear_console()
    print("""
    ********************************
    **      WELCOME TO PySHOP     **
    ********************************

    ================================
    Select an option:
    ================================
    1. Register a new user.
    2. Show all users.
    3. Add an item to the shop.
    4. Show all items from shop.
    5. Buy items from the shop.
    6. Show total sales.
    7. Exit.


    """)
    select_option()

def select_option():
    option = int(input('>>> Select an option [1-6]:\t'))
    clear_console()
    if option > 7 or option < 1:
        print("Invalid option. Try again.\n")
        time.sleep(1)
        clear_console()
        print_info()
    if option == 1:
        register_user()
    elif option == 2:
        show_users()
    # elif option == 3:
    #     add_items()
    # elif option == 4:
    #     show_shop()
    # elif option == 5:
    #     buy_items()
    # elif option == 6:
    #     show_sales()
    elif option == 7:
        exit()

print_info()