# Basic Streamlit chat app
#
# A chat app that returns a random integer and maintains history

import streamlit as st
import numpy as np

# Define the users
COMPUTER = {'name': 'Computer',
            'icon': "🐱"}
HUMAN = {'name': 'Human',
            'icon': "🧔"}


# Initialize variables
if 'chat_history' not in st.session_state:
    # Make sure this only runs the first time the app is initialised!
    # Otherwise the history and number will be erased!!!
    st.session_state.chat_history = []
    st.session_state.rand_num = np.random.randint(0,9)


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

# Define the Computer's message logic
def reply_message(input_txt:str):
    '''
    Takes the user input message and returns the computer response.
    Returns a tuple with the message and win condition.
    
    return (str, bool)
    '''

    wrong_int_txt = "This is not an integer between 0 and 9.", False
    try:
        input_int = float(input_txt)
    except:
        return wrong_int_txt    
    if input_int < 0 or input_int > 9:
        return wrong_int_txt
    
    if input_int == st.session_state.rand_num:
        return "This is the correct number! 🥳🎉🙌", True
    
    if input_int < st.session_state.rand_num:
        return "The secret number is higher.", False
    if input_int > st.session_state.rand_num:
        return "The secret number is lower.", False
    pass


## Start the UI and app
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
    st.write(st.session_state.rand_num)
    st.write(st.session_state.chat_history)
