'''
1. Search the web and implement a RAG pipeline
    A. Get the list of web addresses
    B. Get the web content and store it in a vector store.
2. Generate questions related to the research topic
3. Get answers to these questions using the RAG pipeline
4. Format this into a file and provide it to the user.
'''
import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from llama_index.core import Settings,SimpleDirectoryReader,VectorStoreIndex,StorageContext
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.vector_stores.deeplake import DeepLakeVectorStore
from llama_index.postprocessor.cohere_rerank import CohereRerank
import os
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from  llama_index.llms.google_genai import GoogleGenAI
from google import genai
gemini = genai.Client(api_key='AIzaSyCFJ3RwiHvLTy9QYMhraasRH1D3h7zZ2G0')
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCFJ3RwiHvLTy9QYMhraasRH1D3h7zZ2G0'
os.environ['ACTIVELOOP_TOKEN'] = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTc1MjQxNTM1MywiZXhwIjoxNzgzOTUxMzQ0fQ.eyJpZCI6ImFrYW5pc2g0NDciLCJvcmdfaWQiOiJha2FuaXNoNDQ3In0.0LvHB3MAmmx_zZoVkqEa_taqfdgU6LtqRUBSuzyIcW4jS-igRJtNaBmb1R4ttwgsWGLY8iAoAp_ENharKghDyw'
llm = GoogleGenAI(model='gemini-2.5-flash-lite-preview-06-17')
embed_model = GoogleGenAIEmbedding(models='model/embedding-001')
Settings.llm = llm
Settings.embed_model = embed_model
cohere_rerank = CohereRerank(api_key='UyZatwiADpPOFnEuws2nE7z5F3oP95JapKp2q6ER',top_n=10)
mcp = FastMCP('deep-research-agent')
dataset_path = f"hub://akanish447/personal_agent/"
def google_search(query,num_results=5):
   url = 'https://www.googleapis.com/customsearch/v1' 
   params = {
      'q':query,
      'key':'AIzaSyA0UsRJUz6YZmhrXHMwnF8u18Er02sAROo',
      'cx':'d13b3db7c447d4d4f',
      "num":num_results
   }
   response = requests.get(url,params=params)
   response = response.json()
   return response.get("items",[])

def get_text(result):
    search_results = []
    for res in result:
        print(res['link'])
        response = requests.get(res['link'],timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text,'html.parser')
        search_results.append(soup.get_text(separator=' ',strip=True))
    return search_results

def save_to_vector_store():
    documents = SimpleDirectoryReader('data/').load_data()
    node_parser = SimpleNodeParser(chunk_size=512)
    nodes = node_parser.get_nodes_from_documents(documents,chunk_overlap=64)
    vector_store = DeepLakeVectorStore(dataset_path=dataset_path,overwrite=True)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    vector_index = VectorStoreIndex(nodes,storage_context=storage_context)
    query_engine = vector_index.as_query_engine(similarity_top_k=10,node_post_processors=[cohere_rerank])
    return query_engine

def gen_research_questions(topic:str):
    response = gemini.models.generate_content(
    model='gemini-2.5-flash-lite-preview-06-17',
    contents=f"""
        The  objective is enclosed by triple backticks, your work is to generate questions on that topic,
        ```{topic}```
        Also please don't specify any headers.
"""
    )
    questions = response.text.split('\n')
    questions = [q for q in questions if q!='']
    return questions

@mcp.tool()
def agent(topic:str):
    """This tool is used when the user want to deep research on a particular topic.
    ARGS: topic
    """
    result = google_search(topic)
    text_content = get_text(result)
    with open('data/content.txt','w',encoding='utf-8') as f:
        for c in text_content:
            f.write(c + '\n')
        
        f.close()
    query_engine = save_to_vector_store()
    questions = gen_research_questions(topic)
    response = ''
    for q in questions:
        response += q + '\n'
        response += str(query_engine.query(q)) + '\n'
    return response
#response = agent("What is Model Context Protocol?")

mcp.run(transport='stdio')

