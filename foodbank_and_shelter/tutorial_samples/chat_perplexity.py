# Try using Chat perplexity: Reference: https://python.langchain.com/v0.2/docs/integrations/chat/perplexity/
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
PPLX_API_KEY = os.getenv('PPLX_API_KEY')
chat = ChatPerplexity(temperature=0, model="llama-3-sonar-small-32k-online")

system = "You are a helpful assistant."
human = "{input}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat
response = chain.invoke({"input": "請告訴我台灣大學的介紹"})
print(response)
