# import pickle
# from pathlib import Path

# import pandas as pd
# import streamlit as st


# def load_file(path: str) -> pd.DataFrame:
#     with open(path, "rb") as f:
#         dataset = pickle.load(f)
#         return dataset


# @st.cache_data
# def load_data(folder: str) -> pd.DataFrame:
#     all_datasets = [load_file(file) for file in Path(folder).iterdir()]
#     df = pd.concat(all_datasets)
#     return df
import pickle
from pathlib import Path
import pandas as pd
import streamlit as st

def load_file(path: str) -> pd.DataFrame:
    with open(path, "rb") as f:
        dataset = pickle.load(f)
        if not isinstance(dataset, pd.DataFrame):
            raise ValueError(f"The file {path} does not contain a valid DataFrame.")
        return dataset

@st.cache_data
def load_data(folder: str) -> pd.DataFrame:
    all_datasets = [load_file(file) for file in Path(folder).iterdir()]
    df = pd.concat(all_datasets, ignore_index=True)
    return df
