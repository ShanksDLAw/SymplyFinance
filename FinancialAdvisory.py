#The essence of this python script is to build a V2 FInancial Mentory Service
#This script takes a user input in a prompt 
#From this script it takes the user input and queries the internet via Google Serper API
#After the search it displays the result

#Importing the Packages
import os
import streamlit as st
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI as LangchainOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI


# Load environment variables
#Input your OpenAI API key in an .env
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']


#Displaying the intial UI/UX
st.title("Symply Finance")
st.write("We are your AI-powered Financial Wizard")
st.subheader("Here's some additional information:")
# Add some more content
st.write("This app provides general information about investing in financial markets.")
st.write("It's important to do your own research and consider professional advice before making any investment decisions.")


#Collecting prompt from our users
prompt = st.text_input('What would you like to know or explained')

# Initialize the Langchain LLM and the Temperature (How creative the AI will be)
llm = LangchainOpenAI(temperature=0.1)


# Initializing the Google Serper API Wrapper tool
# You can get your serper api by opening an account at serper.dev
search = GoogleSerperAPIWrapper(api_key=os.getenv('SERPER_API_KEY'))

# Defining use of the Google SerperAPI Wrapper tool
tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="Useful for when you need to ask with search."
    )
]

#Setting up the chat model using ChatOpenAI mode

# Set up ChatOpenAI model
chat = ChatOpenAI(temperature=0)

# Defining investment-related system messages
investment_system_messages = [
    SystemMessage(content="You are a friendly Stock/Financial analyst that  provides a detailed investment advice."),
    SystemMessage(content="Investing involves risks. It's important to do thorough research and consider professional advice."),
    SystemMessage(content="I can provide general and detailed information about investment strategies and concepts."),
    SystemMessage(content="You Provide highly profitable Financial/Investment Strategies")

]

# Processing user input and display results
if st.button("Submit"):
    if prompt:
        user_input = prompt  # Directly use the user's input
        conversation = [
            *investment_system_messages,
            HumanMessage(content=user_input)
        ]
        result = chat(conversation)
        response_text = result.content
        st.write(response_text)
    else:
        st.write("Please enter a question.")







