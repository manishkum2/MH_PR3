import re
from db_config import get_db_connection
from datetime import datetime,date


def get_today_date():
    print("Today's date entering as date.....")
    return date.today()

def get_apt_date():
    print("Enter appointment date (YYYY-MM-DD). It must be today or a future date.")
    while True:
        user_input = input("Enter Date: ").strip()
        try:
            entered_date = datetime.strptime(user_input, "%Y-%m-%d").date()
            if entered_date >= date.today():
                return entered_date
            else:
                print("Date must be today or in the future. Please try again.")
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")


def check_patient_exists(patient_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM Patients WHERE patient_id = %s",
            (patient_id,)
        )
        count = cursor.fetchone()[0]

        conn.close()
        return count > 0
    except Exception as e:
        print(f"Error validating patient ID: {e}")
        return False

def check_bill_exists(bill_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM Billing WHERE bill_id = %s",
            (bill_id,)
        )
        count = cursor.fetchone()[0]

        conn.close()
        return count > 0
    except Exception as e:
        print(f"Error validating bill ID: {e}")
        return False

def get_valid_patient_id():
    while True:
        pid = input("Enter Patient ID (PAT-XXXXXX): ").strip()
        if re.fullmatch(r"PAT-\d{6}", pid):
            return pid
        else:
            print("Invalid Patient ID. Format must be PAT- followed by 6 digits (e.g., PAT-123456).")

def get_valid_doctor_id():
    while True:
        did = input("Enter Doctor ID (DOC-XXXXXX): ").strip()
        if re.fullmatch(r"DOC-\d{6}", did):
            return did
        else:
            print("Invalid Doctor ID. Format must be DOC- followed by 6 digits (e.g., DOC-654321).")


def get_valid_appointment_id():
    while True:
        aid = input("Enter Appointment ID (APT-XXXXXX): ").strip()
        if re.fullmatch(r"APT-\d{6}", aid):
            return aid
        else:
            print("Invalid Appointment ID. Format must be APT- followed by 6 digits (e.g., APT-123456).")

def get_valid_bill_id():
    while True:
        bid = input("Enter Bill ID (BIL-XXXXXX): ").strip()
        if re.fullmatch(r"BIL-\d{6}", bid):
            return bid
        else:
            print(" Invalid Bill ID. Format must be BIL- followed by 6 digits (e.g., BIL-123456).")

def get_valid_name():
    while True:
        name = input("Enter Name: ").strip()
        if len(name) >= 2 and name.replace(" ", "").isalpha():
            return name
        else:
            print("Name must be at least 2 characters long and contain only letters.")


def get_valid_diagnosis():
    while True:
        name = input("Enter Diagnosis: ").strip()
        if len(name) >= 2 and name.replace(" ", "").isalpha():
            return name
        else:
            print("Diagnosis must be at least 2 characters long and contain only letters.")

def get_valid_age():
    while True:
        try:
            age = int(input("Enter Age: "))
            if 0 < age < 120:
                return age
            else:
                print("Age must be between 1 and 119.")
        except ValueError:
            print("Invalid input. Please enter a valid age.")

def get_valid_gender():
    while True:
        gender = input("Enter Gender (male/female/others): ").strip().lower()
        if gender in ["male", "female", "others"]:
            return gender
        else:
            print("Gender must be one of: male, female, others.")

def get_valid_admission_date():
    while True:
        adm_date = input("Enter Admission Date (YYYY-MM-DD): ")
        try:
            datetime.strptime(adm_date, "%Y-%m-%d")
            return adm_date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_valid_contact():
    while True:
        contact = input("Enter Contact: ").strip()
        if re.fullmatch(r"[1-9]\d{9}", contact):
            return contact
        else:
            print("Contact must be exactly 10 digits and must not start with zero.")



def get_valid_specialisation():  
    while True:
        name = input("Enter Specialisation: ").strip()
        if len(name) >= 2 and name.replace(" ", "").isalpha():
            return name
        else:
            print("Specialisation must be at least 2 characters long and contain only letters.")


def get_valid_service_id():
    while True:
        sid = input("Enter Service ID (format: SVC-XXXXXX): ").strip()
        if re.fullmatch(r"SVC-\d{6}", sid):
            return sid
        else:
            print("Invalid Service ID. It must be in the format SVC- followed by 6 digits.")


def get_valid_cost():
    while True:
        cost_input = input("Enter Cost (up to 2 decimal places): ").strip()
        try:
            cost = cost_input
            if re.fullmatch(r"\d+(\.\d{1,2})?", cost_input):
                return cost
            else:
                print("Cost must be a number with up to 2 decimal places.")
        except ValueError:
            print("Invalid input. Please enter a valid decimal number.")

