from dotenv import load_dotenv
import streamlit as st
from user_utils import *
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.llms import HuggingFaceHub
import sentence_transformers
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from streamlit_chat import message
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
from langchain.memory import ConversationBufferMemory

os.environ["HUGGINGFACEHUB_API_TOKEN"]='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'

#Creating session variables
if 'Part-ARO' not in st.session_state:
    st.session_state['Part-ARO'] =[]
if 'Part-ORO' not in st.session_state:
    st.session_state['Part-ORO'] =[]
if 'Part-CAT' not in st.session_state:
    st.session_state['Part-CAT'] =[]
if 'Part-NCC' not in st.session_state:
    st.session_state['Part-NCC'] =[]
if 'Part-NCO' not in st.session_state:
    st.session_state['Part-NCO'] =[]
if 'Part-SPA' not in st.session_state:
    st.session_state['Part-SPA'] =[]
if 'Part-SPO' not in st.session_state:
    st.session_state['Part-SPO'] =[]
if 'Definitions' not in st.session_state:
    st.session_state['Definitions'] =[]


def main():
    load_dotenv()
    st.set_page_config(page_title='Chatbot with Memory', page_icon=":book:")
    st.header("Automatic Question Classification Tool")
    st.markdown("<h1 style='text-align: center;' How can I help you? <\h1>", unsafe_allow_html=True)


    #creating embeddings instance
    embeddings=create_embeddings()

    #Function to pull index data from Pinecone
    index=pull_from_pinecone("840ccd16-2054-40ef-a767-da8b986a32cf","gcp-starter","pdf",embeddings)
        
    #This function will help us in fetching the top relevent documents from our vector store - Pinecone Index
    #relavant_docs=get_similar_docs(index,user_input)


    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    #llm = CTransformers(model = "llama-2-7b-chat.ggmlv3.q8_0.bin", model_type="llama", max_new_tokens = 512, temperature = 0.5,callback_manager=callback_manager)
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512},callback_manager=callback_manager)


    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=llm,chain_type='stuff',
                                              retriever=index.as_retriever(search_kwargs={"k":4}),
                                              memory=memory)
    def conversation_chat(query):
        result = chain({"question": query, "chat_history": st.session_state['history']})
        st.session_state['history'].append((query, result["answer"]))
        return result["answer"]

    def initialize_session_state():
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello! Ask me about flight operations regulations 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey! 👋"]

    def display_chat_history():
        reply_container = st.container()
        container = st.container()

        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Question:", placeholder="Ask about EASA Flight Operations", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = conversation_chat(user_input)

                button = st.button("Submit ticket?")
                if button:
        
                    embeddings = create_embeddings()
                    query_result = embeddings.embed_query(user_input)

                    #loading the ML model, so that we can use it to predit the class to which this compliant belongs to...
                    department_value = predict(query_result)
                    st.write("your ticket has been sumbitted to : "+department_value)

                    #Appending the tickets to below list, so that we can view/use them later on...
                    if department_value=="Definitions":
                        st.session_state['Definitions'].append(user_input)
                    elif department_value=="Part-ARO":
                        st.session_state['Part-ARO'].append(user_input)
                    elif department_value=="Part-ORO":
                        st.session_state['Part-ORO'].append(user_input)
                    elif department_value=="Part-CAT":
                        st.session_state['Part-CAT'].append(user_input)
                    elif department_value=="Part-NCC":
                        st.session_state['Part-NCC'].append(user_input)
                    elif department_value=="Part-NCO":
                        st.session_state['Part-NCO'].append(user_input)    
                    elif department_value=="Part-SPO":
                        st.session_state['Part-SPO'].append(user_input)
                    else:
                        st.session_state['Part-SPA'].append(user_input)


                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        if st.session_state['generated']:
            with reply_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

    # Initialize session state
    initialize_session_state()
    # Display chat history
    display_chat_history()
    

if __name__ == '__main__':
    main()




