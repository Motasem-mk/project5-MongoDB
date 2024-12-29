from pymongo import MongoClient
import pandas as pd
import logging
import os 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables for MongoDB credentials
mongo_uri = os.getenv("MONGO_URI", "mongodb://admin:securepassword@mongodb:27017/")
db_name = os.getenv("DB_NAME", "healthcare")
collection_name = os.getenv("COLLECTION_NAME", "patients")

# Global MongoDB connection
logging.info("Connecting to MongoDB...")
client = MongoClient(mongo_uri)
logging.info("Successfully connected to MongoDB.")

db = client[db_name]
logging.info(f"Using database: {db_name}")

collection = db[collection_name]
logging.info(f"Using collection: {collection_name}")

# Data cleaning and migration
logging.info("Loading and cleaning the dataset...")
healthcare = pd.read_csv("healthcare_dataset.csv")
healthcare = healthcare.drop_duplicates()

# Convert date columns to datetime
healthcare['Date of Admission'] = pd.to_datetime(healthcare['Date of Admission'])
healthcare['Discharge Date'] = pd.to_datetime(healthcare['Discharge Date'])

# Normalize the name
healthcare['Name'] = healthcare['Name'].str.title()

# Verify logical consistency
invalid_dates = healthcare[healthcare['Discharge Date'] <= healthcare['Date of Admission']]
logging.info(f"Found {len(invalid_dates)} records with invalid dates.")
healthcare = healthcare[healthcare['Discharge Date'] > healthcare['Date of Admission']]

# Convert DataFrame to dictionary
healthcare_dict = healthcare.to_dict(orient='records')
logging.info(f"Prepared {len(healthcare_dict)} records for migration.")

# Insert data into MongoDB
logging.info(f"Inserting {len(healthcare_dict)} records into MongoDB...")
collection.insert_many(healthcare_dict)
logging.info("Data inserted successfully.")

# Creating a user with specific roles (if needed)
try:
    admin_db = client["admin"]
    logging.info("Creating a new user 'crud_user' with readWrite role for the healthcare database...")
    admin_db.command("createUser", "crud_user", pwd="crudpassword", roles=[
        {"role": "readWrite", "db": "healthcare"}
    ])
    logging.info("User 'crud_user' created successfully.")
except Exception as e:
    logging.warning(f"Error creating user or user already exists: {e}")

# CRUD Operations
# Create
new_record = {
    "Name": "Alice Brown",
    "Age": 25,
    "Gender": "Female",
    "Blood Type": "A+",
    "Medical Condition": "Asthma",
    "Date of Admission": "2024-03-01",
    "Doctor": "Sarah Lee",
    "Hospital": "MediCare Center",
    "Insurance Provider": "United Health",
    "Billing Amount": 12345.67,
    "Room Number": 201,
    "Admission Type": "Routine",
    "Discharge Date": "2024-03-05",
    "Medication": "Inhaler",
    "Test Results": "Improved"
}
logging.info("Inserting a new patient record...")
insert_result = collection.insert_one(new_record)
logging.info(f"Record inserted with ID: {insert_result.inserted_id}")

# Read
query = {"Age": {"$gte": 88}}  # Get all patients aged 88 or older
logging.info(f"Querying records with age >= 88...")
results = collection.find(query)
records = list(results)
logging.info(f"Found {len(records)} record(s) matching the query.")

# Update
query = {'Name': 'Alice Brown'}  # Find record with this name
update_fields = {'Room Number': 203, 'Billing Amount': 12000}
logging.info("Updating patient record for 'Alice Brown'...")
update_result = collection.update_many(query, {"$set": update_fields})
logging.info(f"Matched: {update_result.matched_count}, Modified: {update_result.modified_count}")

# Verify the updated record
updated_record = collection.find({'Name': 'Alice Brown'})
logging.info("Updated record:")
for doc in updated_record:
    print(doc)

# Delete
query = {"Name": "Alice Brown"}  # Delete records with this name
logging.info("Deleting patient record for 'Alice Brown'...")
delete_result = collection.delete_many(query)
logging.info(f"Deleted {delete_result.deleted_count} record(s).")

# Verify the deletion
deleted_check = collection.find({'Name': 'Alice Brown'})
if deleted_check.count() == 0:
    logging.info("Record successfully deleted.")
else:
    logging.warning("Record was not deleted.")
