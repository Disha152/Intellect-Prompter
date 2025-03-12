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
os.environ['PANDASAI_API_KEY'] = "$2a$10$ipYpseAvcKuwebxJMt9bauh9vPzzNhTZqBCyXUtOsW9ogPjI4HmRO"

# Set environment variable for GOOGLE_API_KEY
os.environ['GOOGLE_API_KEY'] = "AIzaSyCI7fmbK5Wmj6Sf3mVlUG49OQLJqKP7MHY"

# Configure genai with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
df = load_data("data")

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
  * Enter your data query in the text area above or use voice input.
  * Click the "Generate " button.
  * The results of your query will be displayed below.

  **Note:** This application currently uses Google Generative AI (Gemini) to process your queries and PandasAI to retrieve data from your database.
""")

# Real-time query suggestions
query_suggestions = [
    "Give me the top 10 customer id of customers whose tx_amount > 100",
    "Get me the top 10 customer id with the largest fraud amount (a fraud being tx_fraud=1)",
    "Plot the graph of amount of fraud for the top 10 customer_id"
]

with st.expander("💡Sample Queries"):
    st.write("Try one of the following queries:")
    for suggestion in query_suggestions:
        st.write(f"- {suggestion}")

# Generate button
generate_button = st.button('Generate 🎊')

container = st.container()

if generate_button and query:
    try:
        # Ensure the Google API key is set
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("GOOGLE_API_KEY environment variable not set.")
        else:
            model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
            response = model.generate_content(contents=query)
            sql_query = response.text.strip()
            
            # Extract the first SQL query if multiple are generated
            sql_query = sql_query.split("```sql")[1].split("```")[0].strip()

            # Display SQL Query
            container.code(sql_query, language='sql')

            # Explanation
            with st.expander("📌 SQL Query Explanation"):
                st.write("""
                **Step 1:** Select `customer_id` and compute `SUM(fraud_amount)` for each customer.
                **Step 2:** Filter the transactions where `tx_fraud = 1` (fraudulent transactions).
                **Step 3:** Group by `customer_id` to calculate the total fraud per customer.
                **Step 4:** Order results in descending order to get the highest fraud amounts first.
                **Step 5:** Limit the result to the top 10 customers.
                """)

    except Exception as e:
        st.error(f"Gemini AI Error: {e}")
