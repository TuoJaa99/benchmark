import streamlit as st

 

model = st.selectbox("Select a model:", ['llama3.1:8b', 'llama']) 

token = st.text_input("TOKEN:")
url = st.text_input("URL:")

timeout = st.slider("Timeout", min_value=10,max_value=120, step=10)

rounds = st.slider("Rounds", min_value=5, max_value=100, step=5)

prompts = st.file_uploader("Choose a file", type=['txt'])

if prompts is not None:
    lines = prompts.read().decode("utf-8").splitlines()

    for i, line in enumerate(lines):
        st.write(f"Line{i+1}:")
        st.code(line.strip())

if st.button("Click me"):
    


