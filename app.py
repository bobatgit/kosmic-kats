# Basic Streamlit chat app
#
# A chat app that returns a random integer and maintains history

import streamlit as st
import openai as ai
import numpy as np
import os
from dotenv import load_dotenv
import re


## INITIALIZATION ##
# Define the users
COMPUTER = {'name': 'Computer',
            'icon': "🐱"}
AI = {'name': 'The AI',
            'icon': "🧠"}
HUMAN = {'name': 'Human',
            'icon': "🧔"}

# Initialize variables
if 'chat_history' not in st.session_state:
    # Make sure this only runs the first time the app is initialised!
    # Otherwise the history and number will be erased!!!
    st.session_state.chat_history = []
    st.session_state.gpt_requests = []
    st.session_state.rand_num = np.random.randint(0,9)

# Load OpenAI
load_dotenv()
ai.api_key = os.environ["KEY_OPENAI"]


## FUNCTIONS ##
# Initialise the message writer
def save(user, txt):
    '''Saves a message to the chat history.'''
    num = len(st.session_state.chat_history) + 1
    st.session_state.chat_history.append(
        {"num": num,
        "user": user,
        "txt": txt})

def say(user, txt):
    '''Writes a message to the chat screen as str.'''
    with st.chat_message(user['name'], 
                        avatar=user['icon']):
        st.write(txt)
        
def say_and_save(user, txt):
    '''First saves the message to history then writes it to the screen'''
    save(user, txt)
    say(user, txt)

# OpenAI ChatGPT interface
def get_completion(prompt):
    """
    Takes user input text and tries to extract a number using GPT3.
    
    Returns a tuple with the extracted number and total GPT tokens used.
    """
    model="gpt-4"
    # TODO: GPT-4 is expensive. Use a lower cost model to extract numbers.
    prompt = f"""
        Given the text <{prompt}> what is the first number present? 
        Respond with the number []. If no number is found respond with [NaN].
        """
    messages = [{"role": "user", "content": prompt}]
    response = ai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    
    # Return the useful output
    useful_response = response.choices[0].message.content
    pattern = r'\[(.*?)\]'  # Regular expression pattern to match text within []
    matches = re.findall(pattern, useful_response)
    number = matches[0]

    # Track the GPT3 requests
    st.session_state.gpt_requests.append(
        {"num": len(st.session_state.gpt_requests),
         "input": prompt,
         "output": number,
         "tokens": response.usage.total_tokens,
         "full_response": response}
    )

    return number


# Define the Computer's message logic
def reply_message(input_txt:str):
    '''
    Takes the user input message and returns the computer response.
    Returns a tuple with the message and win condition.
    
    return (str, bool)
    '''

    try:
        input_int = int(input_txt)
    except:
        # Assume the input a number as text. Extract with GPT3.
        input_int = get_completion(input_txt)
        say_and_save(AI, f"The AI has found: {input_int}")
        if isinstance(input_int, str):
            if input_int == "NaN":
                return "Looks like GPT4 cannot see a number in your message. \
                    Please enter an integer between 0 and 9.", False
        # Now make it into an int
        input_int = int(input_int)

    if input_int < 0 or input_int > 9:
        return "This is not an integer between 0 and 9.", False
    
    if input_int == st.session_state.rand_num:
        return "This is the correct number! 🥳🎉🙌", True
    
    if input_int < st.session_state.rand_num:
        return "The secret number is higher.", False
    if input_int > st.session_state.rand_num:
        return "The secret number is lower.", False
    pass


## MAIN ##
# Start the UI and app
st.write("## Guess the secret number between 0 and 9!")

# Set the intro message from the Computer
# This should also only run once. Othewise the computer will spam.
if len(st.session_state.chat_history) < 1:
    save(COMPUTER, f"Try guessing the number. Type any integer from 0 to 9.")
    save(COMPUTER, f"I will tell you if its lower or higher.")    

# Show all the messages
for msg in st.session_state.chat_history:
        say(msg['user'], msg['txt'])

# Human chat entry
# MUST USE WALRUS OPERATOR (:=) to continuously add messages to the history
if prompt := st.chat_input("Type something to the computer...."):
    say_and_save(HUMAN, prompt)
    response, win = reply_message(prompt)
    say_and_save(COMPUTER, response)
    if win:
        st.balloons()


# Create the debug space
st.divider()
with st.expander("Show debug:", expanded=False):
    tab1, tab2, tab3 = st.tabs(["GPT3 Requests","Chat History","Random Number"])
    with tab1:
        st.write(st.session_state.gpt_requests)
    with tab2:
        st.write(st.session_state.chat_history)
    with tab3:
        st.write(st.session_state.rand_num)

