from db_config import get_db_connection
from validations import *
from tabulate import tabulate

class Services:
    def __init__(self, service_id, service_name, cost):
        self.id = service_id
        self.name = service_name
        self.cost = cost

    def add_service(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO services (service_id, service_name, cost) VALUES (%s, %s, %s)",
                (self.id, self.name, self.cost)
            )
            conn.commit()
            print(f" Service added: ID={self.id}, Name={self.name}, Cost={self.cost}")
        except Exception as e:
            print(" Error creating service:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def view_service(service_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM services WHERE service_id = %s", (service_id,))
            result = cursor.fetchone()
            if result:
                print(f" Service found: {result}")
            else:
                print(f" No service found with ID={service_id}")
            return result
        except Exception as e:
            print(" Error reading service:", e)
            return None
        finally:
            cursor.close()
            conn.close()

    def update_service(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE services SET service_name = %s, cost = %s WHERE service_id = %s",
                (self.name, self.cost, self.id)
            )
            conn.commit()
            print(f" Service updated: ID={self.id}, Name={self.name}, Cost={self.cost}")
        except Exception as e:
            print(" Error updating service:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_service(service_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM services WHERE service_id = %s", (service_id,))
            conn.commit()
            print(f" Service with ID={service_id} has been deleted.")
        except Exception as e:
            print(" Error deleting service:", e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def view_all_service():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT service_id, service_name, cost FROM services")
            results = cursor.fetchall()
            if results:
                print("\nAvailable Services:\n")
                print(tabulate(
                    results,
                    headers={"service_id": "ID", "service_name": "Service Name", "cost": "Cost (₹)"},
                    tablefmt="grid"
                ))
            else:
                print("No services found.")
            return results
        except Exception as e:
            print("Error reading services:", e)
            return []
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def assign_service_to_patient():
        conn = get_db_connection()
        cursor = conn.cursor()
        services = Services.view_all_service()
        if not services:
            print("No services available to assign.")
            return

        patient_id = get_valid_patient_id()
        
        valid_ids = [service['service_id'] for service in services]
        while True:
            service_id = get_valid_service_id()
            if service_id in valid_ids:
                break
            print(f"Service ID {service_id} is not valid.")
            


        try:
            cursor.execute(
                "INSERT INTO patient_services (patient_id, service_id) VALUES (%s, %s)",
                (patient_id, service_id)
            )
            conn.commit()
            print(f"Assigned service ID {service_id} to patient ID {patient_id}")
        except Exception as e:
            print("Error assigning service to patient:", e)
        finally:
            cursor.close()
            conn.close()

