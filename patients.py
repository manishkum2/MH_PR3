from db_config import get_db_connection
from person import Person
from datetime import datetime,date
from formatting_var import single_dash_length
from tabulate import tabulate
class Patient(Person):
    def __init__(self, patient_id, name, age, gender, admission_date, contact_no):
        super().__init__(name, contact_no)
        self.id = patient_id
        self.age = age
        self.gender = gender
        self.admission_date = admission_date

    def add_patient(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        print("-"*single_dash_length)
        try:
            cursor.execute(
                """
                INSERT INTO patients (patient_id, name, age, gender, admission_date, contact_no)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (self.id, self.name, self.age, self.gender, self.admission_date, self.contact_no)
            )
            conn.commit()
            
            print(f"\nPatient added successfully:")
            print(f" ID: {self.id}")
            print(f" Name: {self.name}")
            print(f" Age: {self.age}")
            print(f" Gender: {self.gender}")
            print(f" Admission Date: {self.admission_date}")
            print(f" Contact No: {self.contact_no}")
            
        except Exception as e:
            print("Error creating patient:", e)
        finally:
            cursor.close()
            conn.close()
            print("-"*single_dash_length)


    @staticmethod
    def view_patient(patient_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            result = cursor.fetchone()
            if result:
                print("\nPatient found:\n")
                table_data = [[key.capitalize(), str(value)] for key, value in result.items()]
                print(tabulate(table_data, headers=["Field", "Value"], tablefmt="grid"))
            else:
                print(f"\nNo patient found with ID = {patient_id}")
            return result
        except Exception as e:
            print("Error reading patient:", e)
            return None
        finally:
            cursor.close()
            conn.close()


    def update_patient(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        print("-"*single_dash_length)
        try:
            cursor.execute(
                """
                UPDATE patients
                SET name = %s, age = %s, gender = %s, admission_date = %s, contact_no = %s
                WHERE patient_id = %s
                """,
                (self.name, self.age, self.gender, self.admission_date, self.contact_no, self.id)
            )
            conn.commit()
            print(f"\nPatient updated successfully:")
            print(f" ID: {self.id}")
            print(f" Name: {self.name}")
            print(f" Age: {self.age}")
            print(f" Gender: {self.gender}")
            print(f" Admission Date: {self.admission_date}")
            print(f" Contact No: {self.contact_no}")
        except Exception as e:
            print("Error updating patient:", e)
        finally:
            cursor.close()
            conn.close()
            print("-"*single_dash_length)

    @staticmethod
    def delete_patient(patient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        print("-"*single_dash_length)
        try:
            cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
            conn.commit()
            print(f"\nPatient with ID = {patient_id} has been deleted.")
        except Exception as e:
            print("Error deleting patient:", e)
        finally:
            cursor.close()
            conn.close()
            print("-"*single_dash_length)


    @staticmethod
    def search_patients(p_name):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        print("-" * 60)
        try:
            query = "SELECT patient_id, name, age, gender, contact_no FROM patients WHERE name LIKE %s"
            cursor.execute(query, (f'%{p_name}%',))
            results = cursor.fetchall()
            if results:
                print(f"\nFound {len(results)} patient(s):\n")
                table = tabulate(
                    results,
                    headers={"patient_id": "ID", "name": "Name", "age": "Age", "gender": "Gender", "contact_no": "Contact"},
                    tablefmt="grid"
                )
                print(table)
            else:
                print("\nNo matching patients found.")
            return results
        except Exception as e:
            print("Error searching patients:", e)
            return []
        finally:
            cursor.close()
            conn.close()
            print("-" * 60)


    @staticmethod
    def get_days_admitted_from_db(patient_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        print("-"*single_dash_length)
        try:
            cursor.execute("SELECT admission_date FROM patients WHERE patient_id = %s", (patient_id,))
            result = cursor.fetchone()
            if result and result['admission_date']:
                admission_date = result['admission_date']
                days = (datetime.today().date() - admission_date).days
                return days
            else:
                print("No admission date found.")
                return None
        except Exception as e:
            print("Error fetching admission date:", e)
            return None
        finally:
            cursor.close()
            conn.close()
            print("-"*single_dash_length)

    @staticmethod
    def get_days_between_appointments_from_db(patient_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        print("-"*single_dash_length)
        try:
            cursor.execute("""
                SELECT a_date FROM appointments 
                WHERE patient_id = %s ORDER BY a_date
            """, (patient_id,))
            results = cursor.fetchall()
            if len(results) >= 2:
                date1 = results[0]['a_date']
                date2 = results[1]['a_date']
                return abs((date2 - date1).days)
            else:
                print("Not enough appointments to calculate difference.")
                return None
        except Exception as e:
            print("Error fetching appointments:", e)
            return None
        finally:
            cursor.close()
            conn.close()
            print("-"*single_dash_length)
