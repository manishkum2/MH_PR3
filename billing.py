from db_config import get_db_connection

class Billing:
    def __init__(self, bill_id, patient_id, total_amount, billing_date):
        self.bill_id = bill_id
        self.patient_id = patient_id
        self.total_amount = total_amount
        self.billing_date = billing_date

    @staticmethod
    def view_bill(bill_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM billing WHERE bill_id = %s", (bill_id,))
            result = cursor.fetchone()
            if result:
                print(f" Bill found: {result}")
            else:
                print(f" No bill found with ID={bill_id}")
            return result
        except Exception as e:
            print(" Error reading bill:", e)
            return None
        finally:
            cursor.close()
            conn.close()

    def update_bill(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE billing SET patient_id = %s, total_amount = %s, billing_date = %s WHERE bill_id = %s",
                (self.patient_id, self.total_amount, self.billing_date, self.bill_id)
            )
            conn.commit()
            print(f" Bill updated: ID={self.bill_id}, Patient ID={self.patient_id}, Amount=₹{self.total_amount}, Date={self.billing_date}")
        except Exception as e:
            print(" Error updating bill:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_bill(bill_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM billing WHERE bill_id = %s", (bill_id,))
            conn.commit()
            print(f" Bill with ID={bill_id} has been deleted.")
        except Exception as e:
            print(" Error deleting bill:", e)
        finally:
            cursor.close()
            conn.close()
