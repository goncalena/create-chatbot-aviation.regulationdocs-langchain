import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import joblib
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.llms import HuggingFaceHub
import sentence_transformers
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"]='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'

#Function to pull index data from Pinecone
def pull_from_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings):

    pinecone.init(
    api_key=pinecone_apikey,
    environment=pinecone_environment
    )

    index_name = pinecone_index_name

    index = Pinecone.from_existing_index(index_name, embeddings)
    return index

def create_embeddings():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    query_result = embeddings.embed_query("large language model")
    print(len(query_result))
    return embeddings

#This function will help us in fetching the top relevent documents from our vector store - Pinecone Index
def get_similar_docs(index,query,k=2):

    similar_docs = index.similarity_search(query, k=k)
    return similar_docs

#def get_answer(docs,user_input):
    #callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    #llm = CTransformers(model = "llama-2-7b-chat.ggmlv3.q8_0.bin", model_type="llama", max_new_tokens = 512, temperature = 0.5,callback_manager=callback_manager)
    #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512},callback_manager=callback_manager)


    #memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    #chain = ConversationalRetrievalChain.from_llm(llm=llm,chain_type='stuff',retriever=vector_store.as_retriever(search_kwargs={"k":4}),memory=memory)

    #return chain


def predict(query_result):
    Fitmodel = joblib.load('modelsvm.pk1')
    result=Fitmodel.predict([query_result])
    return result[0]