import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker and set seeds
fake = Faker()
Faker.seed(123)
np.random.seed(123)

# Number of rows
n = 300


data = {
    "patient_id": [f"PAT-{100000 + i}" for i in range(n)],
    "name": [fake.name() for _ in range(n)],
    "age": [random.randint(1, 90) for _ in range(n)],
    "gender": [random.choice(["Male", "Female", "Other"]) for _ in range(n)],
    "admission_date": pd.date_range(start='2023-01-01', periods=n, freq='D').strftime('%Y-%m-%d').tolist(),
    "contact_no": [str(random.randint(6000000000, 9999999999)) for _ in range(n)]
}

# Create DataFrame
df_healthcare = pd.DataFrame(data)

# Save to CSV
df_healthcare.to_csv("patients_dataset.csv", index=False)
print("Dataset saved as 'healthcare_appointments_dataset.csv'")
