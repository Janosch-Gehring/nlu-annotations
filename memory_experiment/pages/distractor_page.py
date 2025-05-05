"""import streamlit as st
import time

def release_the_balloons(time_left):
    st.write(f"Time left: {60 - time_left} seconds")
    st.balloons()

@st.fragment(run_every=15)
def distraction():
    if "time" not in st.session_state:
        st.session_state.time = 0
        release_the_balloons(time_left=st.session_state.time)
    else:
        st.session_state.time += 15
        if st.session_state.time >= 60:
            st.session_state.time = 0
            st.switch_page("memory_experiment/pages/recall_page.py")
        else:
            release_the_balloons(time_left=st.session_state.time)

distraction()"""

import streamlit as st
import time

with st.spinner("Please wait for one minute before continuing", show_time=True):
    time.sleep(60)
st.switch_page("memory_experiment/pages/recall_page.py")