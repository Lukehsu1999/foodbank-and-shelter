"""
Purpose: Create SQLite database of social service providers from the csv file arnav gave us (/data/Foodpantries0611.csv)

Schema (Foodpantries0611.csv):
EFROID
Agency Name
Day of the Week
Opening Hour
Closing Hour
Frequency
Type of Organization
Address
Phone
Comments
24/7
Meal Type
Date Created
Inactive
Last Modified

New Schema:
Agency Name
Phone
Address
Service: food, shelter, ...
Monday: N/A or operating hours
Tuesday
Wednesday
Thursday
Friday
Saturday
Sunday
Last Modified

"""

import os
from dotenv import load_dotenv
import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, inspect
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

path_to_pantry_list = '../data/Foodpantries0611.csv'
path_to_new_csv = '../data/Foodpantries0611_new.csv'
path_to_new_db = ""

df = pd.read_csv(path_to_pantry_list)

# convert to new format
# Initialize the new_df with the desired columns
# Initialize the new_df with the desired columns
new_df = pd.DataFrame(columns=['Agency Name', 'Phone', 'Address', 'Service', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Last Modified'])

# Assuming df is already defined
for index, row in df.iterrows():
    agency_name = row['Agency Name']

    if agency_name in new_df['Agency Name'].values:
        new_df.loc[new_df['Agency Name'] == agency_name, row['Day of the Week']] = row['Opening Hour'] + ' - ' + row['Closing Hour']
    else:
        # Create a dictionary for the new row
        new_row = {
            'Agency Name': row['Agency Name'],
            'Phone': row['Phone'],
            'Address': row['Address'],
            'Service': row['Type of Organization'],
            'Monday': '',
            'Tuesday': '',
            'Wednesday': '',
            'Thursday': '',
            'Friday': '',
            'Saturday': '',
            'Sunday': '',
            'Last Modified': row['Last Modified']
        }
        # Set the specific day with the opening and closing hours
        new_row[row['Day of the Week']] = row['Opening Hour'] + ' - ' + row['Closing Hour']
        
        # Convert new_row to DataFrame and concatenate with new_df
        new_row_df = pd.DataFrame([new_row])
        new_df = pd.concat([new_df, new_row_df], ignore_index=True)

print(new_df.head(2))

# write new_df to a new csv file
new_df.to_csv(path_to_new_csv, index=False)


