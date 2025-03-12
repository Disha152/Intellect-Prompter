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

# Set environment variables
os.environ['PANDASAI_API_KEY'] = "$2a$10$ipYpseAvcKuwebxJMt9bauh9vPzzNhTZqBCyXUtOsW9ogPjI4HmRO"
os.environ['GOOGLE_API_KEY'] = "AIzaSyCI7fmbK5Wmj6Sf3mVlUG49OQLJqKP7MHY"

# Configure Gemini AI with Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page title
st.markdown("# AI-Powered Data Query Interface ✨")

# Load dataset
df = load_data("data")

# Dataframe preview
with st.expander("🤖 Dataframe Preview"):
    st.write(df.tail(100))

# SmartDataframe instance for PandasAI
sdf = SmartDataframe(df)

# User query input
query = st.text_area("🗣️ Chat with Dataframe!")

# Voice input button
if st.button("Use Voice Input 🎤"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Say something!")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        st.write(f"You said: {query}")
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError as e:
        st.error(f"Error: {e}")

# Sample queries
query_suggestions = [
    "Give me the top 10 customer id of customers whose tx_amount > 100",
    "Get me the top 10 customer id with the largest fraud amount (tx_fraud=1)",
    "Plot the graph of amount of fraud for the top 10 customer_id"
]
with st.expander("💡 Sample Queries"):
    for suggestion in query_suggestions:
        st.write(f"- {suggestion}")

# Generate button
if st.button('Generate 🎊') and query:
    try:
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
