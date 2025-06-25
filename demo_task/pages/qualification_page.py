import streamlit as st
import pandas as pd
import os
import time

from core.scripts import user_repository, utils as core_utils
from demo_task.common import logic, utils
from demo_task.common.utils import get_and_increment_counts


def y_scale_animation(x, duration=50, offset=-0.2):
    return x * (max(0, min(1, (st.session_state.animation_timer / duration) - offset)))

def y_scale_animation_v2(x, max_x, duration=50, offset=0.2):
    return max(0, min(x, max_x * ((st.session_state.animation_timer / duration) - offset)))

if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = 0
    st.session_state.current_view = "sample"
    st.session_state.last_choice = 1
    st.session_state.current_sample = {}
    st.session_state.current_score = {"user": 0, "gpt": 0, "ties": 0}
    st.session_state.allow_update = True
st.session_state.page = "demo_task_sample" + str(st.session_state.qualification_progress)

# get index of sample
index = int(st.session_state.qualification_progress)

results_now = False

if st.session_state.current_view == "results":

    if st.session_state.current_score["user"] > st.session_state.current_score["gpt"]:
        victor = "Du"
    elif st.session_state.current_score["gpt"] > st.session_state.current_score["user"]:
        victor = "GPT"
    else:
        victor = "Tie"

    next_input = None

    st.markdown(f"""
# Ergebnisse

#### Siege für dich: {st.session_state.current_score["user"]}
#### Siege für ChatGPT: {st.session_state.current_score["gpt"]}
#### Unentschieden: {st.session_state.current_score["ties"]}
""")

    if victor == "Du":
        st.markdown("# Glückwunsch! Du bist menschlicher als ChatGPT.")
    elif victor == "GPT":
        st.markdown("# Tja!! Vielleicht bist du in Wirklichkeit der Computer...")
    elif victor == "Tie":
        st.markdown("# Unentschieden! Dein Sprachverständnis ähnelt wohl dem von ChatGPT.")

elif st.session_state.current_view == "sample":

    if st.session_state.qualification_progress == 0:

        st.markdown("""
# Hast du mehr 'Common Sense' als ChatGPT-4o?

Du wirst kurze Texte sehen, in denen ein mehrdeutiges Wort vorkommt (z.B. Bank) und eine seiner Bedeutungen (z.B. Sitzgelegenheit)

Auf einer Skala von 1 (Undenkbar) bis 5 (100% gewiss), bewerte, wie plausibel diese Bedeutung im Kontext ist. 

Du trittst gegen ChatGPT-4o an. Du bekommst Punkte, indem du die selbe Antwort wählst wie andere Menschen. 

Nach fünf Runden kommt die Auswertung.
        """)

        next_input = None

        if st.button(label="Los geht's!"):
            st.session_state.qualification_progress = 1
            st.rerun()

    else:

        # print text and widgets
        question, slider, next_input = utils.print_annotation_schema_sliders("qualification", index)

        annotation = {"question": question, "slider": slider}
        samples = core_utils.read_json_from_file(core_utils.TASK_INFO["demo_task"]["qualification_filepath"])

        if index == 1:
            st.session_state.allow_update = st.checkbox(label="Meine Stimme zur Gesamtheit zählen", value=True)


else:
    samples = core_utils.read_json_from_file(core_utils.TASK_INFO["demo_task"]["qualification_filepath"])
    question = samples[str(index)]

    user_choice = st.session_state.last_choice
    st.write(user_choice)
    next_input = None

    counts, precounts = utils.get_and_increment_counts(index, user_choice)
    agreeing_percentage = int((precounts[user_choice-1] / max(1, sum(counts)) * 100))
    gpt_agreeing_percentage = int((precounts[question["gpt_choice"]-1] / max(1, sum(counts)) * 100))

    oneshot_user = [0, 0, 0, 0, 0, 0]
    oneshot_user[user_choice-1] = 1 * max(1, (sum(counts) * 0.04))  # scale it so it remains visible
    #values = pd.DataFrame(list(zip(precounts, oneshot_user)), columns=["Menschen", "Du"])

    oneshot_gpt = [0, 0, 0, 0, 0, 0]
    oneshot_gpt[question["gpt_choice"] - 1] = 1 * max(1, (sum(counts) * 0.04))

    st.markdown(f"""
### Deine Wahl: {user_choice}

### ChatGPT wählt: {question["gpt_choice"]}

ChatGPT schreibt dazu: "*{question["gpts_opinion"]}*"
""")

    chart = st.empty()
    while st.session_state.animation_timer < 200:
        results_now = True
        values = pd.DataFrame(
            {
                "x": [1, 2, 3, 4, 5, "z"],
                "Menschen": [y_scale_animation_v2(x, max(precounts), duration=80, offset=1) for x in precounts] + [0],
                "Du": oneshot_user,
                "z": [0, 0, 0, 0, 0, max(precounts)*1.1],
                "ChatGPT": [y_scale_animation_v2(x, max(precounts), duration=20, offset=0.3) for x in oneshot_gpt]
            }
        )

        chart.bar_chart(data=values, x="x", color=("#00ff00", "#ff0000", "#0000ff", "#ffffff"), width=500, height=500, use_container_width=False)

        time.sleep(0.01)
        st.session_state.animation_timer += 1

    st.markdown(f"## {str(agreeing_percentage)}% wählten {user_choice} wie du.")
    if user_choice != question["gpt_choice"]:
        st.markdown(f"## {str(gpt_agreeing_percentage)}% wählten {question["gpt_choice"]} wie ChatGPT.")
    else:
        st.markdown(f"## ChatGPT hatte ebenfalls den gleichen Gedanken.")

    if agreeing_percentage > gpt_agreeing_percentage:
        st.markdown("# Glückwunsch! Ein Punkt für dich.")
    elif gpt_agreeing_percentage > agreeing_percentage:
        st.markdown("# Schade! Ein Punkt für ChatGPT.")
    else:
        st.markdown("# Diese Runde ist ein Unentschieden!")

    next_input = st.button(key=10 * index + 9, label="Weiter")


if next_input:
    if st.session_state.current_view == "sample":
        st.session_state.last_choice = slider
        st.session_state.current_view = "stats"
        st.session_state.animation_timer = 0
    else:
        st.session_state.current_view = "sample"
        st.session_state.qualification_progress += 1
        if st.session_state.qualification_progress > 5:
            st.session_state.current_view = "results"

    st.rerun()


if results_now and not next_input and st.session_state.current_view == "stats":
    if agreeing_percentage > gpt_agreeing_percentage:
        st.session_state.current_score["user"] += 1
    elif gpt_agreeing_percentage > agreeing_percentage:
        st.session_state.current_score["gpt"] += 1
    else:
        st.session_state.current_score["ties"] += 1