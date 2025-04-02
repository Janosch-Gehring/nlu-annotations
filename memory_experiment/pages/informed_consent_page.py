import streamlit as st
from core.scripts import user_repository, database_repository

target_id = st.session_state.user_id
user = user_repository.get_user(target_id)
task = st.session_state.task

if not user:
        with st.container():
            st.html("<h1>Welcome to this Experiment!")
            st.html("""<h2>This is the informed consent form for the experiment. Please read it carefully before continuing.
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                    Morbi faucibus, magna non egestas varius, ante mi hendrerit tortor, non volutpat dolor risus id eros. 
                    Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; 
                    Pellentesque pharetra luctus felis blandit feugiat. Pellentesque rhoncus bibendum rhoncus. 
                    Nam luctus velit ante, nec laoreet ipsum porta eget. Suspendisse potenti. Ut maximus malesuada quam ac euismod.
                    Pellentesque imperdiet, elit ac rutrum efficitur, urna ipsum molestie lorem, sit amet consectetur risus nulla at diam. 
                    Pellentesque in purus ut erat egestas dapibus ac eget erat.
                    
                    <h2>Suspendisse sed neque lorem. Quisque a felis sit amet turpis semper efficitur. 
                    <p>Cras lacinia eget sapien vel malesuada. 
                    Praesent pretium rhoncus justo, sit amet viverra nulla tempus id. 
                    Proin nec posuere dolor. Phasellus fermentum vel arcu eu sagittis. 
                    Donec egestas vitae justo et sodales. Mauris non ipsum leo. Suspendisse potenti. 
                    Praesent at bibendum purus, quis auctor nunc. Nunc nisi tortor, varius volutpat efficitur ut, 
                    ullamcorper a mi. Ut felis nunc, blandit sagittis tellus sit amet, sagittis tristique justo. 
                    Suspendisse potenti.
                    
                    <p>Please enter your prolific ID below:""")

            prolific_id = st.text_input("Prolific ID:", max_chars=200)
        if prolific_id:
            user_repository.create_user(target_id, task=task, data={"prolific_id": prolific_id})
            user = user_repository.get_user(target_id)
            st.session_state.user = list(user)
            st.switch_page("memory_experiment/pages/presentation_page.py")
