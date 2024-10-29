import duckdb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.duckdb import DuckDBVectorStore
from llama_index.core import StorageContext
# https://docs.llamaindex.ai/en/stable/examples/data_connectors/WebPageDemo/
# https://www.datacamp.com/tutorial/building-ai-projects-with-duckdb 
# https://scholarcommons.sc.edu/cgi/viewcontent.cgi?article=7019&context=etd
from IPython.display import Markdown, display
import os
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings


llm = OpenAI(model="gpt-4o",api_key=os.environ["OPENAI_API_KEY"])

embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
)




Settings.llm = llm
Settings.embed_model = embed_model

documents = SimpleDirectoryReader("PDFs").load_data()



vector_store = DuckDBVectorStore(database_name = "dc.duckdb",table_name = "mahler",persist_dir="./", embed_dim=1536)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# check it
con = duckdb.connect("dc.duckdb")
con.execute("SHOW ALL TABLES").fetchdf()
con.execute("SELECT * FROM mahler LIMIT 10").fetchdf()



# create a simple RAG

query_engine = index.as_query_engine()
response = query_engine.query("Who is Mahler? Report back in a funny poem")
display(Markdown(f"<b>{response}</b>"))

response = query_engine.query("What did I just ask?")
display(Markdown(f"<b>{response}</b>")) # funny, that is not what i asked?

# create a RAG with memory

from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine

memory = ChatMemoryBuffer.from_defaults(token_limit=3900)


chat_engine = CondensePlusContextChatEngine.from_defaults(
    index.as_retriever(),
    memory=memory,
    llm=llm
)


response = chat_engine.chat(
    "Did Mahler write for the trombone?"
)

display(Markdown(response.response))


response = chat_engine.chat(
    "What did I just ask?"
)
display(Markdown(response.response)) # works!
