from pymongo import MongoClient
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global MongoDB connection
logging.info("Connecting to MongoDB...")
client = MongoClient('mongodb://mongodb:27017/')
logging.info("Successfully connected to MongoDB.")

db_name = 'healthcare'
logging.info(f"Using database: {db_name}")

collection_name = "patients"
logging.info(f"Using collection: {collection_name}")

db = client[db_name]
collection = db[collection_name]

# Data cleaning
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

# CRUD Operations
#1-Create (insert a new record)
def create_patient_record(new_record):
    try:
        result = collection.insert_one(new_record)
        logging.info(f"CRUD Operation 1-Create ... >>> Record inserted with ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        logging.error(f"Error inserting record: {e}")
        return None

# Example: Add a new record
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
create_patient_record(new_record)

#2. Read (Query Records)
def read_patient_records(collection, query={}):
    try:
        results = collection.find(query)
        records = list(results)
        logging.info(f"CRUD Operation 2. Read ... >>> Found {len(records)} record(s) matching the query.")
        return records
    except Exception as e:
        logging.error(f"Error reading records: {e}")
        return []
query1 = {"Age": {"$gte": 87}}  # Get all patients aged 87 or older
documents = read_patient_records(collection, query1)

for document in documents:
    print(documents)


#3. Update (Modify an Existing Record)

def update_patient_record(collection, query, update_fields):
    try:
        result = collection.update_many(query, {"$set": update_fields})
        logging.info(f"CRUD Operation 3. Update ... >>> Updated {result.modified_count} record(s).")
        return f"Matched :{result.matched_count} , Modified : {result.modified_count} "

    except Exception as e:
        logging.error(f"Error updating records: {e}")
        return 0

query2 = {'Name': 'Alice Brown'} # find record with this name 
update_field = {'Room Number':203 , 'Billing Amount':12000}
update_patient_record(collection , query2, update_field)

#check the updated document
document = collection.find({'Name': 'Alice Brown'})
for i in document :
    print(i)

#4. Delete (Remove Records)
def delete_patient_records(collection, query):
    try:
        result = collection.delete_many(query)
        logging.info(f"CRUD Operation 4. Delete... >> Deleted {result.deleted_count} record(s).")
        return result.deleted_count
    except Exception as e:
        logging.error(f"Error deleting records: {e}")
        return 0

query3 = {"Name": "Alice Brown"}  # Delete records with this name
delete_patient_records(collection, query3)

# check deleted record >> should print nothing  if the record is deleted 
doc= collection.find({'Name': 'Alice Brown'})
for i in doc :
    print(i)
