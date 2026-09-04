from faker import Faker
import pandas as pd
import secrets
import string
import os
from google.cloud import storage

fake = Faker()


# -----------------------------
# 1. Generate random password
# -----------------------------
def generate_random_password(length=14):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))


# -----------------------------
# 2. Generate employee data
# -----------------------------
employees = []

for i in range(100):

    employees.append({
        "employee_id": f"EMP{i+1:04d}",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address().replace("\n", ", "),
        "date_of_birth": fake.date_of_birth(
            minimum_age=21,
            maximum_age=60
        ),
        "department": fake.random_element([
            "IT",
            "Finance",
            "HR",
            "Operations",
            "Payments",
            "Risk",
            "Data"
        ]),
        "job_title": fake.job(),
        "salary": fake.random_int(
            min=30000,
            max=150000
        ),
        "password": generate_random_password()
    })


# -----------------------------
# 3. Convert to DataFrame
# -----------------------------
df = pd.DataFrame(employees)


# -----------------------------
# 4. Save as CSV
# -----------------------------
csv_file = "employee_data.csv"

df.to_csv(
    csv_file,
    index=False
)

print(f"CSV created: {csv_file}")


# -----------------------------
# 5. Upload CSV to GCS
# -----------------------------

bucket_name = os.getenv("bkt-employee-data-ji")
destination_blob_name = "employee_data/employee_data.csv"

if bucket_name:
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(csv_file)

    print("CSV successfully uploaded to GCS bucket.")
else:
    print("GCS_BUCKET_NAME is not set; skipping GCS upload.")