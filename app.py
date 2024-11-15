import streamlit as st
import openai
import json
import os
import requests
import pandas as pd
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
#from google.colab import userdata
import json
import urllib.parse
from data.newsletters import *
import data.members as members



API_KEY = st.secrets["API_KEY"]
MC_KEY = st.secrets["MC_KEY"]
OPEN_AI_KEY =st.secrets["OPEN_AI_KEY"]

SERVER_PREFIX = 'us2'  # Replace 'usX' with your specific Mailchimp server prefix
BASE_URL = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0/'
HEADERS = {
    'Authorization': f'Bearer {MC_KEY}'
    }

"""
GET LIST SUBSCRIBERS:
get_list_subscribers only fetches some data from MC api, specified in fields. It also only fetches those who are subscribed.
It paginates, fetching a batch of 100 each time, until it reaches the end of the list. Pass in a list ID from above.

"""

newsletter_options = {
    "Major Donors": major_donors,
    "Cityside Main Audience": cityside_main_audience,
    "Cityside Master List": cityside_master_list,
    "May 24 Major Donors": may24_major_donors,
    "Oaklandside Newsletter": oaklandside_newsletter,
    "Berkeleyside Newsletter": berkeleyside_newsletter,
    "Richmondside Newsletter": richmondside_newsletter
}



st.title("Citysie membership manager")
st.write("Now it has imported packages AND secrets secretley stored!")

st.subheader("Newsletter")
selected_newsletter = st.selectbox("Choose a newsletter:", list(newsletter_options.keys()))

if st.button("Submit"):
    # Placeholder action
    st.write(f"Button works! You selected: {selected_newsletter}")


#bside_subscribers = members.get_list_subscribers(berkeleyside_newsletter)
#print(len(bside_subscribers))
#st.write(bside_subscribers)