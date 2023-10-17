import os
from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.callbacks import get_openai_callback

import streamlit as st

load_dotenv('key.env')

llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

model = ChatOpenAI()

st.title("Code Generator")
tokens_used = 0  
# Constants
TOKEN_COST = 0.0001  # Replace with your actual cost per token

# Group the related input options under expandable sections
with st.sidebar.expander("1. Input & Output"):
    input_list = st.text_input("Input Word", "Sun rises in the east")
    output_list = st.text_input("Expected Output", "'Sun','rises','in','the','east'")

with st.sidebar.expander("2. Language Selection"):
    lang = st.selectbox("Programming Language", ["c", "c++", "java", "python", "html", "sql"])

with st.sidebar.expander("3. Description"):
    text = st.text_input("Describe the Task", "convert sentence to words")

prompt_text = "use {lang} to {text} with input: {inp} and output: {outp}. Please give me only code"

if st.button("Generate Code"):
    template = ChatPromptTemplate.from_messages([("system", prompt_text)])
    template = template.format_messages(text=text, lang=lang, inp=input_list, outp=output_list)
    
    response = model(template)
    code = response.content
    


    
    with get_openai_callback() as aa:
        result = model(template)
        print(st.write(aa))
    st.subheader("Generated Code:")
    st.code(code)

    


    with open("logs.txt", "a") as logfile:
        logfile.write(f"Language: {lang}\n")
        logfile.write(f"Input: {input_list}\n")
        logfile.write(f"Output: {output_list}\n")
        logfile.write(f"Text: {text}\n")
        logfile.write(f"Generated Code:\n")
        logfile.write(f"{code}\n")
        logfile.write(f"Tokens: {tokens_used}\n")
