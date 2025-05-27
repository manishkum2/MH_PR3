from db_config import get_db_connection
from datetime import date
from validations import *
from tabulate import tabulate
class PatientBillingTracker:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(dictionary=True)
        self.services = {}
        self.consulting_charge=0


    def fetch_services(self, patient_id):
        query = ''' 
            SELECT ps.service_id, s.service_name, s.cost
            FROM patient_services ps
            JOIN services s ON ps.service_id = s.service_id
            LEFT JOIN billing b ON ps.patient_id = b.patient_id
            WHERE ps.patient_id = %s;
        '''
        self.cursor.execute(query, (patient_id,))
        results = self.cursor.fetchall()

        if results:
            print("\nServices Found as follows:\n")
            self.services = {}  # Ensure it's initialized

            table_data = []
            for service in results:
                self.services[service["service_id"]] = {
                    "name": service["service_name"],
                    "cost": service["cost"],
                }
                table_data.append([
                    service["service_id"],
                    service["service_name"],
                    f"₹{service['cost']}"
                ])

            print(tabulate(
                table_data,
                headers=["Service ID", "Service Name", "Cost"],
                tablefmt="grid"
            ))
            print(f"\nFetched {len(self.services)} services for patient ID {patient_id}")
        else:
            print("No services found.")


    def compute_total(self):
        consulting_charge = get_valid_cost() 
        self.consulting_charge = float(consulting_charge)
        total = sum(float(service["cost"]) for service in self.services.values())
        return total + self.consulting_charge

    def insert_billing(self, patient_id, total_amount):
        try:
            
            if not check_patient_exists(patient_id):
                print(f"Error: Patient with ID {patient_id} does not exist.")
                return

            
            while True:
                bill_id = get_valid_bill_id()
                if check_bill_exists(bill_id) > 0:
                    print("Error: Bill ID already exists. Please use a different Bill ID.")
                else:
                    break
                

            
            today = date.today().isoformat()
            query = """
                INSERT INTO billing (bill_id, patient_id, total_amount, billing_date)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (bill_id, patient_id, total_amount, today))
            self.conn.commit()
            print(f"Billing record inserted: {bill_id} for ₹{total_amount}")

            
            while True:
                user_input = input("Do you want to generate an invoice as well? (yes/no): ").strip().lower()
                if user_input == 'yes':
                    self.generate_invoice(patient_id)
                    break
                elif user_input == 'no':
                    print("Okay, you chose not to generate an invoice.")
                    break
                else:
                    print("Please enter a valid choice (yes/no).")

        except Exception as e:
            print("An error occurred while inserting billing information.")
            print(f"Details: {e}")



    def fetch_patient_history(self, patient_id):
        if check_patient_exists(patient_id):
            try:
                print(f"\nAppointment history for patient ID: {patient_id}")
                self.cursor.execute('''
                    SELECT appt_id, p.patient_id, p.name AS PatientName, 
                        d.doctor_id, d.name AS DoctorName, diagnosis, a_date
                    FROM appointments a 
                    JOIN doctors d ON a.doctor_id = d.doctor_id
                    JOIN patients p ON p.patient_id = a.patient_id
                    WHERE p.patient_id = %s
                ''', (patient_id,))
                appointments = self.cursor.fetchall()

                if appointments:
                    print(tabulate(
                        appointments,
                        headers={
                            "appt_id": "Appointment ID",
                            "patient_id": "Patient ID",
                            "PatientName": "Patient Name",
                            "doctor_id": "Doctor ID",
                            "DoctorName": "Doctor Name",
                            "diagnosis": "Diagnosis",
                            "a_date": "Date"
                        },
                        tablefmt="grid"
                    ))
                else:
                    print("No appointment history found.")

                print("\nServices taken by patient:")
                self.cursor.execute('''
                    SELECT ps.service_id, s.service_name 
                    FROM services AS s
                    JOIN patient_services AS ps ON s.service_id = ps.service_id
                    WHERE ps.patient_id = %s
                ''', (patient_id,))
                services = self.cursor.fetchall()

                if services:
                    print(tabulate(
                        services,
                        headers={"service_id": "Service ID", "service_name": "Service Name"},
                        tablefmt="grid"
                    ))
                else:
                    print("No services found for this patient.")

            except Exception as e:
                print("ERROR: Couldn't fetch patient's history.", e)
        else:
            print("Patient doesn't exist.")

    def generate_invoice(self, patient_id):
        
        self.cursor.execute("SELECT patient_id, name, gender, admission_date FROM patients WHERE patient_id = %s", (patient_id,))
        patient = self.cursor.fetchone()

        self.cursor.execute("""
            SELECT 
                b.bill_id, 
                b.total_amount, 
                b.billing_date,
                a.diagnosis as daignosis,
                a.a_date AS appointment_date
            FROM billing b
            JOIN appointments a ON b.patient_id = a.patient_id
            WHERE b.patient_id = %s
            ORDER BY b.billing_date DESC
            LIMIT 1
        """, (patient_id,))

        billing = self.cursor.fetchone()

        if not patient or not billing:
            print("Error: Could not retrieve patient or billing information.")
            return
        print(type(patient))
        
        patient_id = patient['patient_id']
        name = patient['name']
        gender = patient['gender']
        admission_date = patient['admission_date']
        bill_id = billing['bill_id']
        total_amount = billing['total_amount']
        billing_date = billing['billing_date']
        apt_date=billing['appointment_date']
        daignosis=billing['daignosis']
        
        invoice_lines = [
            f"{'='*60}",
            f"{'INVOICE':^60}",
            f"{'='*60}",
            f"Bill ID         : {bill_id}",
            f"Patient ID      : {patient_id}",
            f"Patient Name    : {name}",
            f"Admission Date in Hospital    : {admission_date}",
            f"Gender          : {gender}",
            f"Billing Date          : {apt_date}",
            f"Appointment Date          : {billing_date}",
            f"Daignosed by    : {daignosis}",
            f"Amount (Rs.)      : {total_amount}",
            f"{'='*60}",
            f"{'Thank you for your visit!':^60}",
            f"{'='*60}"
        ]
        print(f"INVOICE generated in Hospital_management_system\output\invoices\{patient_id}.txt")
        invoice_text = "\n".join(invoice_lines)
        file_path = f"output/invoices/invoice_{patient_id}.txt"
        with open(file_path, "w") as file:
            file.write(invoice_text)    

    def close(self):
        self.cursor.close()
        self.conn.close()

