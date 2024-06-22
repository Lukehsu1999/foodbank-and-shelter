from flask import Flask, request
from dotenv import load_dotenv
import os
from flask_cors import CORS
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai.chat_models import ChatOpenAI
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.output_parsers import StrOutputParser
# from twilio.twiml.messaging_response import MessagingResponse
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.agent_toolkits import create_sql_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

load_dotenv()
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

db = SQLDatabase.from_uri("sqlite:///test_pantry.db")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
app = Flask(__name__)

# Query Agent will handle normal queries from any users
query_system_message = SystemMessage(
    content="""You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
If user asks to edit the database, return cannot edit the database""")

query_prompt = ChatPromptTemplate.from_messages(
    [
        query_system_message,
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

query_agent = create_sql_agent(
    llm=llm,
    db=db,
    prompt=query_prompt,
    verbose=True,
    agent_type="openai-tools",
)

# Update Agent will only assist verified providers in updating their information in database
update_system_message = SystemMessage(
    content="""You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
        """)

update_prompt = ChatPromptTemplate.from_messages(
    [
        update_system_message,
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
    ]
)

update_agent = create_sql_agent(
    llm=llm,
    db=db,
    prompt=update_prompt,
    verbose=True,
    agent_type="openai-tools",
)



# #CORS(app)

# # global variables
# # store will store every key-value pair of user_id - chathistory
# model = ChatOpenAI()
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "Build an SMS chatbot for homeless people to find the nearest food center or taxes help or financial help or medical assistance. Use a session ID to remember users. Keep responses under 280 characters, clear, and helpful. Be kind, harmless, and filter any inappropriate content. Aim to assist quickly. When giving details on location, give phone number as well.",
#         ),
#         MessagesPlaceholder(variable_name="history"),
#         ("human", "{input}"),
#     ]
# )
# output_parser = StrOutputParser()
# runnable = prompt | model | output_parser

# store = {}

# support functions
def verify_update_users(phone_number, db):
    print("Checking phone number: ", phone_number)
    # Define the SQL query to check if the phone number exists and get permissions
    query = f"SELECT * FROM Foodpantry WHERE PhoneNumber = '{phone_number}'"
    
    # Execute the query (assuming you have a function to execute queries and return results)
    results = db.run(query)
    print(results)
    # Check if the phone number exists and has the necessary permissions
    if results:

        return True, format_query_results(results)
    else:
        return False, "You do not have permission to edit the database."

def format_query_results(results):
    item = results[0] # assuming no shared phone number among food pantries
    print("item: ",item)
    return results
    return "Name: " + item[0] + ", Phone number: " + item[1] + ", Address: " + item[2] + ", Hours: " + item[3]  

# routes
@app.route('/')
def home():
    print('home')
    return 'Hello, Flask!'

@app.route('/query', methods=['POST'])
def query():
    # can only query Database, cannot update database
    request_dict = request.get_json()
    print("Request dictionary: ", request_dict)
    phonenumber = request_dict['From']
    message = request_dict['Body']
    response = query_agent.invoke({"input": message})
    return response

@app.route("/update", methods=['GET', 'POST'])
def update():
    # can query and update Database
    # Step 1: Get Inforation
    request_dict = request.get_json()
    phonenumber = request_dict['From']
    message = request_dict['Body']
    print("Request dictionary: ", request_dict)
    print("Messages: ", message)
    print("Phone number: ", phonenumber)

    # Step 2: Check if phone number is valid for making an update
    verified, res = verify_update_users(phonenumber, db)
    
    # Step 3: If phone number is valid, process their requests
    if not verified:
        return res
    else:
        print("Corresponding Entry to the number: ", res)
        # phone number restriction
        limitation_query = f"WHERE PhoneNumber = '{phonenumber}'"
        print("Limitation query: ", limitation_query)
        response = update_agent.invoke({"input": message + limitation_query, "phone_number": phonenumber})
        #updated_results = 
        return response

if __name__ == '__main__':
    # chat('1', 'My name is John')
    # chat('2', 'My name is Tim')
    # chat('1', 'what is my name?')
    # chat('2', 'what is my name?')
    # print(get_session_history('1').messages)
    # print(get_session_history('2').messages)
    app.run(host='0.0.0.0', port=8000, debug=True) # change host ='0.0.0.0' for EC2
