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

load_dotenv()
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

db = SQLDatabase.from_uri("sqlite:///test_pantry.db")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

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

app = Flask(__name__)
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

    print("Messages: ", request_dict['message'])
    response = query_agent.invoke({"input": request_dict['message']})
    return response

@app.route("/update", methods=['GET', 'POST'])
def update():
    # can query and update Database
    return 'update'

@app.route("/updateInfo", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    request_dict = dict(request.values)
    print("Request dictionary: ", request_dict)
    userId = request_dict['From']
    message = request_dict['Body']
    print("From: "+str(userId)+" Message: "+str(message))

    resp = MessagingResponse()
    output = chat(userId, message)
    # need to send Andrew incoming_message and number
    # Add a message
    resp.message(output)

    return str(resp)

if __name__ == '__main__':
    # chat('1', 'My name is John')
    # chat('2', 'My name is Tim')
    # chat('1', 'what is my name?')
    # chat('2', 'what is my name?')
    # print(get_session_history('1').messages)
    # print(get_session_history('2').messages)
    app.run(host='0.0.0.0', port=8000, debug=True) # change host ='0.0.0.0' for EC2
