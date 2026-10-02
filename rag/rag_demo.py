import os
from constants import openai_key
from constants import openai_base_url
from typing import List, TypedDict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END

os.environ["OPENAI_API_KEY"]=openai_key
os.environ["OPENAI_BASE_URL"]=openai_base_url

news_urls = [
    "https://www.bbc.com/news",
    "https://www.cnn.com/world"
]

docs = [WebBaseLoader(url).load() for url in news_urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
chunk_size=300, chunk_overlap=20
)
#doc_splits is the chunked text that you would usually embed and store for semantic search.
# the docs_list size and doc_splits can be different and based on the lenght of the articles and chunk_size
doc_splits = text_splitter.split_documents(docs_list)

#Store and Retrive Current Affairs with ChromaDB
vectorstore = Chroma.from_documents(documents = doc_splits,
                                    collection_name="current-affairs-news",
                                    embedding=OpenAIEmbeddings()
                                    )

retriver = vectorstore.as_retriever()

# Prompt for Current Affairs News Summarization
prompt = ChatPromptTemplate.from_template(
    """
    you are a news analyst summarizing the latest current affairs. Use the retrieved articles to provide
    a consise summary. Highlight key global events and developments.

    Question: {question}
    New Articles: {context}
    Summary:
    """
)

## OPENNAI LLMS
getllm = ChatOpenAI(
    temperature=0.7,
    model="openai/gpt-5-mini"
)

current_affairs_chain = (
    prompt | getllm | StrOutputParser()
)

class CurrentAffairsGraphState(TypedDict):
    question : str
    retrived_news: List[str]
    generation: str

def retrieve_current_affairs(state):
    question = state["question"]
    retrived_news = retriver.invoke(question)
    return {"question":question, "retrived_news":retrived_news}

def generate_current_affairs_summary(state):
    question = state["question"]
    retrived_news =  state["retrived_news"]
    generation = current_affairs_chain.invoke({"question":question, "context":retrived_news})
    return {"question":question, "retrived_news":retrived_news,"generation":generation}

workflow = StateGraph(CurrentAffairsGraphState)
workflow.add_node("retrieve_current_affairs" , retrieve_current_affairs)
workflow.add_node("generate_current_affairs_summary" , generate_current_affairs_summary)

workflow.add_edge(START,"retrieve_current_affairs")
workflow.add_edge("retrieve_current_affairs","generate_current_affairs_summary")
workflow.add_edge("generate_current_affairs_summary",END)

graph = workflow.compile()


response = graph.invoke({"question":"What are the top global headlines today?"})

print(response["generation"])