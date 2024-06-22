# Reference: https://python.langchain.com/v0.1/docs/use_cases/sql/csv/
# Query Limitations: 
# 1. Can do Time and Date filtering
# 2. Can do Zip Code filtering, however, not actual address

import os
from dotenv import load_dotenv
import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, inspect
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 1. Load CSV 
df = pd.read_csv("foodpantries0611.csv")
# print(df.shape)
# print(df.columns.tolist())

# 2. Turn CSV into SQL
engine = create_engine("sqlite:///foodpantries0611.db")

# Check if table exists and drop it if it does
if not inspect(engine).has_table("foodpantries0611"):
    df.to_sql("foodpantries0611", engine, index=False)

db = SQLDatabase(engine=engine)

# 3. Specify LLM & SQL Agent
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
print(agent_executor.invoke({"input": "Find me 5 food pantries that open on weekends"}))