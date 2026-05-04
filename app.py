import streamlit as st
from rag_chat import get_rag_response

st.set_page_config(page_title="AI Security Assistant")

st.title("🛡️ AI Security Policy Assistant")

st.write("Ask questions about GDPR, OWASP, CIS policies")

user_input = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_input:
        with st.spinner("Thinking..."):
            response = get_rag_response(user_input)
        st.success(response)