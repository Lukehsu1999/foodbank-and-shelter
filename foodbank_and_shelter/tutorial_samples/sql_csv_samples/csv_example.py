import os
from dotenv import load_dotenv
import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 1. Load CSV 
df = pd.read_csv("titanic.csv")
# print(df.shape)
# print(df.columns.tolist())

# 2. Turn CSV into SQL
engine = create_engine("sqlite:///titanic.db")
df.to_sql("titanic", engine, index=False)

db = SQLDatabase(engine=engine)
print(db.dialect)
print(db.get_usable_table_names())
print(db.run("SELECT * FROM titanic WHERE Age < 2;"))

# 3. Specify LLM & SQL Agent
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
print(agent_executor.invoke({"input": "what's the average age of survivors"}))