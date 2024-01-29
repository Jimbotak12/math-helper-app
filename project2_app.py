from streamlit_option_menu import option_menu
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import requests 
import openai
import os

# load the .env file
load_dotenv()

# get the secrety key
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        # {
        #     "role":"user",
        #     "content":"""
        #     I am a secondary school student seeking assistance in mathematic to sit in SPM exam. The specific topic or problem I need help with is algebra. The subtopic I want to get the understanding is Quadratic Equations. I hope can get the full support to get fully understanding about the topic."""
        # },
        # {
        #     "role":"assistant",
        #     "content":"""
        #     Absolutely, I'd be happy to help you with quadratic equations. Understanding this topic is essential for your SPM exam. Let's start by reviewing the basic concepts of quadratic equations and then we can work through some problems together.

        #     A quadratic equation is an equation of the form ax^2 + bx + c = 0, where a, b, and c are constants and a ≠ 0.

        #     The solutions to a quadratic equation can be found using the quadratic formula:
        #     x = (-b ± √(b^2 - 4ac)) / (2a)
        #     This formula gives the values of x which satisfy the quadratic equation.

        #     Now, let's work through some quadratic equation problems together. Here are a few questions to get started:

        #     Question 1: Solve the equation x^2 - 5x + 6 = 0

        #     Question 2: Solve the equation 2x^2 + 3x - 2 = 0

        #     Question 3: Solve the equation 3x^2 - 7x + 2 = 0

        #     Please provide your solutions for these questions, and I'll check them for you. If you need help or if you have any questions, feel free to ask!"""
        # },
        # {
        #     "role":"user",
        #     "content":"""
        #     1. (x-3)(x-2)
        #     2. (2x-1)(x+2)
        #     3. (x-2)(3x-1)"""
        # },
        # {
        #     "role":"assistant",
        #     "content":"""
        #     It looks like you have factored the quadratic equations instead of solving for the values of x. Let's work through the solutions together:

        #     Question 1: Solve the equation x^2 - 5x + 6 = 0
        #     To solve this quadratic equation, we can factorize it as (x-3)(x-2) = 0
        #     By setting each factor to zero, we have:
        #     x - 3 = 0   or   x - 2 = 0
        #     So, the solutions are:
        #     x = 3   or   x = 2

        #     Question 2: Solve the equation 2x^2 + 3x - 2 = 0
        #     To solve this quadratic equation, we can factorize it as (2x-1)(x+2) = 0
        #     By setting each factor to zero, we have:
        #     2x - 1 = 0   or   x + 2 = 0
        #     So, the solutions are:
        #     2x = 1   or   x = -2
        #     x = 1/2   or   x = -2

        #     Question 3: Solve the equation 3x^2 - 7x + 2 = 0
        #     To solve this quadratic equation, we can factorize it as (x-2)(3x-1) = 0
        #     By setting each factor to zero, we have:
        #     x - 2 = 0   or   3x - 1 = 0
        #     So, the solutions are:
        #     x = 2   or   3x = 1
        #     x = 2   or   x = 1/3

        #     Great effort in factoring the quadratic equations! You have successfully factored the quadratic equations, but remember that to solve the equations, we need to find the values of x. Keep practicing, and if you have any more questions or if there's anything else you'd like to discuss, feel free to ask!"""
        # }
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



