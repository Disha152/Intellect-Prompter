# AI-POWERED QUERY GENERATOR


https://github.com/user-attachments/assets/7d7381f4-75b8-44c0-a92f-e8ca3b987198




This project demonstrates a web-based application to query a dataset through natural language using AI-powered solutions.

## Features

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
pip install streamlit google-generativeai python-dotenv pandas pandasai numpy faker pydantic requests pyyaml
```

# Set the API KEYS :
1) Get your apis key from [Pandasai]{https://www.pandabi.ai/admin/api-keys} and [GoogleAPI]{https://aistudio.google.com/app/apikey}.
2) Replace the 'your_pandasai_api_key' and 'your_google_api_key' with your actual apis key in your main.py file with your actual api key.
3) Save the changes.

#Install python dependencies in the activate Python environment 
```sh 
pip install -r requirements.txt
```

#Run the app
```SH
streamlit run main.py
```
