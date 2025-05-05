import streamlit as st

st.html("""In the following, you will see some news headlines one after the other. Each headline is presented for 7 seconds. 
        
        Please read each headline carefully and try to memorize them as well as possible. 
        
        Do not use any external tools to help you memorize the headlines as it is important for us to get an accurate understanding of participants' memory performance.
        Your reward is not affected by the number of items you remember.
        
        The first headline will be presented once you click on the "Start Experiment" button below.""")

if st.button("Start Experiment", key="start_experiment_button"):
    st.switch_page("memory_experiment/pages/presentation_page.py")