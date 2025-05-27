from db_config import get_db_connection

import pandas as pd

def daily_visits_report():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a_date, COUNT(*) AS total_visits
            FROM appointments
            GROUP BY a_date
            ORDER BY a_date DESC
        """)
        results = cursor.fetchall()
        print("\n Daily Visits Report:")
        for row in results:
            print(f"{row[0]}: {row[1]} Patient(s) visit")
    except Exception as e:
        print(" Error generating report:", e)
    finally:
        cursor.close()
        conn.close()

def most_consulted_doctors_report():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT d.doctor_id, d.name, COUNT(*) AS total_appointments
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            GROUP BY d.doctor_id, d.name
            ORDER BY total_appointments DESC
            LIMIT 5
        """)
        results = cursor.fetchall()
        print("\n Most Consulted Doctors:")
        for row in results:
            print(f"Dr. {row[1]} (ID {row[0]}) has  {row[2]} appointment(s)")
    except Exception as e:
        print(" Error generating report:", e)
    finally:
        cursor.close()
        conn.close()


def export_billing_to_csv(file_path):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        
        cursor.execute("SELECT * FROM billing")
        billing = cursor.fetchall()

        if not billing:
            print(" No billing records found.")
            return

        
        billing_df = pd.DataFrame(billing)

        
        billing_df.to_csv(file_path, index=False)

        print(f" Billing data exported to {file_path}")
    except Exception as e:
        print(" Error exporting billing data:", e)
    finally:
        cursor.close()
        conn.close()

def export_appointments_to_csv(file_path):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        
        cursor.execute("SELECT * FROM appointments")
        appointments = cursor.fetchall()

        if not appointments:
            print(" No appointment records found.")
            return

        
        appointments_df = pd.DataFrame(appointments)

        
        appointments_df.to_csv(file_path, index=False)

        print(f" Appointments data exported to {file_path}")
    except Exception as e:
        print(" Error exporting appointments data:", e)
    finally:
        cursor.close()
        conn.close()
