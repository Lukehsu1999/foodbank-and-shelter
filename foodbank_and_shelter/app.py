from flask import Flask, request
from dotenv import load_dotenv
import os
from flask_cors import CORS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

app = Flask(__name__)
#CORS(app)

# global variables
# store will store every key-value pair of user_id - chathistory
model = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're an assistant who's good. Respond in 20 words or fewer",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
output_parser = StrOutputParser()
runnable = prompt | model | output_parser

store = {}

# support functions
def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

def chat(session_id, input_message):
    print("chatting with", session_id, ":", input_message)
    history = get_session_history(session_id)
    output = with_message_history.invoke(
        {"input": input_message},
        config={"configurable": {"session_id": session_id}},
    )
    print("output:", output)
    return output

# routes
@app.route('/')
def home():
    print('home')
    return 'Hello, Flask!'

@app.route('/chat', methods=['POST'])
def chat_route():
    print('chat_route')
    session_id = request.json['session_id']
    input_message = request.json['input_message']
    print('session_id:', session_id, 'input_message:', input_message)
    output = chat(session_id, input_message)
    return output

@app.route('/history', methods=['POST'])
def history():
    session_id = request.json['session_id']
    history = get_session_history(session_id)
    print('history:', history.messages)
    return str(history.messages)

if __name__ == '__main__':
    # chat('1', 'My name is John')
    # chat('2', 'My name is Tim')
    # chat('1', 'what is my name?')
    # chat('2', 'what is my name?')
    # print(get_session_history('1').messages)
    # print(get_session_history('2').messages)
    app.run(debug=True)
