# Midterm Project: Order Processing System

## Project Overview
This project is designed to process orders from a JSON file, organize customer data, and generate two output files: `customers.json` and `items.json`. This structure simplifies the order data by separating customer and item data into two separate JSON files for easy and efficient analysis.

## Design
The project is structured around a Python script named `process_orders.py`, which deals with the data processing. The design focuses on simplicity and efficiency, ensuring that the data extraction, transformation, and storage are handled in a clean, straightforward manner.
The organisation of the design is as follows:

**Organized Code Structure:**
-The script is divided into sections that handle different tasks like loading data, organizing, and saving the results.
-This clear structure makes the code easier to read and edit.

**Data Extraction:**
-The script reads order data from a JSON file (example_orders.json).
-It uses Python's built-in JSON handling capabilities to load this data quickly and accurately.

**Data Processing:**
-After loading the data, the script cleans it up and organizes it.
-It makes sure that customer details are consistent and groups the items in the orders properly.

**Saving the Results:**
-The cleaned data is saved into two new files: customers.json and items.json.
-customers.json has customer details like names and phone numbers, with duplicates removed.
-items.json lists the ordered items, showing order history which includes name, how many, and the prices of the items.

**Error Handling:**
-The script includes basic checks to handle problems like missing information or data that doesn’t fit the expected format.
-It makes sure the data is correct before saving it to the output files.

**Simple and Efficient:**
-The design keeps the script as simple as possible without losing the ability to handle the data correctly.
-This makes it easy to understand how the data is being processed and makes future updates or changes simpler.


## Key Components
1. **Input File:**
   - `example_orders.json`: Contains raw order data, including customer information and ordered items.

2. **Output Files:**
   - `customers.json`: Stores customer names and phone numbers extracted from the order data.
   - `items.json`: Contains item details such as item names, prices, and the number of times each item was ordered.

3. **Script:**
   - `process_orders.py`: The core script that reads the order data from `example_orders.json`, processes it, and generates the two output files (`customers.json` and `items.json`).

## How to Use the Project

### Prerequisites
- Python 3.x must be installed on your system.

### Setup Instructions
1. **Clone the repository:**
   git clone https://github.com/vivek-cs/Midterm_project.git

2. **Navigate to the project directory:**
    cd Midterm_project

3. **Running the Project To process the order data and generate the output files, run the following command:**
    python process_orders.py example_orders.json

### Expected Output:
After running the script, two files will be generated in the project directory:
-customers.json: Contains a list of customers with their names and phone numbers.
-items.json: Contains the items ordered, including their prices and order counts.
