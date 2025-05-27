
from db_config import get_db_connection
from person import Person
from tabulate import tabulate
class Doctor(Person):
    def __init__(self, doctor_id, name, specialization, contact_no):
        super().__init__(name,contact_no)
        self.id = doctor_id
        self.specialization = specialization
        

    def add_doctor(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO doctors (doctor_id, name, specialization, contact_no) VALUES (%s, %s, %s, %s)",
                (self.id, self.name, self.specialization, self.contact_no)
            )
            conn.commit()
            print(f" Doctor added: ID={self.id} | Name={self.name} | Specialization={self.specialization} | Contact No={self.contact_no}")
        except Exception as e:
            print(" Error creating doctor:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def view_doctor(doctor_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
            result = cursor.fetchone()
            if result:
                print(f" Doctor found: {result}")
            else:
                print(f"⚠️ No doctor found with ID={doctor_id}")
            return result
        except Exception as e:
            print(" Error reading doctor:", e)
            return None
        finally:
            cursor.close()
            conn.close()

    def update_doctor(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE doctors SET name = %s, specialization = %s, contact_no = %s WHERE doctor_id = %s",
                (self.name, self.specialization, self.contact_no, self.id)
            )
            conn.commit()
            print(f" Doctor updated: ID={self.id}, Name={self.name}, Specialization={self.specialization}, Contact No={self.contact_no}")
        except Exception as e:
            print(" Error updating doctor:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_doctor(doctor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,))
            conn.commit()
            print(f" Doctor with ID={doctor_id} has been deleted.")
        except Exception as e:
            print(" Error deleting doctor:", e)
        finally:
            cursor.close()
            conn.close()
    
   

    @staticmethod
    def search_doctors(d_name):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT doctor_id, name, specialization, contact_no
                FROM doctors
                WHERE name LIKE %s
            """
            cursor.execute(query, (f'%{d_name}%',)) 
            results = cursor.fetchall()
            if results:
                print(f"\nFound {len(results)} doctor(s):\n")
                print(tabulate(
                    results,
                    headers={"doctor_id": "ID", "name": "Name", "specialization": "Specialization", "contact_no": "Contact"},
                    tablefmt="grid"
                ))
            else:
                print("No matching doctors found.")
            return results
        except Exception as e:
            print("Error searching doctors:", e)
            return []
        finally:
            cursor.close()
            conn.close()
