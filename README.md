# create-chatbot-aviation.regulationdocs-langchain
In this project I try to create chatbot with EASA air operations regulations rules and FAQs about this field. Firstly I preprocess pdf of regulations rules and create dataframe from FAQs that include question,answer, category variables.
Chatbot include different parts which are question-answer and classification of questions. I use Llama2-7b with the help of Langchain. I create vectorstore from pdf data, using Callbackmanager to add memory in chatbot deployement. I also use streamlit for deployement of chatbot
