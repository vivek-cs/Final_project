import json
import sys

def read_orders(file_name):
    """Reads orders from a JSON file."""
    with open(file_name, 'r') as file:
        orders = json.load(file)
    return orders

def create_customers_json(orders):
    """Creates a JSON file named 'customers.json' with phone numbers as keys and customer names as values."""
    customers = {}
    for order in orders:
        phone = order['phone']
        name = order['name']
        customers[phone] = name

    with open('customers.json', 'w') as file:
        json.dump(customers, file, indent=2)

def create_items_json(orders):
    """Creates a JSON file named 'items.json' with item names as keys, and price and order count as values."""
    items = {}
    for order in orders:
        for item in order['items']:
            name = item['name']
            price = item['price']

            if name in items:
                items[name]['orders'] += 1
            else:
                items[name] = {'price': price, 'orders': 1}

    with open('items.json', 'w') as file:
        json.dump(items, file, indent=2)

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <orders_file.json>")
        sys.exit(1)

    orders_file = sys.argv[1]
    orders = read_orders(orders_file)

    create_customers_json(orders)
    create_items_json(orders)

if __name__ == "__main__":
    main()
