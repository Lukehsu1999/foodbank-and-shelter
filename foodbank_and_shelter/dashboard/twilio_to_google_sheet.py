"""
Convert a Twilio Messaging Log to our Google Sheet backed format (.csv)
"""
import pandas as pd
import hashlib

# specify the file paths
path_import_twilio_csv = '../data/AskBobby_0715.csv'
path_export_google_csv = '../data/AskBobby_0715_google.csv'

# specify the column mapping
column_mapping = {
    'From':'From_Encrypted',
    'To':'To_Encrypted',
    'Body':'Message',
    'SentDate':'Date',
}

# to protect PII and ensure anonymity, we hash the phone number
# Predefined salt
seed = "42"
reserved_number = "18669141274"
reserved_hashed = 'AskBobby'

# Function to hash phone numbers with SHA-256 and predefined salt
def hash_phone_number_sha256(phone_number):
    # for our own number we don't need to hash it
    if str(phone_number) == reserved_number:
        return reserved_hashed
    else:
        phone_number_str = str(phone_number)
        phone_number_bytes = phone_number_str.encode('utf-8')
        salt_bytes = seed.encode('utf-8')
        hash_object = hashlib.sha256(salt_bytes + phone_number_bytes)
        hashed_phone_number = hash_object.hexdigest()
        return hashed_phone_number

# open twilio csv
twilio_df = pd.read_csv(path_import_twilio_csv)

# Perform hashing on 'From' and 'To' columns
twilio_df['From'] = twilio_df['From'].apply(hash_phone_number_sha256)
twilio_df['To'] = twilio_df['To'].apply(hash_phone_number_sha256)

# convert to google sheet format
google_df = google_df = twilio_df[list(column_mapping.keys())].rename(columns=column_mapping)
google_df.to_csv(path_export_google_csv, index=False)

print(google_df.head)


