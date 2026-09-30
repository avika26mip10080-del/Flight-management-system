Python 3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import mysql.connector


# ---------- Helpers ----------
def get_int(prompt):
    """Keep asking until the user enters a valid integer."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


# ---------- Database setup ----------
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root"
    )


def initialize_database():
    obj = connect_to_database()
    mycursor = obj.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS airlines")
    mycursor.execute("USE airlines")

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS food_items (
            sl_no INT AUTO_INCREMENT PRIMARY KEY,
            food_name VARCHAR(40) NOT NULL,
            price INT NOT NULL
        )
    """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS luggage (
            luggage_id INT AUTO_INCREMENT PRIMARY KEY,
            weight INT NOT NULL,
            price INT NOT NULL
        )
    """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS cust_details (
            cust_id INT AUTO_INCREMENT PRIMARY KEY,
            cust_name VARCHAR(40) NOT NULL,
            cont_no BIGINT NOT NULL
        )
    """)

    # booking_id is the primary key so many customers can share one flight_id
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS flight_details (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            flight_id INT NOT NULL,
            cus_id INT,
            cus_name VARCHAR(40) NOT NULL,
            FOREIGN KEY (cus_id) REFERENCES cust_details(cust_id)
        )
    """)

    obj.commit()
    return obj, mycursor


# ---------- Luggage ----------
def luggage(mycursor, obj):
    print("\nWhat do you want to do?")
    print("1. Add luggage")
    print("2. Delete luggage")
    choice = get_int("Enter your choice: ")

    if choice == 1:
        weight = get_int("Enter luggage weight: ")
        price = get_int("Enter luggage price: ")
        mycursor.execute(
            "INSERT INTO luggage (weight, price) VALUES (%s, %s)",
            (weight, price)
        )
        print("Luggage added.")
    elif choice == 2:
        luggage_id = get_int("Enter luggage ID: ")
        mycursor.execute("DELETE FROM luggage WHERE luggage_id = %s", (luggage_id,))
        print("Luggage deleted." if mycursor.rowcount else "No luggage with that ID.")
    else:
        print("Invalid option.")
    obj.commit()


# ---------- Food ----------
def food(mycursor, obj):
    print("\nWhat do you want to do?")
    print("1. Add new items")
    print("2. Update price")
    print("3. Delete items")
    choice = get_int("Enter your choice: ")

    if choice == 1:
        food_name = input("Enter food name: ")
        price = get_int("Enter food price: ")
        mycursor.execute(
            "INSERT INTO food_items (food_name, price) VALUES (%s, %s)",
            (food_name, price)
        )
        print("Food item added.")
    elif choice == 2:
        food_id = get_int("Enter food ID: ")
        new_price = get_int("Enter new price: ")
        mycursor.execute(
            "UPDATE food_items SET price = %s WHERE sl_no = %s",
            (new_price, food_id)
        )
        print("Price updated." if mycursor.rowcount else "No food item with that ID.")
    elif choice == 3:
        food_id = get_int("Enter food ID: ")
        mycursor.execute("DELETE FROM food_items WHERE sl_no = %s", (food_id,))
        print("Food item deleted." if mycursor.rowcount else "No food item with that ID.")
    else:
        print("Invalid option.")
    obj.commit()


def food_items(mycursor):
    print("\nAvailable Food Items:")
    mycursor.execute("SELECT sl_no, food_name, price FROM food_items")
    rows = mycursor.fetchall()
    if not rows:
        print("No food items available.")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Price: {row[2]}")
    print()


# ---------- Tickets / Flights ----------
def ticket_booking(mycursor, obj):
    cust_name = input("Enter customer name: ")
    contact_no = get_int("Enter contact number: ")
    flight_id = get_int("Enter flight ID: ")

    mycursor.execute(
        "INSERT INTO cust_details (cust_name, cont_no) VALUES (%s, %s)",
        (cust_name, contact_no)
    )
    customer_id = mycursor.lastrowid

    mycursor.execute(
        "INSERT INTO flight_details (flight_id, cus_id, cus_name) VALUES (%s, %s, %s)",
        (flight_id, customer_id, cust_name)
    )
    obj.commit()
    print("Ticket booked successfully!")


def flight_details(mycursor):
    print("\nBooked Flights:")
    mycursor.execute(
        "SELECT booking_id, flight_id, cus_name FROM flight_details ORDER BY flight_id"
    )
    rows = mycursor.fetchall()
    if not rows:
        print("No bookings yet.")
    for row in rows:
        print(f"Booking ID: {row[0]}, Flight ID: {row[1]}, Customer Name: {row[2]}")
    print()


# ---------- Menus ----------
def admin_interface(mycursor, obj):
    while True:
        print("\nAdmin Interface")
        print("1. Manage luggage")
        print("2. Manage food")
        print("3. View flight details")
        print("4. Exit")
        choice = get_int("Enter your choice: ")

        if choice == 1:
            luggage(mycursor, obj)
        elif choice == 2:
            food(mycursor, obj)
        elif choice == 3:
            flight_details(mycursor)
        elif choice == 4:
            break
        else:
            print("Invalid choice.")


def user_interface(mycursor, obj):
    while True:
        print("\nUser Interface")
        print("1. View food items")
...         print("2. Book a ticket")
...         print("3. Exit")
...         choice = get_int("Enter your choice: ")
... 
...         if choice == 1:
...             food_items(mycursor)
...         elif choice == 2:
...             ticket_booking(mycursor, obj)
...         elif choice == 3:
...             break
...         else:
...             print("Invalid choice.")
... 
... 
... def main_menu():
...     obj, mycursor = initialize_database()
...     try:
...         while True:
...             print("\nMain Menu")
...             print("1. Admin")
...             print("2. User")
...             print("3. Exit")
...             choice = get_int("Enter your choice: ")
... 
...             if choice == 1:
...                 admin_interface(mycursor, obj)
...             elif choice == 2:
...                 user_interface(mycursor, obj)
...             elif choice == 3:
...                 print("Exiting... Goodbye!")
...                 break
...             else:
...                 print("Invalid choice.")
...     finally:
...         mycursor.close()
...         obj.close()
... 
... 
... if __name__ == "__main__":
