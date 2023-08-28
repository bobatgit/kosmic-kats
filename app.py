# Basic Streamlit app
#
# A counter with two buttons ++ and -- to change the score

import streamlit as st
import matplotlib.pyplot as plt

# Define initial session state variables
if 'my_int' not in st.session_state:
    st.session_state.my_int = [0]

# Callback functions
def my_int_chg(n):
    new_int = st.session_state.my_int[-1] + n
    st.session_state.my_int.append(new_int)


# Render page and UI
st.write(f"A first attempt at a living value which you can modify with buttons")
st.write(f"### The integer is: {st.session_state.my_int[-1]}")
st.text("")
st.text("")

col_a, col_b, col_rest = st.columns([0.1,0.1,0.8])
with col_a:
    st.button("👍 +", help="Increment the integer by one",
              on_click=my_int_chg, args=(1,))

with col_b:
    st.button("👎 -", help="Decrement the integer by one",
              on_click=my_int_chg, args=(-1,))

st.divider()
st.write(f"With a history: {st.session_state.my_int}")
# st.line_chart(data=st.session_state.my_int)
# Line chart with historic values
plt.style.use("dark_background")
fig, axs = plt.subplots(1, 2, layout='constrained')
axs[0].set_ylabel("Integer value")
axs[0].set_xlabel("Number of changes")
axs[1].set_ylabel("Number of occurences")
axs[1].set_xlabel("Integer value")

axs[0].plot(st.session_state.my_int)
axs[1].hist(st.session_state.my_int, bins=11)

st.pyplot(fig)