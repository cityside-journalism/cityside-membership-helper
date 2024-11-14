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




st.title("Welcome to My Streamlit App")
st.write("Now it has imported packages AND secrets secretley stored!")


#bside_subscribers = members.get_list_subscribers(berkeleyside_newsletter)
#print(len(bside_subscribers))
#st.write(bside_subscribers)