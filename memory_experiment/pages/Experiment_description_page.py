import streamlit as st

st.html("""<p>In the following, you will see some news headlines one after the other. Each headline is presented for 7 seconds. 
        
        <br>Please read each headline carefully and try to memorize them as well as possible. 
        
        <br>Do not use any external tools to help you memorize the headlines as it is important for us to get an accurate understanding of participants' memory performance.
        <br>Your reward is not affected by the number of items you remember.
        
        <br>The first headline will be presented once you click the "Start Experiment" button below.""")

if st.button("Start Experiment", key="start_experiment_button"):
    st.switch_page("memory_experiment/pages/presentation_page.py")