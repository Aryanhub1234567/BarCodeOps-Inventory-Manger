import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from Scanner import scan_barcode
from Database import get_product_by_barcode
from Database import get_inventory


def connect_db():
    return sqlite3.connect('Inventory.db')

def create_table():
    conn = connect_db()
    conn.execute('''
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
    conn.close()

def insert_product(barcode, name, quantity, price, type_):
    conn = connect_db()
    conn.execute('''
        INSERT OR IGNORE INTO products (barcode, product_name, quantity, price, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (barcode, name, quantity, price, type_))
    conn.commit()
    conn.close()

def get_inventory():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df

def delete_product_by_barcode(barcode):
    conn = sqlite3.connect("Inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE barcode=?", (barcode,))
    conn.commit()
    conn.close()

def update_product_quantity(barcode, new_quantity):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET quantity=? WHERE barcode=?", (new_quantity, barcode))
    conn.commit()
    conn.close()

def low_stock(threshold=12):
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM products WHERE quantity <= ?", conn, params=(threshold,))
    conn.close()
    return df

# ---- Streamlit UI ---- #

st.set_page_config(page_title="Inventory Dashboard", layout="wide")
st.image(r"C:\Users\Dell\OneDrive\Pictures\newbanner.jpg", use_container_width=True)
st.title("📦 BarCodeOps: Inventory Manager")

create_table()  # Ensure DB and table exist

st.sidebar.header("➕ Add New Product")
with st.sidebar.form("add_product_form"):
    barcode = st.text_input("Barcode")
    name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    price = st.number_input("Price", min_value=0.0, step=0.1)
    type_ = st.text_input("Type (Category)")
    submitted = st.form_submit_button("Add Product")
    if submitted:
        insert_product(barcode, name, quantity, price, type_)
        st.success(f"✅ Added {name} to Inventory.")

# Inventory display
st.subheader("📋 Current Inventory")
st.dataframe(get_inventory())

# Delete Product by scan

st.subheader("⛔ Delete Product")

if st.button("Start Barcode Scan to Delete"):
    barcode = scan_barcode()
    if barcode:
        product = get_product_by_barcode(barcode)
        if product:
            delete_product_by_barcode(barcode)
            st.success(f"✅ Product '{product[2]}' with Barcode {barcode} deleted successfully!")
        else:
            st.error(f"❌ Product with Barcode {barcode} not found in inventory.")
    else:
        st.warning("No barcode detected.")

# Update Stock quantity

st.subheader("✏️ Update Product Quantity")

if st.button("Start Barcode Scan to Update Quantity"):
    barcode = scan_barcode()
    if barcode:
        product = get_product_by_barcode(barcode)
        if product:
            st.info(f"Product Found: {product[2]} (Current Quantity: {product[3]})")
            new_quantity = st.number_input("Enter New Quantity", min_value=0, value=product[3])

            if st.button("Confirm Update"):
                update_product_quantity(barcode, new_quantity)
                st.success(f"✅ Quantity for '{product[2]}' updated to {new_quantity} successfully!")
        else:
            st.error(f"❌ Product with Barcode {barcode} not found in inventory.")
    else:
        st.warning("No barcode detected.")


# Low stock warning
st.subheader("⚠️ Low Stock Alert")
low_stock_df = low_stock()
if not low_stock_df.empty:
    st.error("Some products have low stock:")
    st.dataframe(low_stock_df)
else:
    st.success("✅ All products have sufficient stock.")


# Stock visuals
st.subheader("📊 Live Stock Visualization")

df = get_inventory()

if df.empty:
    st.warning("Inventory is empty.")
else:
    fig = px.bar(
        df,
        x='product_name',
        y='quantity',
        text='quantity',
        color='quantity',
        color_continuous_scale='Blues',
        title="📦 Stock Quantity per Product"
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)