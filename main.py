import os
import streamlit as st
from dotenv import load_dotenv
from pandasai import SmartDataframe
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

# Configure Gemini AI with Google API key
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

# Load dataset
df = load_data("data")

# Dataframe preview
with st.expander("🤖 Dataframe Preview"):
    st.write(df.tail(100))

# SmartDataframe instance for PandasAI
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

            # Display SQL Query
            st.markdown("### 📌 Generated SQL Query:")
            st.code(sql_query, language='sql')

            # Step-by-step explanation
            st.markdown("### 🔍 Step-by-Step Explanation:")
            explanation = """
            1. **SELECT customer_id, SUM(fraud_amount) AS total_fraud_amount**  
               → Selects the `customer_id` and calculates total fraudulent transactions per customer.
            
            2. **FROM transactions**  
               → Fetches data from the `transactions` table.

            3. **WHERE tx_fraud = 1**  
               → Filters only fraudulent transactions (`tx_fraud = 1`).

            4. **GROUP BY customer_id**  
               → Groups data by `customer_id` to calculate fraud sum per user.

            5. **ORDER BY total_fraud_amount DESC**  
               → Sorts the results in descending order based on the fraud amount.

            6. **LIMIT 10**  
               → Returns only the **top 10** customers with the highest fraud amount.
            """
            st.markdown(explanation)
    except Exception as e:
        st.error(f"Gemini AI Error: {e}")
