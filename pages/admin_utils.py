from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.llms import OpenAI
import pinecone
import numpy as np
from langchain.vectorstores import Pinecone
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from langchain.document_loaders.csv_loader import CSVLoader

#**********Functions to help you load documents to PINECONE***********

#Read PDF data
#def read_pdf_data(pdf_file):
    #pdf_page = PdfReader(pdf_file)
    #text = ""
    #for page in pdf_page.pages:
        #text += page.extract_text()
    #return text

def read_pdf_data(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


#Split data into chunks
def split_data(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    docs = text_splitter.split_text(text)
    docs_chunks =text_splitter.create_documents(docs)
    return docs_chunks

#Create embeddings instance
def create_embeddings_load_data():
    #embeddings = OpenAIEmbeddings()
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    return embeddings

#Function to push data to Pinecone
def push_to_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings,docs):

    pinecone.init(
    api_key=pinecone_apikey,
    environment=pinecone_environment
    )

    index_name = pinecone_index_name
    index = Pinecone.from_documents(docs, embeddings, index_name=index_name)

    return index

#*********Functions for dealing with Model related tasks...************

#Read dataset for model creation
def read_data(data):
    df = pd.read_csv(data,delimiter=',', header=None, encoding='utf-8')  
    return df

#Create embeddings instance
def get_embeddings():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

#Generating embeddings for our input dataset
def create_embeddings(df,embeddings):
    df[2] = df[0].apply(lambda x: embeddings.embed_query(x))
    return df

#Splitting the data into train & test
def split_train_test__data(df_sample):
    # Split into training and testing sets
    sentences_train, sentences_test, labels_train, labels_test = train_test_split(
    list(df_sample[2]), list(df_sample[1]), test_size=0.25, random_state=0,shuffle=True)
    print(len(sentences_train))
    return sentences_train, sentences_test, labels_train, labels_test


#Get the accuracy score on test data
def get_score(svm_classifier,sentences_test,labels_test):
    score = svm_classifier.score(sentences_test, labels_test)
    return score
