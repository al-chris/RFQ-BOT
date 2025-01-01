import streamlit as st
import pandas as pd
import requests
import json
import pyperclip
from util import clean_json_string

# Page configuration
st.set_page_config(page_title="RFQ BOT", layout="wide")

# Title section
# st.markdown("<h1 style='background-color:#B22222; color: white; text-align: center; padding: 10px;'>RFQ BOT</h1>", unsafe_allow_html=True)
st.title("RFQ BOT")



def display_data(email_id):
    resp = requests.get(f"http://localhost:8000/emails/{email_id}")
    response = resp.json()
    with st.container():
        m_col1, m_col2 = st.columns([1, 1])
        with m_col1:
            with st.expander("Subject: Request for Quote"):
                # subject = st.text_area("Enter Subject")
                st.write(response.get("body"))
            
        with m_col2:    
            # Expander for Suppliers
            with st.expander("Suppliers:"):
                suppliers = st.markdown(response.get("template_json"))

        # Expander for Template
        with st.expander("Template:"):
            template = st.markdown("""
                                
                                    Dear Supplier,

                                    We are looking for quotations for the following items:

                                    
                                    """)
            
            a = st.table(pd.DataFrame(json.loads(clean_json_string(response.get("template_table")))))
            st.markdown("""
                        \n
                            Please provide your best price and delivery time for each item.

                            Thank you,
                            Procurement Team
                        """)
            col1, col2 = st.columns([1, 1], gap="medium", vertical_alignment="center")
            with col1:
                if st.button("Regenerate", use_container_width=True):
                    st.write("Regenerate template (not implemented yet)")
            with col2:
                if st.button("Copy", use_container_width=True):
                    st.write("Template copied to clipboard (not implemented yet)")


# Sidebar (Emails section)
emails = requests.get("http://localhost:8000/emails/").json()
st.sidebar.header("Emails:")
for email in emails:
    button = st.sidebar.button(f"{email.get("subject")}", use_container_width=True, key=email.get("email_id"))
    if button:
        display_data(email.get("email_id"))

