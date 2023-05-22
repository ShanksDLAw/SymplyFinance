from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
import os
import streamlit as st
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.llms import OpenAI as LangchainOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper
# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

# Displaying the initial UI/UX
st.title("Symply Finance")
st.write("We are your AI-powered Financial Wizard")
st.subheader("Here's some additional information:")
st.write("This app provides general information about investing in financial markets.")
st.write("It's important to do your own research and consider professional advice before making any investment decisions.")

# Collecting prompt from our users
prompt = st.text_input('What would you like to know or explained')

# Initialize the Langchain LLM and the Temperature (How creative the AI will be)
llm = LangchainOpenAI(temperature=0.1)

# Initializing the Google Serper API Wrapper tool
search = GoogleSerperAPIWrapper(api_key=os.getenv('SERPER_API_KEY'))

# Defining use of the Google SerperAPI Wrapper tool
tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="Useful for when you need to ask with search."
    )
]

# Initialize the tools and agent
tools = load_tools(["google-serper"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

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
#...
if st.button("Submit"):
    if prompt:
        user_input = prompt
        conversation = [
            *investment_system_messages,
            HumanMessage(content=user_input)
        ]
        result = agent(conversation)
        response_text = result['output']
        st.write(response_text)
        
        # Add the feedback link
        feedback_link = "https://docs.google.com/forms/d/e/1FAIpQLSfRg1b0ZzOAu2tFVDV8b_B_mXiZ3Kt4gCiNsnqXzvJmMuJoRA/viewform?usp=sf_link"
        st.markdown(f"## Have feedback? We'd love to hear from you! [Submit Feedback]({feedback_link})")
        
    else:
        st.write("Please enter a question.")



