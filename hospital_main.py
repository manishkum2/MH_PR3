from patients import Patient 
from doctors import Doctor
from services import Services
from billing import Billing
from appointments import Appointment
from patient_billing_tracking import PatientBillingTracker
from validations import *
from others_information import *
from formatting_var import *

def main_menu():
    while True:
        print("\n" + "="*double_dash_length)
        print("              HOSPITAL MANAGEMENT SYSTEM")
        print("="*double_dash_length)
        print(" 1.  Patients")
        print(" 2.  Doctors")
        print(" 3.  Services")
        print(" 4.  Appointments")
        print(" 5.  Billing")
        print(" 6.  Patient Billing Tracking")
        print(" 7.  Reporting Menu")
        print(" 8.  Exporting Menu")
        print(" 0.  Exit")
        print("="*double_dash_length)

        choice = input("Select a module (0-8): ")

        if choice == '1':
            patient_menu()
        elif choice == '2':
            doctor_menu()
        elif choice == '3':
            service_menu()
        elif choice == '4':
            appointment_menu()
        elif choice == '5':
            billing_menu()
        elif choice == '6':
            billing_tracking_menu()
        elif choice == '7':
            reporting_menu()
        elif choice == '8':
            exporting_menu()
        elif choice == '0':
            print("\nGoodbye! Thank you for using the system.")
            break
        else:
            print("Invalid option. Please try again.")


def exporting_menu():
    print("\n" + "-"*single_dash_length)
    print("               EXPORTING MENU")
    print("-"*single_dash_length)
    print(" 1. Export billing to CSV")
    print(" 2. Export appointments to CSV")
    print(" 0. Back to Main Menu")
    print("-"*single_dash_length)

    choice = input("Select an option: ")

    if choice == '1':
        export_billing_to_csv("output/CSVs/billing_summary_1.csv")
    elif choice == '2':
        export_appointments_to_csv("output/CSVs/appointment_summary_1.csv")
    elif choice == '0':
        return
    else:
        print("Invalid option. Please try again.")

def reporting_menu():
    while True:
        print("\n" + "-"*50)
        print("               REPORTING MENU")
        print("-"*50)
        print(" 1. Daily Visits")
        print(" 2. Most Consulted Doctors")
        print(" 0. Back to Main Menu")
        print("-"*50)

        choice = input("Select an option: ")

        if choice == '1':
            daily_visits_report()
        elif choice == '2':
            most_consulted_doctors_report()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def billing_tracking_menu():
    while True:
        print("\n" + "-"*50)
        print("         PATIENT BILLING TRACKING MENU")
        print("-"*50)
        print(" 1. Track multiple services used by the patient")
        print(" 2. Insert billing for a patient")
        print(" 3. Compute total bill (without inserting)")
        print(" 4. View complete patient history")
        print(" 5. Generate detailed invoice")
        print(" 0. Back to Main Menu")
        print("-"*50)

        choice = input("Select an option: ")

        if choice == '1':
            patient_id = get_valid_patient_id()
            tracker = PatientBillingTracker()
            tracker.fetch_services(patient_id)
            tracker.close()

        elif choice == '2':
            patient_id = get_valid_patient_id()
            tracker = PatientBillingTracker()
            tracker.fetch_services(patient_id)
            total = tracker.compute_total()
            tracker.insert_billing(patient_id, total)
            tracker.close()

        elif choice == '3':
            patient_id = get_valid_patient_id()
            tracker = PatientBillingTracker()
            tracker.fetch_services(patient_id)
            total = tracker.compute_total()
            print(f"Total bill for patient {patient_id} (including consulting charge): ₹{total}")
            tracker.close()

        elif choice == '4':
            patient_id = get_valid_patient_id()
            tracker = PatientBillingTracker()
            tracker.fetch_patient_history(patient_id)
            tracker.close()

        elif choice == '5':
            patient_id = input("Enter Patient ID: ").strip()
            tracker = PatientBillingTracker()
            tracker.generate_invoice(patient_id)
            tracker.close()

        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def patient_menu():
    while True:
        print("\n" + "-"*50)
        print("                 PATIENT MENU")
        print("-"*50)
        print(" 1. Add Patient")
        print(" 2. View Patient")
        print(" 3. Update Patient")
        print(" 4. Delete Patient")
        print(" 5. Days Admitted")
        print(" 6. Days Between Appointments")
        print(" 7. Search Patient by Name")
        print(" 0. Back to Main Menu")
        print("-"*50)

        choice = input("Select an option: ")

        if choice == '1':
            patient_id = get_valid_patient_id()
            try:
                if not check_patient_exists(patient_id) and patient_id:
                    name = get_valid_name()
                    age = get_valid_age()
                    gender =get_valid_gender()
                    adm_date = get_today_date()
                    contact_no =  get_valid_contact()
                    Patient(patient_id, name, age, gender, adm_date, contact_no).add_patient()
                else:
                    raise ValueError("Patient ID exists.")
            except Exception as e:
                print("Patient ID exists. Try another one.")
                
            
        elif choice == '2':
            patient_id = get_valid_patient_id()
            Patient.view_patient(patient_id)

        elif choice == '3':
            patient_id = get_valid_patient_id()
            name = get_valid_name()
            age = get_valid_age()
            gender = get_valid_gender()
            adm_date = get_today_date()
            contact = get_valid_contact()
            Patient(patient_id, name, age, gender, adm_date, contact).update_patient()

        elif choice == '4':
            patient_id = get_valid_patient_id()
            Patient.delete_patient(patient_id)

        elif choice == '5':
            patient_id = get_valid_patient_id()
            data = Patient.view_patient(patient_id)
            if data:
                patient = Patient(data['patient_id'], data['name'], data['age'], data['gender'], str(data['admission_date']), data['contact_no'])
                days = patient.get_days_admitted_from_db(patient_id)
                if days is not None:
                    print(f"Patient has been admitted for {days} day(s).")

        elif choice == '6':
            patient_id = get_valid_patient_id()
            days = Patient.get_days_between_appointments_from_db(patient_id)
            if days is not None:
                print(f"Days between appointments: {days} day(s)")

        elif choice == '7':
            patient_name = get_valid_name()
            Patient.search_patients(patient_name)

        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")

def doctor_menu():
    while True:
        print("\n" + "-"*50)
        print("                 DOCTOR MENU")
        print("-"*50)
        print(" 1. Add Doctor")
        print(" 2. View Doctor")
        print(" 3. Update Doctor")
        print(" 4. Delete Doctor")
        print(" 5. Search Doctor by Name")
        print(" 0. Back to Main Menu")
        print("-"*50)

        choice = input("Select an option: ")

        if choice == '1':
            doctor_id = get_valid_doctor_id()
            name = get_valid_name()
            specialty = get_valid_specialisation()
            contact_num = get_valid_contact()
            Doctor(doctor_id, name, specialty, contact_num).add_doctor()

        elif choice == '2':
            doctor_id = get_valid_doctor_id()
            Doctor.view_doctor(doctor_id)

        elif choice == '3':
            doctor_id = get_valid_doctor_id()
            name = get_valid_name()
            specialty = get_valid_specialisation()
            contact_num = get_valid_contact()
            Doctor(doctor_id, name, specialty, contact_num).update_doctor()

        elif choice == '4':
            doctor_id = get_valid_doctor_id()
            Doctor.delete_doctor(doctor_id)

        elif choice == '5':
            doctor_name = get_valid_name()
            Doctor.search_doctors(doctor_name)  

        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def service_menu():
    while True:
        print("\n" + "-"*50)
        print("                 SERVICE MENU")
        print("-"*50)
        print(" 1. Add Service")
        print(" 2. View Service")
        print(" 3. Update Service")
        print(" 4. Delete Service")
        print(" 5. View All Service")
        print(" 6. Assign Services to patient")
        print(" 0. Back to Main Menu")
        print("-"*50)

        choice = input("Select an option: ")

        if choice == '1':
            service_id = get_valid_service_id()
            name = get_valid_name()
            cost = get_valid_cost()
            Services(service_id, name, cost).add_service()

        elif choice == '2':
            service_id = get_valid_service_id()
            Services.view_service(service_id)
            # Services.view_all_service()

        elif choice == '3':
            service_id = get_valid_service_id()
            name = get_valid_name()
            cost = get_valid_cost()
            Services(service_id, name, cost).update_service()

        elif choice == '4':
            service_id = get_valid_service_id()
            Services.delete_service(service_id)
        elif choice == '5':
            Services.view_all_service()
        elif choice=='6':
            Services.assign_service_to_patient()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def appointment_menu():
    while True:
        print("\n" + "-"*50)
        print("              APPOINTMENT MENU")
        print("-"*50)
        print(" 1. Add Appointment")
        print(" 2. View Appointment")
        print(" 3. Update Appointment")
        print(" 4. Delete Appointment")
        print(" 5. View Appointments Today")
        print(" 6. View Appointments Last Week")
        print(" 7. View Appointments in Date Range")
        print(" 0. Back to Main Menu")
        print("-"*50)

        choice = input("Select an option: ")

        if choice == '1':
            appointment_id = get_valid_appointment_id()
            patient_id = get_valid_patient_id()
            doctor_id = get_valid_doctor_id()
            date =get_apt_date()
            diagnosis = get_valid_diagnosis()
            Appointment(appointment_id, patient_id, doctor_id, date, diagnosis).add_appointment()

        elif choice == '2':
            appointment_id = get_valid_appointment_id()
            Appointment.view_appointment(appointment_id)

        elif choice == '3':
            appointment_id = get_valid_appointment_id()
            patient_id = get_valid_patient_id()
            doctor_id = get_valid_doctor_id()
            date = get_apt_date()
            diagnosis = get_valid_diagnosis()
            Appointment(appointment_id, patient_id, doctor_id, date, diagnosis).update_appointment()

        elif choice == '4':
            appointment_id = get_valid_appointment_id()
            Appointment.delete_appointment(appointment_id)

        elif choice == '5':
            Appointment.appointments_today()

        elif choice == '6':
            Appointment.appointments_last_week()

        elif choice == '7':
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            Appointment.filter_appointments_by_date_range(start_date, end_date)

        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def billing_menu():
    while True:
        print("\n" + "-"*50)
        print("                 BILLING MENU")
        print("-"*50)
        print(" 1. View Bill")
        print(" 2. Update Bill")
        print(" 3. Delete Bill")
        print(" 0. Back to Main Menu")
        print("-"*50)

        choice = input("Select an option: ")

        if choice == '1':
            bill_id = get_valid_bill_id()
            Billing.view_bill(bill_id)

        elif choice == '2':
            bill_id = get_valid_bill_id()
            patient_id = get_valid_patient_id()
            amount = get_valid_cost()
            billing_date = get_today_date()
            Billing(bill_id, patient_id, amount, billing_date).update_bill()

        elif choice == '3':
            bill_id = get_valid_bill_id()
            Billing.delete_bill(bill_id)

        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main_menu()
