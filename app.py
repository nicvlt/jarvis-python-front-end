import grpc
import text_to_ast_pb2
import text_to_ast_pb2_grpc

import streamlit as st

channel = grpc.insecure_channel("localhost:3005")
stub = text_to_ast_pb2_grpc.TextToAstStub(channel)


def send_message(session_messages):
    response = stub.ProcessText(
        text_to_ast_pb2.TextToAstConversation(
            messages=[
                {"role": message["role"], "content": message["content"]}
                for message in session_messages
            ]
        )
    )
    response = response.messages[-1].content
    return response


st.title("Welcome to Jarvis")
st.subheader("Your personal financial copilot", divider=True)

st.markdown(
    "To get started, describe your financial strategy in the chat box below. Jarvis will provide you with a JSON representation of your strategy."
)

# Messages are stored in the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            st.json(message["content"])

# Recommendation/Examples: "If the RSI is greater than 70, sell all stocks", "If the SMA 10 is greater than the SMA 20, place an order of 10"
st.markdown("Here are some examples of financial strategies:")
st.markdown("1. If the RSI is greater than 70, sell all stocks")
st.markdown("2. If the SMA 10 is greater than the SMA 20, place an order of 10")

# This is the main chat input
if prompt := st.chat_input(placeholder="Describe your financial strategy"):
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    jarvis_response = send_message(session_messages=st.session_state.messages)

    with st.chat_message("assistant"):
        st.json(jarvis_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": jarvis_response}
        )

        st.download_button(
            label="Download JSON",
            data=jarvis_response,
            file_name="AST.json",
            mime="application/json",
        )
