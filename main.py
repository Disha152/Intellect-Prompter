import os
import streamlit as st
from dotenv import load_dotenv
from pandasai import SmartDataframe
from pandasai.responses import ResponseParser
from data import load_data
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import speech_recognition as sr  

# Load environment variables
load_dotenv()

# Set environment variable for PANDASAI_API_KEY
os.environ['PANDASAI_API_KEY'] = "your_pandasai_api_key"

# Set environment variable for GOOGLE_API_KEY
os.environ['GOOGLE_API_KEY'] = "your_google_api_key"

# Configure genai with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define custom callback class for Gemini
class StreamlitCallback:
    def __init__(self, container) -> None:
        self.container = container

    def on_code(self, response: str):
        self.container.code(response)

# Define custom response parser for PandasAI
class StreamlitResponse(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        st.dataframe(result["value"])
        return

    def format_plot(self, result):
        st.plotly_chart(px.bar(result["value"]))
        return

    def format_other(self, result):
        st.code(result["value"], language='sql')
        return

# Voice recognition for query input
def get_voice_query():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Say something!")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        st.write(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        st.error("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")

# Page title
st.markdown("# AI-Powered Data Query Interface ✨")

# Load the dataset
df = load_data("./data")

# Display a dataframe preview
with st.expander("🤖 Dataframe Preview"):
    st.write(df.tail(100))

# Create a SmartDataframe instance for PandasAI
sdf = SmartDataframe(df)

# Input for user query
query = st.text_area("🗣️ Chat with Dataframe !")

# Voice input button
voice_query_button = st.button("Use Voice Input 🎤")
if voice_query_button:
    query = get_voice_query()



# How to Use section
with st.expander("❓How to Use?"):
    st.write("""
  * Enter your data query in the text area above or you can use voice input by clicking the "Use Voice Input" button or you can directly copy paste from the sample queries below.
  * Click the "Generate " button.
  * The results of your query will be displayed below the input area.

  **Note:** This application currently uses Google Generative AI (Gemini) to process your queries and PandasAI to directly retrieve data from your database.
""")

# Real-time query suggestions
query_suggestions = ["Give me the top 10 customer id of customers whose tx_amount > 100", "Get me the top 10 customer id with the largest fraud amount (a fraud being tx_fraud=1)", "Plot the graph of amount of fraud for the top 10 customer_id"]
with st.expander("💡Sample Queries"):
    st.write("Try one of the following queries:")
    for suggestion in query_suggestions:
        st.write(f"- {suggestion}")

# Generate button
st.button('Generate 🎊')

container = st.container()

if query:
    try:
        # PandasAI interaction
        response = sdf.chat(query)
        
        if isinstance(response, dict):
            if response.get("type") == "dataframe":
                st.dataframe(response["value"])
            elif response.get("type") == "plot":
                st.plotly_chart(px.bar(response["value"]))
            else:
                st.write(response)
        else:
            st.write(response)
    except Exception as e:
        st.error(f"PandasAI Error: {e}")
    
    try:
        # Ensure the Google API key is set
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("GOOGLE_API_KEY environment variable not set.")
        else:
            model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
            response = model.generate_content(contents=query)
            sql_query = response.text.strip()
            container.code(sql_query, language='sql')
    except Exception as e:
        st.error(f"Gemini AI Error: {e}")