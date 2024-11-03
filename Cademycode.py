import sqlite3 
import pandas as pd   
import json
import numpy as np    
import os    
from datetime import datetime
import logging
import unittest    

# Change the working directory
os.chdir(r"C:\Users\maxpe\OneDrive\Documents\Codecademy\Cancelled Subscribers Automated Data Ingestion\subscriber-pipeline-starter-kit\dev") 

# Set up logging configuration to log details to a file
logging.basicConfig(
    filename="cademycode.log",  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  
    filemode="w", 
    level=logging.DEBUG,  
    force=True  
)
logger = logging.getLogger(__name__)  # Create a logger for this module

# Set up a changelog which will be used to record updates and changes to the file
changelog = logging.getLogger("changelog")
changelog_handler = logging.FileHandler("changelog.log", mode="a")  
changelog.addHandler(changelog_handler) 

# This connects to my cademycode.db to run the tests on
def connect_to_db(db_name="cademycode.db"):
    # Attempts to connect to the database, it will create a log to show if it is successful or not.
    try:
        conn = sqlite3.connect(db_name)  
        logger.info("Successfully connected to the database.")  
        return conn  
    except sqlite3.Error as e:  
        logger.error(f"Failed to connect to database: {e}")  
        return None  

# Function to clean the students data, as well as statements for the logger
def cleanse_students(df):
    logger.info("Started cleaning students data.")  
    df['dob'] = pd.to_datetime(df['dob'], errors='coerce')  
    df['age'] = (datetime.now() - df['dob']).dt.days // 365  
    df.dropna(subset=['dob'], inplace=True) 
    logger.info(f"Dropped rows with invalid DOB. Current rows: {len(df)}")  

    
    def parse_contact_info(info):
        parsed_info = json.loads(info) 
        mailing_address = parsed_info['mailing_address'] 
        address_parts = mailing_address.split(', ')  
        if len(address_parts) == 4: 
            street = address_parts[0]
            city = address_parts[1]
            state = address_parts[2]
            post_code = address_parts[3]
        
        email = parsed_info['email']  
        return pd.Series([street, city, state, post_code, email])  

   
    df[['street', 'city', 'state', 'post_code', 'email']] = df['contact_info'].apply(parse_contact_info)
    df.drop(columns=['contact_info'], inplace=True)  


    df['job_id'] = df['job_id'].astype(float)
    df['num_course_taken'] = df['num_course_taken'].astype(float)
    df['current_career_path_id'] = df['current_career_path_id'].astype(float)
    df['time_spent_hrs'] = df['time_spent_hrs'].astype(float)

   
    df = df.dropna(subset=['job_id', 'num_course_taken'])
    df['current_career_path_id'].fillna(0, inplace=True) 
    df['time_spent_hrs'].fillna(0, inplace=True)  

    logger.info("Finished cleaning students data.")  
    return df 

# Function to clean course data as well as logger statements
def cleanse_course_data(df):
    logger.info("Started cleaning course data.") 
    not_applicable = {
        'career_path_id': 0,
        'career_path_name': 'Not Applicable',
        'hours_to_complete': 0
    }
    not_applicable_df = pd.DataFrame([not_applicable]) 
    df = pd.concat([df, not_applicable_df], ignore_index=True) 
    logger.info("Finished cleaning course data.")  
    return df  

# Function to clean student jobs data as well as logger statements
def cleanse_student_jobs(df):
    logger.info("Started cleaning student jobs data.")  
    df = df.drop_duplicates()  
    logger.info("Finished cleaning student jobs data.")  
    return df  

# Function to log changes in the changelog file, showing the version number and row count
def log_changelog(version, row_count):
    changelog.info(f"Version {version} - Rows Processed: {row_count} - Date: {datetime.now().strftime('%Y-%m-%d')}")

# Unit testing class for data cleaning functions
# it will connect to cademycode.db before each test, and will create a log to show the data has been loaded
# tearDown will close the connection after each test to create a consistent testing format
class TestDataCleaning(unittest.TestCase):
    def setUp(self):
        self.conn = connect_to_db()  
        self.merged_df = pd.read_sql_query("SELECT * FROM cademycode_cleaned", self.conn)  
        self.merged_df['dob'] = pd.to_datetime(self.merged_df['dob'], errors='coerce')
        logger.info("Test data loaded.") 

    def tearDown(self):
        self.conn.close()  
        logger.info("Database connection closed after tests.") 
    # Tests for null values throughout the database, and will log if the test passes.
    def test_no_null_values(self):
        """Check that there are no null values in any column."""
        for column in self.merged_df.columns:  # Iterate through all columns
            with self.subTest(column=column):  # Create a sub-test for each column
                self.assertFalse(self.merged_df[column].isnull().any(), f"Null values found in {column}.")  # Assert no null values
        logger.info("Null values test passed.")  # Log that null values test passed

    # Compares data types to expected datatypes
    def test_correct_data_types(self):
        expected_types = {
            'uuid': 'int64',
            'name': 'object',
            'dob': 'datetime64[ns]',
            'sex': 'object',
            'job_id': 'float64',
            'num_course_taken': 'float64',
            'current_career_path_id': 'float64',
            'time_spent_hrs': 'float64',
            'age': 'int64',
            'street': 'object',
            'city': 'object',
            'state': 'object',
            'post_code': 'object',
            'email': 'object',
            'career_path_id': 'int64',
            'career_path_name': 'object',
            'hours_to_complete': 'int64',
            'job_category': 'object',
            'avg_salary': 'int64'
        }
        for column, dtype in expected_types.items():  
            with self.subTest(column=column):  
                self.assertTrue(self.merged_df[column].dtype == dtype, f"{column} should be {dtype}.")  
        logger.info("Data type test passed.")  

    # Checks certain columns for negative values, ensuring data integrity in the schema
    def test_data_integrity(self):
        """Verify logical consistency in the data, such as non-zero course taken counts where applicable."""  
        self.assertTrue((self.merged_df['num_course_taken'] >= 0).all(), "num_course_taken contains negative values.")  
        self.assertTrue((self.merged_df['time_spent_hrs'] >= 0).all(), "time_spent_hrs contains negative values.")  
        logger.info("Data integrity test passed.")  


if __name__ == "__main__":
    try:
        # Connect to database and run unit tests, creates a changelog entry whenever the script has been run
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            total_rows = cursor.execute("SELECT COUNT(*) FROM cademycode_cleaned").fetchone()[0]
            version = "1.0"  
            log_changelog(version, total_rows)  
            unittest.main()  
        else:
            logger.error("Database connection could not be established. Exiting.")
    except SystemExit as e:  
        logger
