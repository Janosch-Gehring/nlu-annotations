import streamlit as st
from core.scripts import user_repository, database_repository
from captcha.image import ImageCaptcha
import random, string

length_captcha = 6
width = 200
height = 150
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

                    Never refresh the page or go back to the previous page, as this will cause the experiment to crash.
                    <p>By clicking the button below, you agree to participate in this experiment and give your consent to the use of your data for research purposes.
                    
                    <p>Please enter your prolific ID below:""")

            prolific_id = st.text_input("Prolific ID:", max_chars=200)
        if prolific_id:
            if "captcha_control" not in st.session_state:
                print("adding captcha control to session state")
                st.session_state.captcha_control = False
            col1, col2 = st.columns(2)
            if "captcha" not in st.session_state:
                print("adding captcha to session state")
                st.session_state.captcha = "".join(random.choices(string.ascii_letters + string.digits, k=length_captcha))
                print("the captcha is: ", st.session_state.captcha)
            Image = ImageCaptcha(width=width, height=height)
            data = Image.generate(st.session_state.captcha)
            col1.image(data)
            captcha_text = col2.text_input("Please enter the captcha text:", max_chars=length_captcha)
            if captcha_text:
                print("Captcha text entered: ", captcha_text)
                if captcha_text == st.session_state.captcha:
                    st.session_state.captcha_control = True
                    st.success("Captcha is correct!")
                    user_repository.create_user(target_id, task=task, data={"prolific_id": prolific_id})
                    user = user_repository.get_user(target_id)
                    st.session_state.user = list(user)
                    st.switch_page("memory_experiment/pages/presentation_page.py")
                else:
                    st.error("Captcha is incorrect. Please try again.")
