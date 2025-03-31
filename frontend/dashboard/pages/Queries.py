import pandas as pd
import os
import streamlit as st

current_file = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file, "../../../../"))
data_folder = os.path.join(project_root, "data")

st.header("Queries Already Made")

queries = pd.read_csv(os.path.join(data_folder, "queries.csv"))

st.write(queries)