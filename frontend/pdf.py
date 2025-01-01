import streamlit as st

from streamlit_pdf_viewer import pdf_viewer

container_pdf, container_chat = st.columns([50, 50])

with container_pdf:
    with st.popover("Add file"):
        pdf_file = st.file_uploader("Upload PDF", type=("pdf"))

        if pdf_file:
            binary_data = pdf_file.getvalue()
            pdf_viewer(input=binary_data, width=700)
    # prompt := st.chat_input("Say something", max_chars=350)
    prompt = st.chat_input("Say something", max_chars=350)