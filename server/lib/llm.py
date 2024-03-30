import os

from dotenv import load_dotenv
from langchain.prompts import (FewShotPromptTemplate, MessagesPlaceholder,
                               PromptTemplate,
                               SemanticSimilarityExampleSelector,
                               SystemMessagePromptTemplate)
from langchain.prompts.chat import ChatPromptTemplate
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from sqlalchemy import create_engine

from .prompts import examples, prefix

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_LLM_URL") or ""

engine = create_engine(SQLALCHEMY_DATABASE_URL)

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)

example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
)

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "top_k", "dialect"],
    prefix=prefix,
    suffix="",
)

full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

db = SQLDatabase(engine)
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_toolkit.get_tools()

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=sql_toolkit,
    agent_type="openai-tools",
    verbose=True,
    prompt=full_prompt,
)

# agent_executor.invoke(
#     {
#         "input": "Which outlet closed the latest?",
#         "dialect": "PostgreSQL",
#         "top_k": 10,
#     }
# )
