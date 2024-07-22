
import os
import streamlit as st
from dotenv import load_dotenv
from pandasai import SmartDataframe
from pandasai.responses import ResponseParser
from data import load_data
import google.generativeai as genai
import pandas as pd

# Load environment variables
load_dotenv()


# Set API Keys
os.environ['PANDASAI_API_KEY'] ="$2a$10$UrAOkPe3dcj4KxxuccajZe1/Tw8YZl1TwHERKf3JrhwOXebnnxebS"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define custom callback class for Gemini
class StreamlitCallback:
    def __init__(self, container) -> None:  # Corrected __init__ method
        self.container = container

    def on_code(self, response: str):
        self.container.code(response)

# Define custom response parser for PandasAI
class StreamlitResponse(ResponseParser):
    def __init__(self, context) -> None:  # Corrected __init__ method
        super().__init__(context)

    def format_dataframe(self, result):
        st.dataframe(result["value"])
        return

    def format_plot(self, result):
        st.image(result["value"])
        return

    def format_other(self, result):
        st.code(result["value"], language='sql')
        return

# st.write("#AI Query Generator ✨")
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
container = st.container()

# How to Use section
with st.expander(" How to Use?"):
    st.write("""
  * Enter your data query in the text area above.
  * Click the "Generate " button.
  * The results of your query will be displayed below the input area.

  **Note:** This application currently uses Google Generative AI (Gemini) to process your queries and PandasAI to directly retrieve data from your database.
""")


st.button('Generate 🎊')

if query:
    try:
        # PandasAI interaction
        response = sdf.chat(query)
        
        if isinstance(response, dict):
            if response.get("type") == "dataframe":
                st.dataframe(response["value"])
            elif response.get("type") == "plot":
                st.image(response["value"])
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

