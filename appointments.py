from db_config import get_db_connection

from tabulate import tabulate
from datetime import date, timedelta

class Appointment:
    def __init__(self, appt_id, patient_id, doctor_id, date, diagnosis):
        self.appt_id = appt_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.a_date = date
        self.diagnosis = diagnosis

    def add_appointment(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO appointments (appt_id, patient_id, doctor_id, a_date, diagnosis) VALUES (%s, %s, %s, %s, %s)",
                (self.appt_id, self.patient_id, self.doctor_id, self.a_date, self.diagnosis)
            )
            conn.commit()
            print(f" Appointment created: ID={self.appt_id}, Patient ID={self.patient_id}, Doctor ID={self.doctor_id}, Date={self.a_date}, Diagnosis={self.diagnosis}")
        except Exception as e:
            print(" Error creating appointment:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def view_appointment(appt_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM appointments WHERE appt_id = %s", (appt_id,))
            result = cursor.fetchone()
            if result:
                print(f" Appointment found: {result}")
            else:
                print(f" No appointment found with ID={appt_id}")
            return result
        except Exception as e:
            print(" Error reading appointment:", e)
            return None
        finally:
            cursor.close()
            conn.close()

    def update_appointment(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE appointments SET patient_id = %s, doctor_id = %s, a_date = %s, diagnosis = %s WHERE appt_id = %s",
                (self.patient_id, self.doctor_id, self.a_date, self.diagnosis, self.appt_id)
            )
            conn.commit()
            print(f" Appointment updated: ID={self.appt_id}, Patient ID={self.patient_id}, Doctor ID={self.doctor_id}, Date={self.a_date}, Diagnosis={self.diagnosis}")
        except Exception as e:
            print(" Error updating appointment:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_appointment(appt_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM appointments WHERE appt_id = %s", (appt_id,))
            conn.commit()
            print(f" Appointment with ID={appt_id} has been deleted.")
        except Exception as e:
            print(" Error deleting appointment:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def filter_appointments_by_date_range(start_date, end_date):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM appointments WHERE a_date BETWEEN %s AND %s",
                (start_date, end_date)
            )
            results = cursor.fetchall()
            if results:
                print(f"\nAppointments from {start_date} to {end_date}:\n")
                print(tabulate(results, headers="keys", tablefmt="grid"))
            else:
                print(f"No appointments found between {start_date} and {end_date}.")
            return results
        except Exception as e:
            print("Error filtering appointments:", e)
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def appointments_today():
        today = date.today().isoformat()
        return Appointment.filter_appointments_by_date_range(today, today)

    @staticmethod
    def appointments_last_week():
        today = date.today()
        last_week = today - timedelta(days=7)
        return Appointment.filter_appointments_by_date_range(last_week.isoformat(), today.isoformat())
