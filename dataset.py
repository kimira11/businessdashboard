import pandas as pd
import sqlite3

# 1. Load the CSV file (replace 'dataset.csv' with your actual file path)
df = pd.read_csv('retail_sales_dataset.csv')

# 2. Data Cleaning - basic cleaning examples
df = df.dropna(subset=['Customer ID', 'Product Category', 'Total Amount', 'Quantity', 'Price per Unit'])
df['Customer ID'] = df['Customer ID'].astype(str)
df['Product Category'] = df['Product Category'].astype(str)
df['Total Amount'] = pd.to_numeric(df['Total Amount'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Price per Unit'] = pd.to_numeric(df['Price per Unit'], errors='coerce')
df = df.dropna()

# 3. Structure the tables

# Customers Table
customers = df[['Customer ID', 'Gender', 'Age']].drop_duplicates().copy()
customers['city'] = None  # Missing info
customers['email'] = None
customers['signupdate'] = None
customers.rename(columns={'Customer ID': 'id'}, inplace=True)
customers = customers[['id', 'Gender', 'email', 'city', 'signupdate', 'Age']]

# Products Table
products = df[['Product Category', 'Price per Unit']].drop_duplicates().copy()
products['id'] = products.index + 1
products['name'] = products['Product Category']
products['category'] = products['Product Category']
products['price'] = products['Price per Unit']
products['stock'] = None
products = products[['id', 'name', 'category', 'price', 'stock']]

# Orders Table
orders = df.copy()
orders['id'] = orders.index + 1
orders['customerid'] = orders['Customer ID']
orders['productid'] = orders['Product Category'].map(dict(zip(products['category'], products['id'])))
orders['quantity'] = orders['Quantity']
orders['orderdate'] = pd.to_datetime(orders['Date'], errors='coerce').dt.date
orders['total'] = orders['Total Amount']
orders = orders[['id', 'customerid', 'productid', 'quantity', 'orderdate', 'total']]

# Sales Table
sales = orders[['id', 'total', 'orderdate']].copy()
sales.rename(columns={'id': 'orderid', 'total': 'revenue', 'orderdate': 'salesdate'}, inplace=True)
sales['profitmargin'] = sales['revenue'] * 0.2  # dummy 20% profit margin
sales.reset_index(inplace=True)
sales.rename(columns={'index': 'id'}, inplace=True)
sales = sales[['id', 'orderid', 'revenue', 'profitmargin', 'salesdate']]

# 4. Store in SQLite
conn = sqlite3.connect('retail_dashboard.db')
customers.to_sql('customers', conn, if_exists='replace', index=False)
products.to_sql('products', conn, if_exists='replace', index=False)
orders.to_sql('orders', conn, if_exists='replace', index=False)
sales.to_sql('sales', conn, if_exists='replace', index=False)
conn.close()

print("Database created & tables loaded successfully.")
