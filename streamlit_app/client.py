import streamlit as st
import requests
import json
import uuid


API_URL = "http://fastapi:8000/agent"

st.set_page_config(page_title="AI Travel Companion", page_icon=":airplane:")
st.title("Super Travel Companion")


if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if user_input := st.chat_input("Ask me about travel!"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        payload = {
            "user_input": user_input,
            "thread": st.session_state["thread_id"]
        }
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        agent_response = response.json()["response"]

        st.session_state.messages.append({"role": "assistant", "content": agent_response})
        with st.chat_message("assistant"):
            st.markdown(agent_response)

    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the backend API: {e}")
    except (KeyError, json.JSONDecodeError) as e:
        st.error(f"Error processing response from the API: {e}. Raw response: {response.text if hasattr(response, 'text') else 'No response text'}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")