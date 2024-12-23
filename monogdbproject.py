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
    try :
        #connect to MongoDB
        logging.info("connection to MongoDB...")
        client=MongoClient('mongodb://localhost:27017/')
        db = client[db_name]
        collection = db[collection_name]
        logging.info("Connected to MongoDB successfully")

        #insert data into MongoDB
        logging.info(f"Inserting {len(data)} records into MongoDB...")
        collection.insert_many(data)
        logging.info("Data inserted successfully")

        # Display a few records
        logging.info("Fetching sample records...")
        for document in collection.find().limit(5):
            logging.info(document)

    except Exception as e:
        logging.error(f"An error occurred: {e}")


#Migrate data
db_name = 'healthcare'
collection_name = "patients"
migrate_to_mongodb(healthcare_dict,db_name, collection_name)
