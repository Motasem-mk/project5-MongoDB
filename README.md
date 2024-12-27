# MongoDB Data Migration Script

## Description
This project contains a Python script designed to migrate a healthcare dataset from a CSV file into a MongoDB database. The script performs essential data cleaning, such as removing duplicates, normalizing column values, and converting date columns into a consistent format, before inserting the data into MongoDB. It also logs the progress and outputs sample records to verify the migration.

---

## Features
- Reads a healthcare dataset from a CSV file.
- Performs basic data cleaning:
  - Removes duplicate records.
  - Converts date columns to `datetime` format.
  - Normalizes names to title case for consistency.
- Inserts cleaned data into MongoDB.
- Configurable database and collection names.
- Logs progress and errors for debugging.

---

## Prerequisites
Before running the script, ensure the following:
- **MongoDB** is installed and running locally on `localhost:27017`.
- **Python** version 3.8 or higher is installed.
- Required Python libraries:
  - `pymongo`
  - `pandas`
  - `logging`

---

## Installation


 # Clone the repository
git clone https://github.com/Motasem-mk/project5-MongoDB.git

# Navigate to the project folder
cd project5-MongoDB

# Install required libraries
pip install -r requirements.txt


