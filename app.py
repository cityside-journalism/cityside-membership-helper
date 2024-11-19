import streamlit as st
import openai
# import json
# import os
# import pandas as pd
# import mailchimp_marketing as MailchimpMarketing
# from mailchimp_marketing.api_client import ApiClientError
# #from google.colab import userdata
# import urllib.parse
from components import *
from data.newsletters import *
import data.members as members
from utils import *
from datetime import datetime
from pages import fetch_data, explore_data  # Import your pages




API_KEY = st.secrets["API_KEY"]
MC_KEY = st.secrets["MC_KEY"]
OPEN_AI_KEY =st.secrets["OPEN_AI_KEY"]

SERVER_PREFIX = 'us2'  # Replace 'usX' with your specific Mailchimp server prefix
BASE_URL = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0/'
HEADERS = {
    'Authorization': f'Bearer {MC_KEY}'
    }

 

# st.sidebar.title("Navigation")
# page = st.sidebar.selectbox("Go to", ["Fetch Data", "Explore Data"])

# # Load the selected page
# if page == "Fetch Data":
#     fetch_data  # Fetch Data page functionality
# elif page == "Explore Data":
#     explore_data  # Explore Data page functionality


st.title("Cityside Membership Helper")
 st.write("Now with supabase!")
 
# selected_newsletter = st.selectbox("Choose a newsletter:", list(newsletter_options.keys()))

# if st.button("Get Newsletter Activity"):
#     get_newsletter_activity(selected_newsletter, store_as_json)

# if get_list_members_button(selected_newsletter):
#     st.write(f"Fetching members for {selected_newsletter}")

st.markdown("<hr style='border: 1px solid #ccc; margin: 20px 0;'>", unsafe_allow_html=True)
