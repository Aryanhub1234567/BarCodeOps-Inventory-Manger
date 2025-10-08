import sqlite3
import csv

# Create/connect to database
conn = sqlite3.connect('Inventory.db')
cursor = conn.cursor()

#cursor.execute("DROP TABLE IF EXISTS products")

# Create table (run only once)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT UNIQUE,
        product_name TEXT,
        quantity INTEGER,
        price REAL,
        type TEXT
    )
''')
conn.commit()

# Creating Product class
class Product:
    def __init__(self, barcode, name, quantity, price, type):
        self.barcode = barcode
        self.name = name
        self.quantity = quantity
        self.price = price
        self.type = type

# Inserting product info

def insert_product(product):
    conn = sqlite3.connect('Inventory.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO products (barcode, product_name, quantity, price, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (product.barcode, product.name, product.quantity, product.price, product.type))
    conn.commit()
    conn.close()


# Fetch Data
def get_inventory():
    conn = sqlite3.connect('Inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    return rows

# Print the products
for product in get_inventory():
    print(product)


##############################################################  CSV export
# Fetch all data from the 'products' table
cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()

# Column names (optional, but useful)
column_names = [description[0] for description in cursor.description]

# Write to CSV
with open('Stock.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write header
    csvwriter.writerow(column_names)
    
    # Write data rows
    csvwriter.writerows(rows)


print("Data exported to Stock.csv")
###############################################################

def get_product_by_barcode(barcode):
    conn = sqlite3.connect('Inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE barcode=?", (barcode,))
    result = c.fetchone()
    conn.close()
    return result

# Update Stock (incr/decr) :

def update_stock(barcode, change):
    conn = sqlite3.connect('Inventory.db')
    c = conn.cursor()
    c.execute("UPDATE products SET quantity = quantity + ? WHERE barcode = ?", (change, barcode))
    conn.commit()
    conn.close()

# update_stock("1234567890", -1)  # Reduce stock by 1 on sale
# update_stock("1234567890", 5)   # Add stock by 5 on restocking


# Reset Table and ID
'''cursor.execute("DELETE FROM products")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='products'")  # Resets AUTOINCREMENT
conn.commit()'''


# Find the highest ID (most recent entry)
cursor.execute("SELECT id FROM products ORDER BY id DESC LIMIT 1")
row = cursor.fetchone()

def DEL_recentID() :
    if row:
        last_id = row[0]
        cursor.execute("DELETE FROM products WHERE id = ?", (last_id,))
        conn.commit()
        print(f"Deleted row with ID: {last_id}")
    else:
        print("No data to delete.")

#DEL_recentID()


conn.close()
