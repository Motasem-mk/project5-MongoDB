## **MongoDB Data Migration Project**

### **Project Overview**
This project demonstrates the use of Python for migrating healthcare data from a CSV file to a MongoDB database. The project incorporates functionality for performing CRUD (Create, Read, Update, Delete) operations on the MongoDB database and uses Docker to containerize both the Python script and the MongoDB instance for portability and scalability.

---

```markdown
## Prerequisites
- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed ([Install Docker Compose](https://docs.docker.com/compose/install/))

## Steps to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/Motasem-mk/project5-MongoDB.git
   cd project5-MongoDB
   ```

2. Run the migration:
   ```bash
   docker-compose up
   ```
   - This will:
     - Start a MongoDB container.
     - Build and run a Python container to migrate the data from the CSV file to MongoDB.

3. Verify the data:
   - Connect to MongoDB at `localhost:27017` using a MongoDB client (e.g., [MongoDB Compass](https://www.mongodb.com/products/compass)).
   - Check the database and collection specified in `mongodbproject.py`.

## Notes
- The CSV file (`healthcare_dataset.csv`) is included in the repository and will be used for the migration.
- MongoDB will be available at `localhost:27017`.
- The Python script (`mongodbproject.py`) reads the CSV file and inserts the data into MongoDB.

## Project Structure
```
project5-MongoDB/
├── Dockerfile
├── docker-compose.yml
├── healthcare_dataset.csv
├── mongodbproject.py
├── requirements.txt
└── README.md
```

## Troubleshooting
- If the migration fails, ensure that:
  - Docker and Docker Compose are installed correctly.
  - The CSV file (`healthcare_dataset.csv`) is present in the project directory.
  - MongoDB is running and accessible at `localhost:27017`.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### **Features**
1. **Data Migration**:
   - Reads healthcare data from a CSV file.
   - Cleans the dataset by removing duplicates and ensuring logical consistency.
   - Converts date fields to `datetime` format.
   - Inserts the cleaned data into MongoDB.


## **Data Integrity Checks**
Before and after migration, the script performs the following data integrity checks:
**Pre-migration checks**:
   - Missing values in essential fields.
   - Duplicates in the dataset.
   - Invalid dates (Discharge Date must be after Admission Date).
   - Negative values in key fields like Age and Billing Amount.
**Post-migration checks**:
   - Ensures the number of records in MongoDB matches the original dataset.
   - Verifies that required fields (e.g., Age, Medical Condition, Name) are present.
   - Checks that dates and numeric fields are logically consistent.


2. **CRUD Operations**:
   - **Create**: Add new records to the database.
   - **Read**: Query records based on specific criteria.
   - **Update**: Modify existing records.
   - **Delete**: Remove records from the database.

3. **Containerization**:
   - A `Dockerfile` to containerize the Python script for migration and CRUD operations.
   - A `docker-compose.yml` to manage the MongoDB and Python containers.

---

### **Authentication System and User Roles**

#### **MongoDB Authentication**
MongoDB uses role-based access control (RBAC) to manage user permissions. For this project, authentication is enabled, and the **admin user** has full access to the MongoDB instance.

- **Admin User**:
  - **Username**: `admin`
  - **Password**: `motasem`
  - **Role**: `root` (Full administrative access to MongoDB)
  - This user is responsible for managing all aspects of MongoDB, including user creation and database management.
  
- **MongoDB Roles**:
  - **`root`**: Full administrative control over the MongoDB instance, including creating users, managing databases, and running all administrative commands.
  - **Authentication** is enabled, so you must provide the **admin credentials** (`admin:motasem`) when connecting to MongoDB.

---

### **Database Schema**

#### **Database: `healthcare`**
The `healthcare` database contains the following **patients** collection.

- **Collection Name**: `patients`

##### **Fields in the `patients` Collection**:
- **`Name`** (string): Patient's full name.
- **`Age`** (integer): Patient's age.
- **`Gender`** (string): Patient's gender.
- **`Blood Type`** (string): Patient's blood type.
- **`Medical Condition`** (string): Medical condition diagnosis.
- **`Date of Admission`** (datetime): Date the patient was admitted.
- **`Discharge Date`** (datetime): Date the patient was discharged.
- **`Doctor`** (string): Name of the attending doctor.
- **`Room Number`** (integer): Room number assigned to the patient.
- **`Billing Amount`** (float): Billing amount for the treatment.
- **`Admission Type`** (string): Type of admission (e.g., Routine, Emergency).
- **`Insurance Provider`** (string): The insurance company providing coverage.
- **`Medication`** (string): Medication prescribed to the patient.
- **`Test Results`** (string): Results of medical tests conducted.

The schema is simple, focusing on patient details and hospital admission information.

---



---

### **CRUD Operations**

#### **Create a Record**
Adds a new patient record to the database.
Example:
```python
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
```

#### **Read Records**
Query records from the database.
Example:
```python
query = {"Age": {"$gte": 87}}
read_patient_records(collection, query)
```

#### **Update Records**
Modify existing records in the database.
Example:
```python
query = {"Name": "Alice Brown"}
update_fields = {"Room Number": 203, "Billing Amount": 12000}
update_patient_record(collection, query, update_fields)
```

#### **Delete Records**
Remove records from the database.
Example:
```python
query = {"Name": "Alice Brown"}
delete_patient_records(collection, query)
```

---

### **Purpose of Docker Compose**
Docker Compose allows you to define and run multi-container Docker applications. In this project:
- MongoDB runs in one container.
- The Python script runs in another container.
- The two containers communicate through a Docker network.

---

## **Author**
Motasem Abualqumboz

For more information, refer to the [GitHub Repository](https://github.com/Motasem-mk/project5-MongoDB).

