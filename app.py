import streamlit as st
import base64
from openai import OpenAI
import os
import time
from config import API_KEY


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", API_KEY))
thread = client.beta.threads.create()


# Hide the audio player using custom CSS
hide_audio_player = """
    <style>
    audio {
        display: none;
    }
    </style>
    """

# Inject the CSS into the app
#st.markdown(hide_audio_player, unsafe_allow_html=True)
c_audio = st.audio("music/track_1.mp3", format="audio/mp3", loop=True, start_time=0, autoplay=True)



def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    
def create_thread_and_run(user_input):
    custom_gpt_id = 'asst_wc3l1Lp3C5dcsVAH7SPPxNtO'
    thread = client.beta.threads.create()
    run = submit_message(custom_gpt_id, thread, user_input)
    return thread, run
    
# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()


# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run







def generate(text):
    thread1, run1 = create_thread_and_run(
    text
  )
    # Wait for Run 1
    run1 = wait_on_run(run1, thread1)
    response = get_response(thread1)
    for message in response.data:
        if message.role == "assistant":
            return message.content[0].text.value



if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you? You can tell me about your project or ask any professional data."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"],avatar="images/brain_4.webp").write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    msg = generate(prompt)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant",avatar="images/brain_4.webp").write(msg)
