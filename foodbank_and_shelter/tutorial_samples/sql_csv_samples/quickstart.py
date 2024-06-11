# Reference: https://python.langchain.com/v0.1/docs/use_cases/sql/quickstart/
# Security Note: Building Q&A systems of SQL databases requires executing model-generated SQL queries. 

import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
print(db.dialect)
print(db.get_usable_table_names())
db.run("SELECT * FROM Artist LIMIT 10;")
