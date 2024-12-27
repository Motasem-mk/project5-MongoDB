from pymongo import MongoClient
import pandas as pd 
import logging

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Data cleaning 
logging.info("Loading and cleaning the dataset...")
healthcare = pd.read_csv("healthcare_dataset.csv")
#Drop duplicates
healthcare = healthcare.drop_duplicates()

# Convert date columns to datetime
healthcare['Date of Admission'] = pd.to_datetime(healthcare['Date of Admission'])
healthcare['Discharge Date'] = pd.to_datetime(healthcare['Discharge Date'])

#Normalize the name
healthcare['Name'] = healthcare['Name'].str.title()

# Verify Logical Consistency:
invalid_dates = healthcare[healthcare['Discharge Date'] <= healthcare['Date of Admission']]
print(invalid_dates)

# Convert DataFrame to dictionary
healthcare_dict = healthcare.to_dict(orient='records')
logging.info(f"Prepared {len(healthcare_dict)} records for migration.")


def migrate_to_mongodb(data,db_name,collection_name):
    """
    Migrate data to MongoDB

    args: 
        data : List of dictionaries (JSON- Like format to insert)
        db_name(str) : Name of the MongoDB database
        collection_name (str): Name of the MongoDB collection

    Returns :
        None 
    """   
    try:
        logging.info("Connecting to MongoDB...")
        client = MongoClient('mongodb://mongodb:27017/')
        logging.info("Successfully connected to MongoDB.")

        db = client[db_name]
        logging.info(f"Using database: {db_name}")

        collection = db[collection_name]
        logging.info(f"Using collection: {collection_name}")

        logging.info(f"Inserting {len(data)} records into MongoDB...")
        collection.insert_many(data)
        logging.info("Data inserted successfully.")

        logging.info("Fetching and displaying sample records...")
        for document in collection.find().limit(1):
            logging.info(document)

    except Exception as e:
        logging.error(f"An error occurred: {e}")


#Migrate data
db_name = 'healthcare'
collection_name = "patients"
migrate_to_mongodb(healthcare_dict,db_name, collection_name)



