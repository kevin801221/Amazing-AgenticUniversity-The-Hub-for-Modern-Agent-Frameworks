from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

llm                 = ChatOpenAI(temperature=0)

system = """You are a helpful AI assistant which specializes in reading stock data provided in pandas.Dataframe format and answering relevant queries.
            Answer the question user asks. Be polite.
            Consider the provided context to frame your answer 
            At the end ask if the user would like to ask any more queries. 
"""
generation_prompt   = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Stock Data: {context}\n\nUser question: {question}")
    ]
)

generation_chain    = generation_prompt | llm | StrOutputParser()
