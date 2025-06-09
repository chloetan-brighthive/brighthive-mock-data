import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import os
from datetime import datetime

# Get current date for directory naming
current_date = datetime.now()
date_suffix = current_date.strftime("%m-%d")

# Get script directory and create output directory
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, f"../output/retail_{date_suffix}")
os.makedirs(output_dir, exist_ok=True)

fake = Faker()
np.random.seed(42)
random.seed(42)

def generate_dates(n, start_date='2023-01-01'):
    start = pd.to_datetime(start_date)
    dates = [start + timedelta(days=x) for x in range(n)]
    return pd.to_datetime(random.choices(dates, k=n))

def generate_customer_data(n_customers):
    def create_email_from_name(name):
        # Convert name to lowercase and replace spaces with dots
        name = name.lower().replace(' ', '.')
        # Remove any special characters
        name = ''.join(e for e in name if e.isalnum() or e == '.')
        # Add a random number (1-999) to make it more unique
        random_num = random.randint(1, 999)
        # Choose a random domain
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        domain = random.choice(domains)
        return f"{name}{random_num}@{domain}"

    # Generate names first
    names = [fake.name() for _ in range(n_customers)]

    customers = {
        'customer_id': range(1, n_customers + 1),
        'name': names,
        'email': [create_email_from_name(name) for name in names],
        'phone': [fake.phone_number() for _ in range(n_customers)],
        'address': [fake.address().replace('\n', ', ') for _ in range(n_customers)],
        'registration_date': generate_dates(n_customers),
        'customer_segment': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], n_customers,
                                           p=[0.4, 0.3, 0.2, 0.1])
    }
    return pd.DataFrame(customers)

def generate_product_data(n_products):
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports', 'Beauty', 'Toys']

    # Create lists of adjectives and nouns for product names
    adjectives = ['Premium', 'Deluxe', 'Basic', 'Ultra', 'Essential', 'Professional', 'Classic', 'Elite', 'Luxury', 'Smart']
    electronics = ['Headphones', 'Smartphone', 'Laptop', 'Tablet', 'Camera', 'Speaker', 'Monitor', 'Keyboard', 'Mouse', 'Charger']
    clothing = ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sweater', 'Shorts', 'Skirt', 'Coat', 'Socks', 'Hat']
    home_garden = ['Chair', 'Table', 'Lamp', 'Rug', 'Pillow', 'Vase', 'Plant', 'Mirror', 'Clock', 'Blanket']
    books = ['Novel', 'Cookbook', 'Biography', 'Textbook', 'Magazine', 'Comic', 'Journal', 'Guide', 'Manual', 'Dictionary']
    sports = ['Ball', 'Racket', 'Shoes', 'Bag', 'Mat', 'Weights', 'Gloves', 'Helmet', 'Bat', 'Jersey']
    beauty = ['Shampoo', 'Cream', 'Lotion', 'Perfume', 'Soap', 'Mask', 'Oil', 'Brush', 'Mirror', 'Serum']
    toys = ['Doll', 'Car', 'Puzzle', 'Game', 'Block', 'Robot', 'Plush', 'Board Game', 'Action Figure', 'Art Set']

    category_products = {
        'Electronics': electronics,
        'Clothing': clothing,
        'Home & Garden': home_garden,
        'Books': books,
        'Sports': sports,
        'Beauty': beauty,
        'Toys': toys
    }

    products = []
    for i in range(n_products):
        category = np.random.choice(categories)
        adjective = np.random.choice(adjectives)
        product_type = np.random.choice(category_products[category])
        brand = fake.company()[:10]  # Get a random brand name

        products.append({
            'product_id': i + 1,
            'product_name': f"{brand} {adjective} {product_type}",
            'category': category,
            'sub_category': product_type,
            'unit_price': np.random.uniform(10, 1000, 1)[0].round(2),
            'stock_quantity': np.random.randint(0, 1000),
            'reorder_point': np.random.randint(10, 100),
            'supplier_id': np.random.randint(1, 51),
            'weight_kg': np.random.uniform(0.1, 20, 1)[0].round(2)
        })

    return pd.DataFrame(products)

def generate_sales_data(n_transactions, customers_df, products_df):
    sales = []
    for _ in range(n_transactions):
        customer_id = np.random.choice(customers_df['customer_id'])
        n_items = np.random.randint(1, 6)
        transaction_date = fake.date_time_between(start_date='-1y', end_date='now')

        for _ in range(n_items):
            product_id = np.random.choice(products_df['product_id'])
            product_price = products_df.loc[products_df['product_id'] == product_id, 'unit_price'].iloc[0]
            quantity = np.random.randint(1, 5)

            sales.append({
                'transaction_id': fake.uuid4(),
                'customer_id': customer_id,
                'product_id': product_id,
                'transaction_date': transaction_date,
                'quantity': quantity,
                'unit_price': product_price,
                'total_amount': quantity * product_price,
                'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash']),
                'channel': np.random.choice(['Online', 'In-store', 'Mobile App'], p=[0.6, 0.3, 0.1])
            })
    return pd.DataFrame(sales)

def generate_inventory_movements(n_movements, products_df):
    movements = {
        'movement_id': range(1, n_movements + 1),
        'product_id': np.random.choice(products_df['product_id'], n_movements),
        'date': generate_dates(n_movements),
        'movement_type': np.random.choice(['IN', 'OUT'], n_movements),
        'quantity': np.random.randint(1, 100, n_movements),
        'warehouse_id': np.random.randint(1, 6, n_movements)
    }
    return pd.DataFrame(movements)

# Generate the datasets
customers_df = generate_customer_data(1000)
products_df = generate_product_data(200)
sales_df = generate_sales_data(5000, customers_df, products_df)
inventory_df = generate_inventory_movements(2000, products_df)

# Save the datasets with new naming convention
file_names = {
    'customers': f'retail_data_customers_{date_suffix}.csv',
    'products': f'retail_data_products_{date_suffix}.csv',
    'sales': f'retail_data_sales_{date_suffix}.csv',
    'inventory': f'retail_data_inventory_{date_suffix}.csv'
}

# Save files
# customers_df.to_csv(os.path.join(output_dir, file_names['customers']), index=False)
# products_df.to_csv(os.path.join(output_dir, file_names['products']), index=False)
sales_df.to_csv(os.path.join(output_dir, file_names['sales']), index=False)
# inventory_df.to_csv(os.path.join(output_dir, file_names['inventory']), index=False)

# Print dataset information
print("\nDataset Summaries:")
print(f"\nOutput Directory: {output_dir}")

print("\n1. Customers Dataset:")
print(f"Number of records: {len(customers_df)}")
print(f"Columns: {customers_df.columns.tolist()}")

print("\n2. Products Dataset:")
print(f"Number of records: {len(products_df)}")
print(f"Columns: {products_df.columns.tolist()}")

print("\n3. Sales Dataset:")
print(f"Number of records: {len(sales_df)}")
print(f"Columns: {sales_df.columns.tolist()}")

print("\n4. Inventory Movements Dataset:")
print(f"Number of records: {len(inventory_df)}")
print(f"Columns: {inventory_df.columns.tolist()}")

# Created/Modified files during execution:
print("\nCreated/Modified files:")
for file_name in file_names.values():
    print(os.path.join(output_dir, file_name))
