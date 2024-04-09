from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# for retrievers:
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain.chains import create_retrieval_chain

load_dotenv()
LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# set up llm
llm = ChatOpenAI(api_key=OPENAI_API_KEY)

# set up prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

# set up output parser
output_parser = StrOutputParser()

# set up chain
chain = prompt | llm | output_parser

#print(chain.invoke({"input": "how can langsmith help with testing?"}))

# set up retriever
loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
docs = loader.load()
embeddings = OpenAIEmbeddings()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

# example of using document context
# print(document_chain.invoke({
#     "input": "how can langsmith help with testing?",
#     "context": [Document(page_content="langsmith can let you visualize test results")]
# }))

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)
response = retrieval_chain.invoke({"input": "how can langsmith help with testing?"})
print(response["answer"])