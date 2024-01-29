from streamlit_option_menu import option_menu
from openai import OpenAI
import streamlit as st
import requests 
import openai
import os

# load the API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

# set the API key
openai.api_key = api_key

# Preference options
algebra_subtopic = ["Linear Equations and Inequalities","Quadratic Equations","Functions and Relations","Polynomials","Exponents and Logarithms","Any"]


def teacher_ai(chat):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=chat,
        temperature=0.5,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        
    msg = response.choices[0].message.content

    with st.spinner('Typing...'):
        st.session_state.messages.append({"role":'assistant','content':msg})
        st.chat_message("assistant").write(msg)
        # Add asssistant input to chat history
        chat.append({"role": "assistant", "content":msg})

    return chat

def main():
    system_prompt = """
        As a seasoned secondary school mathematics teacher with two decades of experience, specializing in guiding Sijil Pelajaran Malaysia (SPM) students. Your expertise extends to crafting and evaluating SPM examination papers. Your proficiency in solving SPM-level mathematical problems allows you to offer detailed step-by-step explanations to students. Your approach is supportive and encouraging, considering the academic level of secondary school students. The ways you approach the student, you will initially present the student with one SPM-level calculation questions. After that, you will discuss the answer given by student step by step calculation. Keep in mind during check the answer given by student, make sure the question you check same with the question given. Then, you will ask the student if he/she want another question until the student satisfied. During discussion you open the student tu ask any question. 
    """

    chat = [
        {
            "role": "system",
            "content": system_prompt,
        },   
    ]

    st.set_page_config(
        page_title="MathHelper",
        page_icon=":mortar_board:",
    )
    
    # Sidebar
    sb_style = """
    <style>
        .sidebar-title {
            font-size: 24px;
            font-family: 'Baskerville', sans-serif;
            text-align: center;
            color: #2B3A67;
        }
    </style>
    """
    st.sidebar.markdown(sb_style, unsafe_allow_html=True)
    st.sidebar.markdown('<span class="sidebar-title"><strong>Math Helper :mortar_board: </strong></span>', unsafe_allow_html=True)
    
    # Sidebar Input
    with st.sidebar:
        st.selectbox("Level",["SPM"])
        selected_method = st.selectbox("Method",["Teaching","Problem-Solving"])
        if selected_method == "Teaching":
            selected_topic = st.selectbox("Topic",['Algebra'])
            if selected_topic == 'Algebra':
                selected_subtopic = st.selectbox("Select the subtopic:", algebra_subtopic)

        # submit and clear button       
        col1, col2 = st.columns(2)

        with col1:
            submit_button = st.button("Start")

        with col2:
            clear_button = st.button("Clear")

    # Chat Bot
    st.title("Math Helper :mortar_board:")
    st.markdown()

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo-1106"

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role":"assistant","content":"How can I help you"}]
        
    for msg in st.session_state.messages:
        role = msg.get("role", "")
        if role in ["user", "assistant"]:
            st.chat_message(role).write(msg["content"])
    
    # After click the clear button
    if clear_button:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you"}]
        st.session_state.user_input = ""

    # After click start button
    if submit_button:
        st.session_state.messages = [ ]
        # Auto generate user input
        user_input = f"I am a secondary school student seeking assistance in mathematic to sit in SPM exam. The specific topic or problem I need guidance is {selected_topic}. The subtopic I want to get more the understanding is {selected_subtopic}. I hope can get the full support to get fully understanding about the topic."
        
        with st.spinner("Generating..."):
            # Display user input in chat message
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)
            # Add user input to chat history
            chat.append({"role": "user", "content": user_input})
    
        # Get response from ai
        chat = teacher_ai(chat)

    # User typing input
    if user_input := st.chat_input("Type message"):
        with st.spinner("Generating..."):
            # Display user input in chat message
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)       
            # Add user input to chat history
            chat.append({"role": "user", "content": user_input})

            # Get response from ai
            chat = teacher_ai(chat)

if __name__ == "__main__":
    main()



