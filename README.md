# Cademycode Subscriber Data Pipeline Update Process

## Introduction:

This pipeline is designed to cleanse, reorganise and reformat a provided database. The cleansing and reformatting is done within Jupyter Notebooks, which then creates a new database and CSV, this database is then opened in a Python file, which runs unit tests on the data, outputting this to a log, and a changelog. Finally, a bash script has been created, this will detect updates within the change log, and push them into a new 'production' folder.


## Project Structure:

```
C:\Users\maxpe\OneDrive\Documents\Codecademy\Cancelled Subscribers Automated Data Ingestion\subscriber-pipeline-starter-kit
├── /dev
│   ├── Subscriber Data Pipeline.ipynb   
│   ├── Cademycode.py                    
│   ├── cademycode.log                  
│   ├── changelog.log                    
│   ├── cademycode.db                 
│   ├── cademycode_cleaned.csv          
│   └── final_data.csv                  
│   └── update_production.sh              
│
└── /production                           
```                         

## File Descriptions:

**Subscriber Data Pipeline.ipynb** - This notebook cleanses and manipulates cademycode.db, condensing it into one organised table, it then resaves and updates cademycode.db.
**Cademycode.py** - This Python file connects to the cleansed cademycode.db, runs data cleansing and performs unit tests, it loggs to 'cademycode.log' and updates the 'changelog.log' file.
**cademycode.log** - This is the log showing the INFO statements from the .py script.
**changelog.log** - This log file records a new entey everytime 'Cademycode.py' is ran.
**cademycode.db** - This is the database that was originally cleansed in Jupyter, it is now the cleansed file.
**cademycode_cleaned.csv** - This is a csv format of the cleansed database.
**final_data.csv** - The original CSV file, showing the original data given.
**update_production.sh** - Bash script that checks for new entries in the 'changelog.log' file, moving files into the /production folder.

## Execution Instrctions:

1) Navigate to the correct directory, open and run the Subscriber Data Pipeline.ipynb to cleanse the data, generating the up to date database and csv file.

2) Run Cademycode.py, this will execute the relevant unit tests and log to 'cademycode.log' and 'changelog.log'

3) Run the bash script to check for new entries in changelog and move the files into the production directory (./update_production.sh)

## Summary:

This was my first large project, although I found this very challenging, I have learnt alot more apposed to studying theory. I particularly enjoyed the section within Jupyter, as the outputs show you the code changes in real time, which made me realise how useful this tool is for data maniuplation, from cleaning data, to splitting a cluttered address column into its retrospective parts. THis project will serve me will in the future, as I will always have it to refer back to.
