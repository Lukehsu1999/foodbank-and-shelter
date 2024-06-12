# Reference: https://python.langchain.com/v0.1/docs/use_cases/sql/quickstart/
# Security Note: Building Q&A systems of SQL databases requires executing model-generated SQL queries. 

import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

db = SQLDatabase.from_uri("sqlite:///test_pantry.db")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
# Test Query
print(agent_executor.invoke({"input": "Give me Luke Food Pantry's Opening Hours"}))

# Test Update Database
#print(agent_executor.invoke({"input": "Change Luke Food Pantry's opening hours to weekends, same time"}))