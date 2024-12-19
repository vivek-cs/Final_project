##Final_Project

     #Readme file:

##FastAPI SQLite Integration
This project demonstrates a simple CRUD (Create, Read, Update, Delete) API using FastAPI framework with SQLite database integration. It allows managing customers, items, and orders.

##Features:
•	Create, read, update, and delete customers
•	Create, read, update, and delete items
•	Create and read orders

##Prerequisites:
•	Python 3.7 or later installed
•	Virtual environment setup
•	Installation

##Steps for Execution:
 1.Create a virtual environment 
    •	python -m venv venv
 2.Activate the virtual environment:
    •	venv\Scripts\activate
    •	source venv/bin/activate
 3.Install dependencies:
   •	pip install fastapi
   •	pip install uvicorn
   •	pip install pydantic
 4.Initialize the SQLite database:
   •	python db_init.py
   This script will create the necessary tables and populate them with sample data from example_orders.json.
 5.Run the FastAPI server:
   •	uvicorn main:app --reload
   The server will start running on http://127.0.0.1:8000.
   Access the API documentation:Open your web browser and navigate to http://127.0.0.1:8000/docs to access the Swagger UI. Here, you can explore and interact with the API endpoints.


##API Endpoints
Customers:
POST /customers/: Create customer
GET /customers/{cust_id}: Read Customer
PUT /customers/{cust_id}: Update Customer 
DELETE /customers/{cust_id}: Delete Customer 
Items:
POST /items/: Create  item
GET /items/{item_id}: Read item 
PUT /items/{item_id}: Update item 
DELETE /items/{item_id}: Delete  item 
Orders:
POST /orders/: Create Order
GET /orders/{order_id}: Read Order 
PUT /orders/{order_id}: Update Order 
DELETE /orders/{order_id}: Delete Order 
 
