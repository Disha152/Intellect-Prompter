# AI-POWERED QUERY GENERATOR



https://github.com/user-attachments/assets/00be4fb4-ec15-4a97-9d46-b34ce28a1a11






This project demonstrates a web-based application to query a dataset through natural language using AI-powered solutions.

## Features

1) Error Handling -
   Included try-except block to catch and display errors from both PandasAI and 
   Google GenerativeAI and added  voice recognition error handling.
2) Real time Query Suggestions -
   Added an expander with the sample query suggestions assiting 
   users in formatting queries.
3) Advanced Visualization -
   Utilized plotly library for plotting the retrieved data which is the actual response.

## Implementation
  
Travel to the root of the directory !

For this purpose, it uses:

- [Streamlit] to build a data science web app.
- [PandasAI](https://www.pandabi.ai/admin/api-keys) to generate Pandas code from a query.
- [Google Generative AI (Gemini)](https://ai.google.dev/gemini-api/docs/api-key) to process natural language queries.

## Download Dataset

Download the dataset "data" folder to the root folder of directory , from [dataset](https://github.com/Fraud-Detection-Handbook/simulated-data-transformed.git).

## Run the Project

If you don't have a Python environment available, you can use the [conda package manager](https://docs.conda.io/projects/conda/en/latest/index.html) which comes with the [Anaconda distribution](https://www.anaconda.com/download) to manage a clean Python environment.

### Setup Conda Environment

Create a new environment and activate it:

```sh
conda create -n streamlit-pandasai python=3.9
conda activate streamlit-pandasai
```

##Install the Dependencies 

In your active conda environment install dependencies : 

```sh
pip install streamlit google-generativeai python-dotenv pandas pandasai numpy faker pydantic requests pyyaml SpeechRecognition plotly
```

##Set the API KEYS :
1) Get your apis key from [Pandasai](https://www.pandabi.ai/admin/api-keys) and [GoogleAPI](https://aistudio.google.com/app/apikey).
2) Replace the 'your_pandasai_api_key' and 'your_google_api_key' with your actual apis key in your main.py file with your actual api key.
3) Save the changes.

##Run the app
```SH
streamlit run main.py
```
Therefore , our query generator not only give the SQL query but also it's explanation , the output and the visual reperesentation of data.
