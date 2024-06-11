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

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 1. Load SQL Database
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
# print(db.dialect)
# print(db.get_usable_table_names())
# db.run("SELECT * FROM Artist LIMIT 10;")

# 2. Specify LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# chain = create_sql_query_chain(llm, db)
# response = chain.invoke({"question": "How many employees are there"})
# print(db.run(response))

# Look at the prompt
#print(chain.get_prompts()[0].pretty_print())

# 3. Execute Query Pipeline
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
# chain = write_query | execute_query
# chain.invoke({"question": "How many employees are there"})


# 4. Output Parser
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

print(chain.invoke({"question": "How many employees are there"}))
