import streamlit as st

import pandas as pd
import random 

st.write("Next, we will show you some more headlines. For each headline, decide whether you have seen it before or not.")

headlines = pd.read_excel("memory_experiment/resources/Manipulated_headlines.xlsx")
i = random.randint(0, len(headlines))
st.write(headlines["Original"][i])
st.radio("Have you seen the text above before?", ["Yes, this was shown to me in the initial task", "No, this headline is new"])
if st.button("Show next"):
    i = random.randint(0, len(headlines))
