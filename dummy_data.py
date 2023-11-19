import random
from datetime import datetime
from faker import Faker
import pandas as pd

queues = list(range(19, 1019))


def generate_dummy_data(num_records):
    fake = Faker()

    data = {
        "medical_id": [fake.ssn() for _ in range(num_records)],
        "first_name": [fake.first_name() for _ in range(num_records)],
        "last_name": [fake.last_name() for _ in range(num_records)],
        "address": [fake.address() for _ in range(num_records)],
        "created_at": [datetime.now() for _ in range(num_records)],
        "city": [fake.city() for _ in range(num_records)],
        "state": [fake.country() for _ in range(num_records)],
        "zip_code": [fake.postcode() for _ in range(num_records)],
        "phone": [fake.msisdn() for _ in range(num_records)],
        "birth_date": [fake.simple_profile()["birthdate"] for _ in range(num_records)],
        "comment": [fake.paragraph(nb_sentences=2) for _ in range(num_records)],
        "user_queue_id": [random.choice(queues) for _ in range(num_records)],
    }

    return pd.DataFrame(data)


# Specify the number of records you want
num_records = 10000

# Generate dummy data
dummy_data = generate_dummy_data(num_records)

print(dummy_data)

dummy_data.to_csv("submissions.csv", index=False)


# medical_id,first_name,last_name,address,created_at,city,state,zip_code,phone,birth_date,comment,user_queue_id
