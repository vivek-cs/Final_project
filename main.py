from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import time

# Initialize FastAPI app
app = FastAPI()

# Define models
class Customer(BaseModel):
    cust_id: int | None = None
    name: str
    phone: str

class Item(BaseModel):
    id: int | None = None
    name: str
    price: float

class Order(BaseModel):
    order_id: int | None = None
    notes: str
    cust_id: int
    timestamp: int

# Database connection and foreign key support
conn = sqlite3.connect("db.sqlite")
conn.execute("PRAGMA foreign_keys = ON;")
conn.close()

# Customer routes
@app.post("/customers/")
def create_customer(customer: Customer):
    if customer.cust_id is not None:
        raise HTTPException(status_code=400, detail="cust_id cannot be set on POST request")

    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (customer.name, customer.phone))
    customer.cust_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return customer

@app.get("/customers/{cust_id}")
def read_customer(cust_id: int):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM customers WHERE id=?", (cust_id,))
    customer = cursor.fetchone()
    conn.close()
    if customer is not None:
        return Customer(cust_id=customer[0], name=customer[1], phone=customer[2])
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@app.put("/customers/{cust_id}")
def update_customer(cust_id: int, customer: Customer):
    # Check if customer ID provided in the path matches

    # Update logic changed here: 
    # Instead of updating all fields, lets allow partial updates based on provided data
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    # Check if the customer ID exists in the database
    cursor.execute("SELECT id FROM customers WHERE id = ?;", (cust_id,))
    existing_customer = cursor.fetchone()
    if existing_customer is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer ID not found")

    # Build update query based on provided data in customer object
    update_query = "UPDATE customers SET "
    update_data = []
    if customer.name is not None:
        update_query += "name=?, "
        update_data.append(customer.name)
    if customer.phone is not None:
        update_query += "phone=? "
        update_data.append(customer.phone)

    # Remove trailing comma if only one field is updated
    update_query = update_query.rstrip(", ") + " WHERE id=?; "
    update_data.append(cust_id)

    # Execute update query with parameters
    cursor.execute(update_query, update_data)
    conn.commit()

    # Re-fetch the updated customer data
    cursor.execute("SELECT id, name, phone FROM customers WHERE id=?", (cust_id,))
    updated_customer = cursor.fetchone()

    # Close the connection after all operations are completed
    conn.close()

    # Return the updated customer information
    if updated_customer is not None:
        return Customer(cust_id=updated_customer[0], name=updated_customer[1], phone=updated_customer[2])
    else:
        # This shouldn't happen, but handle potential error
        raise HTTPException(status_code=500, detail="Internal server error during update")



@app.delete("/customers/{cust_id}")
def delete_customer(cust_id: int):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=?;", (cust_id,))
    conn.commit()
    conn.close()
    return {"message": "Customer deleted successfully"}


@app.post("/items/")
def create_item(item: Item):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    try:
        # Check for duplicate item name before inserting
        curr.execute("SELECT id FROM items WHERE name = ?", (item.name,))
        existing_item = curr.fetchone()
        if existing_item:
            raise HTTPException(status_code=400, detail="Item with that name already exists")

        curr.execute("INSERT INTO items (name, price) VALUES (?, ?);", (item.name, item.price))
        conn.commit()
        new_id = curr.lastrowid
        return {"id": new_id, "name": item.name, "price": item.price}
    finally:
        conn.close()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    try:
        curr.execute("SELECT id, name, price FROM items WHERE id = ?", (item_id,))
        item = curr.fetchone()
        if item is not None:
            return {"id": item[0], "name": item[1], "price": item[2]}  # Access elements by index
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    finally:
        conn.close()


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item.id != item_id:
        raise HTTPException(status_code=400, detail="Item ID does not match ID in path")

    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    try:
        curr.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        existing_item = curr.fetchone()
        if existing_item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        # Update only provided fields
        update_query = "UPDATE items SET "
        update_data = []
        if item.name is not None:
            update_query += "name=?, "
            update_data.append(item.name)
        if item.price is not None:
            update_query += "price=? "
            update_data.append(item.price)

        # Remove trailing comma if only one field is updated
        update_query = update_query.rstrip(", ") + "WHERE id=?; "
        update_data.append(item_id)

        curr.execute(update_query, update_data)
        conn.commit()
        return {"message": "Item updated successfully"}
    finally:
        conn.close()

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    try:
        curr.execute("DELETE FROM items WHERE id=?;", (item_id,))
        total_changes = conn.total_changes
        conn.commit()
        if total_changes == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return total_changes
    finally:
        conn.close()



@app.post("/orders/")
def create_order(order: Order):
    if order.order_id is not None:
        raise HTTPException(status_code=400, detail="order_id cannot be set on POST request")
    if order.cust_id is None:
        raise HTTPException(status_code=400, detail="cust_id is required")

    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    try:
        # Check for existing customer (similar to previous logic)
        curr.execute("SELECT id FROM customers WHERE id=?;", (order.cust_id,))
        customer = curr.fetchone()
        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Instead of storing timestamp in request, generate it on server
        current_timestamp = int(time.time())  # Import time module

        # Insert the order with generated timestamp
        curr.execute("INSERT INTO orders (notes, cust_id, timestamp) VALUES (?, ?, ?);",
                     (order.notes, order.cust_id, current_timestamp))
        new_order_id = curr.lastrowid
        conn.commit()
        return Order(order_id=new_order_id, notes=order.notes, cust_id=order.cust_id, timestamp=current_timestamp)
    finally:
        conn.close()


@app.get("/orders/{order_id}")
def read_order(order_id: int):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    try:
        # Retrieve the order details (unchanged)
        curr.execute("SELECT id, notes, cust_id, timestamp FROM orders WHERE id=?", (order_id,))
        order = curr.fetchone()

        # Check if the order exists (unchanged)
        if order is not None:
            return Order(order_id=order[0], notes=order[1], cust_id=order[2], timestamp=order[3])
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    finally:
        conn.close()


@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    if order.order_id is not None and order.order_id != order_id:
        raise HTTPException(status_code=400, detail="order_id does not match ID in path")

    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    try:
        # Check if the order exists (unchanged)
        curr.execute("SELECT id FROM orders WHERE id=?;", (order_id,))
        existing_order = curr.fetchone()
        if existing_order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        # Check if the customer exists (unchanged)
        curr.execute("SELECT id FROM customers WHERE id=?;", (order.cust_id,))
        existing_customer = curr.fetchone()
        if existing_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Update logic changed: instead of updating all fields, allow partial updates
        update_query = "UPDATE orders SET "
        update_data = []
        if order.notes is not None:
            update_query += "notes=?, "
            update_data.append(order.notes)

        # No update for timestamp as it's not editable

        # Remove trailing comma if only notes are updated
        update_query = update_query.rstrip(", ") + "WHERE id=?; "
        update_data.append(order_id)

        # Execute update query with parameters (if any)
        if update_data:
            curr.execute(update_query, update_data)
        else:
            # No update needed, inform user
            return {"message": "No changes provided for update"}

        conn.commit()
        # Don't return the entire order, just a success message
        return {"message": "Order updated successfully"}
    finally:
        conn.close()


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    try:
        # Connect to the database
        conn = sqlite3.connect("db.sqlite")
        curr = conn.cursor()

        # Check if the order exists using a single query
        exists = await curr.execute(
            "SELECT EXISTS(SELECT 1 FROM orders WHERE id=?)", (order_id,)
        )

        # Process deletion based on existence
        if exists.fetchone()[0]:
            # Delete the order
            await curr.execute("DELETE FROM orders WHERE id=?;", (order_id,))
            conn.commit()
            return {"message": "Order deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Order not found")

    finally:
        # Close the connection (using async context manager)
        await conn.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}
