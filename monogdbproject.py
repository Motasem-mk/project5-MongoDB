from pymongo import MongoClient
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables for MongoDB credentials
admin_mongo_uri = "mongodb://admin:motasem@mongodb:27017/"  #  admin credentials
db_name = "healthcare"
collection_name = "patients"

# Step 1: Connect as admin
logging.info("Connecting to MongoDB as admin...")
admin_client = MongoClient(admin_mongo_uri)
db = admin_client[db_name]
logging.info(f"Using database: {db_name}")
collection = db[collection_name]
logging.info(f"Using collection: {collection_name}")

# Step 2: Data migration
logging.info("Loading and cleaning the dataset...")
healthcare = pd.read_csv("healthcare_dataset.csv")

# Pre-migration data integrity checks
# Check for missing values
missing_values = healthcare.isnull().sum()
logging.info("Missing values per column:\n", missing_values)

# Check for duplicates
duplicates = healthcare.duplicated().sum()
logging.info(f"Number of duplicate records: {duplicates}")

# Check for logical errors in the dates (discharge date should be after admission date)
invalid_dates = healthcare[healthcare['Discharge Date'] <= healthcare['Date of Admission']]
logging.info(f"Number of invalid date records: {len(invalid_dates)}")

# Check if age or billing amounts are negative
invalid_values = healthcare[(healthcare['Age'] < 0) | (healthcare['Billing Amount'] < 0)]
logging.info(f"Number of records with invalid values (negative age or billing amount): {len(invalid_values)}")

# Optional: Stop the script if any integrity issues are found
if duplicates > 0 or len(invalid_dates) > 0 or len(invalid_values) > 0:
    raise ValueError("Data contains integrity issues. Please fix the data before migration.")

# Clean data (drop duplicates, remove invalid dates)
healthcare = healthcare.drop_duplicates()
healthcare = healthcare[healthcare['Discharge Date'] > healthcare['Date of Admission']]

# Convert date columns to datetime
healthcare['Date of Admission'] = pd.to_datetime(healthcare['Date of Admission'])
healthcare['Discharge Date'] = pd.to_datetime(healthcare['Discharge Date'])

# Normalize the name
healthcare['Name'] = healthcare['Name'].str.title()

# Convert DataFrame to dictionary
healthcare_dict = healthcare.to_dict(orient='records')
logging.info(f"Prepared {len(healthcare_dict)} records for migration.")

# Insert data into MongoDB
logging.info(f"Inserting {len(healthcare_dict)} records into MongoDB...")
collection.insert_many(healthcare_dict)
logging.info("Data inserted successfully.")

# Step 3: Post-migration Data Integrity Checks

# Check if the number of records in MongoDB matches the CSV data
mongo_count = collection.count_documents({})
csv_count = len(healthcare)
logging.info(f"Records in MongoDB: {mongo_count}, Records in CSV: {csv_count}")

if mongo_count != csv_count:
    raise ValueError("The number of records in MongoDB does not match the CSV data!")

# Check for missing fields in MongoDB
missing_in_mongo = []
for field in ['Age', 'Medical Condition', 'Name']:
    missing = collection.count_documents({field: {"$exists": False}})
    if missing > 0:
        missing_in_mongo.append(field)

if missing_in_mongo:
    logging.warning(f"Missing fields in MongoDB: {missing_in_mongo}")

# Check for invalid dates in MongoDB (discharge date should be after admission date)
invalid_mongo_dates = collection.find({"$where": "this['Discharge Date'] <= this['Date of Admission']"})
invalid_mongo_dates_count = sum(1 for _ in invalid_mongo_dates)
if invalid_mongo_dates_count > 0:
    raise ValueError(f"Found {invalid_mongo_dates_count} records with invalid dates in MongoDB!")

# Check for negative values in Age or Billing Amount in MongoDB
invalid_mongo_values = collection.find({"$or": [{"Age": {"$lt": 0}}, {"Billing Amount": {"$lt": 0}}]})
invalid_mongo_values_count = sum(1 for _ in invalid_mongo_values)
if invalid_mongo_values_count > 0:
    raise ValueError(f"Found {invalid_mongo_values_count} records with negative values in MongoDB!")

# Step 4: CRUD Operations
# Create new record
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

# Read records
query = {"Age": {"$gte": 88}}  # Get all patients aged 88 or older
logging.info(f"Querying records with age >= 88...")
results = collection.find(query)
records = list(results)
logging.info(f"Found {len(records)} record(s) matching the query.")

# Update record
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

# Delete record
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
