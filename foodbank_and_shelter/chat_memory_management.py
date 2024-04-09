import dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


dotenv.load_dotenv()

LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

chat = ChatOpenAI(api_key=OPENAI_API_KEY)

# for example 1 & 2
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a helpful assistant. Answer all questions to the best of your ability.",
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )

# chain = prompt | chat

# example 1
# demo_ephemeral_chat_history = ChatMessageHistory()

# demo_ephemeral_chat_history.add_user_message(
#     "Translate this sentence from English to French: I love programming."
# )

# demo_ephemeral_chat_history.add_ai_message("J'adore la programmation.")

# print(demo_ephemeral_chat_history.messages)

# example 2
# demo_ephemeral_chat_history = ChatMessageHistory()

# input1 = "Translate this sentence from English to French: I love programming."

# demo_ephemeral_chat_history.add_user_message(input1)

# response = chain.invoke(
#     {
#         "messages": demo_ephemeral_chat_history.messages,
#     }
# )

# demo_ephemeral_chat_history.add_ai_message(response)

# input2 = "What did I just ask you?"

# demo_ephemeral_chat_history.add_user_message(input2)

# response2 = chain.invoke(
#     {
#         "messages": demo_ephemeral_chat_history.messages,
#     }
# )
# demo_ephemeral_chat_history.add_ai_message(response2)

# print(demo_ephemeral_chat_history.messages)

# example 3: Automatic History Management
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = prompt | chat

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history",
)

res1 = chain_with_message_history.invoke(
    {"input": "My name is Ariel. Translate this sentence from English to French: I love programming."},
    {"configurable": {"session_id": "unused"}},
)
res2 = chain_with_message_history.invoke(
    {"input": "What is my name? What did I just ask you?"}, {"configurable": {"session_id": "unused"}}
)
res2 = chain_with_message_history.invoke(
    {"input": "Hello this is Luke"}, {"configurable": {"session_id": "newuser"}}
)
res3 = chain_with_message_history.invoke(
    {"input": "What is my name"}, {"configurable": {"session_id": "newuser"}}
)
res4 = chain_with_message_history.invoke(
    {"input": "What is my name?"}, {"configurable": {"session_id": "unused"}}
) # returns Luke actually, because the unused is expired?
print(demo_ephemeral_chat_history_for_chain.messages)