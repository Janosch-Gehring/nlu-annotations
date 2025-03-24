import streamlit as st
import pandas as pd
import time

headlines = pd.read_excel("memory_experiment/resources/Manipulated_headlines.xlsx")

placeholder = st.empty()

for index, row in headlines[:3].iterrows():
    placeholder.write(row["Original"])
    time.sleep(2)

st.switch_page("memory_experiment/pages/recall_page.py")