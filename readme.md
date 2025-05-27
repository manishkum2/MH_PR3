	=========Hospital Patient Record & Billing System (CLI APP)=========

Welcome to the Hospital Patient Record & Billing System! This is a simple, menu-driven command-line application built with Core Python and MySQL/MS SQL Server.
It helps hospitals manage patients, doctors, services, appointments, and billing — with features like automated bill generation, patient tracking, and service recording.

## Features:
    -> Patient Management (Add, Update, Delete, Search, View, Calculate Days Admitted, days between appointments)

    -> Doctor Management with Specialization and Contact Info

    -> Appointment Management with Diagnosis Recording(Filter appointments by date,last week appointments)

    -> Service Management (Add/View/Delete Medical Services and Costs)

    -> Automated Billing Generation Based on Services Used

    -> Daily Reports for Appointments and Billing

    -> CSV Backup for Appointments, and Billing

    -> Clean CLI Dashboard Navigation
 
 
## Techincal Requirements:
        -> Programming Language: Python 3.x
        -> Database:  MySQL Workbench
        -> Libraries:
            > mysql.connector – for MySQL Workbench connection
            > datetime, decimal, os, re – core modules
 |
 
## Project Structure:
hospital_mgmt/
	├── db_config.py # DB connection logic
	├── patients.py # Patient class
	├── appointments.py # Appointment class
	├── doctors.py # Doctor class
	├── services.py # Services logic
	├── patient_billing_tracking.py # Billing logic
	├── hospital_main.py # Main menu & CLI
	├── requirements.txt # List of required libraries	
	├── validations.py # List of validations used		
	├── output/
	│ └── invoices/
	│ 	└── invoice_PAT-100009.txt
	│ └── CSVs/
	│ 	└── appointment_summary_1.csv
	└── README.md

## Setup Instructions:
        1. Install Dependencies:
            Ensure Python 3 is installed, then install mysql.connector:
                -> pip install mysql.connector        #run this in CLI
 
        2. Configure  MySQL Workbench:
            -> Create a database named hospital in MYSQL.
 
            -> Set up the required tables (patients, doctors,services, appointments, billing).
		patients:
		patient_id, name, age, gender, admission_date, contact_no

		doctors:
		doctor_id, name, specialization, contact_no

		services:
		service_id, service_name, cost

		appointments:
		appt_id, patient_id, doctor_id, date, diagnosis

		billing:
		bill_id, patient_id, total_amount, billing_date
 
            -> Ensure Trusted_Connection=yes is configured for local integrated authentication and it will be connected with windows user       credentials.
 
        3. connect  MySQL Workbench with python using mysql.connector  library
 
        4. Run the application in CLI and Use the CLI dashboard to manage patients, doctors, appointments, services etc
 
 
## CSV and Invoice Files:
        -> CSV exports and imports are saved in:
           path = C:\Users\manish.kumar30\RLL_ProjectManish\Hospital_management_system\output\CSVs
 
        -> Invoices are stored in:
             path = C:\Users\manish.kumar30\RLL_ProjectManish\Hospital_management_system\output\invoices
 
        These are my path directories (if we want you can defaultly update the paths)
 
 
## Smart Features:
        -> Using PAT-XXXXXX as PatientID, APT-XXXXXX as AppointmentID so on
 
        -> Validates IDs, names, phone numbers,cost etc
 
        -> Tabular form Data fetching while searching Doctors,patients by name
 
        -> Saves invoices in outputs folder
 
        -> gives warning when entering duplicate IDs
 
        -> handles CSV imports/exports easily by giving filename or path