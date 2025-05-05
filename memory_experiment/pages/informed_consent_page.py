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
            st.html("""
<h1>Informed Consent of Participation 
<p>You are invited to participate in the online study Memorability And Credibility Of News Headlines initiated and conducted by Selina Meyer. The research is supervised by Prof. Dr. Michael Roth and Prof. Dr. Magdalena Abel at the UTN Nuremberg. Please note: Your participation is enitrely voluntary The online study will last approximately ... minutes We will record personal demographics (age, gender, etc.) We may publish our results from this and other sessions in our reports, but all such reports will neither include your name nor cannot be associated with your identity. If you have any questions or complaints about the whole informed consent process of this research study or your rights as a human reserach subject, please contact Selina Meyer (E-Mail: selina.meyer@utn.de) or Prof. Dr. Michael Roth & Prof. Dr. Magdalena Abel. You should carefully read the information below. Please take as much time as you need to read the consent form. 
<h2>1. Purpose and Goal of this Research
<p>The purpose of the research project is to identify the dynamics at play in the proliferation of misinformation online. The goal of this study is to explore to which extent certain linguistic features affect memorability and truthfulness judgements of news headlines. Your participation will help us achieve this goal. The results of this research may be presented at scientific or professional meetings or published in scientific proceedings and journals. 
<h2>2. Participation and Compensation
<p>Your participation in this online study is completely voluntary. You will be one of approximately 24 people being surveyed for this research. You will receive 5 EUR as compensation for your participation. You may withdraw and discontinue participation at any time without penalty or losing the compensation. If you decline to participate or withdraw from the online study, no one on the campus will be told. You may refuse to answer any questions you do not want to answer. 
<h2>3. Procedure
<p>After confirming your informed consent you will: 1. Be presented with 16 news headlines one after another with the task to memorize them as well as possible. 2. In the next step, you will be tasked to recall as many headlines as possible from memory. 3. You will be shown headlines again, and tasked to decide whether they have previously seen the headline or not. 4. You will be shown the headlines a third time and asked to judge their perceived truthfulness of the headlines. 5. answer demographic questions The complete procedure of this online study will last approximately 20 minutes. 
<h2>4. Risks and Benefits
<p>There are no risks associated with this online study. Discomforts or inconveniences will be minor and are not likely to happen. If any discomforts become a problem, you may discontinue your participation. Your benefit in participating is your compensation of 5 EUR. 
<h2>5. Data Protection and Confidentiality
<p>Personal data (age, gender, etc.) will be recorded while participation. The researcher will not identify you by your real name in any reports using information obtained from this online study and that your confidentiality as a participant in this online study will remain secure and encrypted. All data you provide in this online study will be published anonymized and treated confidentially in compliance with the General Data Protection Regulation (GDPR) of the European Union (EU). Subsequent uses of records and data will be subject to standard data use policies which protect the full anonymity of the participating individuals. In all cases, uses of records and data will be subject to the GDPR. Faculty and administrators from the campus will not have access to raw data or transcripts. This precaution will prevent your individual comments from having any negative repercussions. This site uses cookies and other tracking technologies to conduct the research, to improve the user experience, the ability to interact with the system and to provide additional content from third parties. Despite careful control of content, the researchers assume no liability for damages, which directly or indirectly result from the use of this online application. Any recordings cannot be viewed by anyone outside this research project unless we have you sign a separate permission form allowing us to use them (see below). Records that have not been made public are automatically deleted after the end of the research. The records will be destroyed if you contact the researcher to destroy or delete them immediately. As with any publication or online related activity, the risk of a breach of confidentiality is always possible. According to the GDPR, the researchers will inform the participant if a breach of confidential data was detected. 
<h2>6. Identification of Investigators
<p>If you have any questions or concerns about the research, please feel free to contact: 
                    Selina Meyer 
                    selina.meyer@utn.de 
                    Natural Language Understanding Lab 
                    Department of Computer Science and Artificial Intelligence 
                    University of Technology Nuremberg 
                    Germany 
<p>By clicking the button below below, you agree to participate in this experiment and give your consent to the use of your data for research purposes. 
<p>Please enter your prolific ID below:
""")
    
            prolific_id = st.text_input("Prolific ID:", max_chars=200)
            agree = st.checkbox("I have read and understood the information above and agree to participate in this experiment")
        if prolific_id and agree:
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
                    st.switch_page("memory_experiment/pages/Experiment_description_page.py")
                else:
                    st.error("Captcha is incorrect. Please try again.")
            if st.button("Generate new Captcha"):
                st.session_state.captcha = "".join(random.choices(string.ascii_letters + string.digits, k=length_captcha))
                print("the captcha is: ", st.session_state.captcha)
                st.rerun()