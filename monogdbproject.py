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