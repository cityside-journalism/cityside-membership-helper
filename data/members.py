import streamlit as st
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import requests
import os
from datetime import datetime
import json
from utils import *

API_KEY = st.secrets["API_KEY"]
MC_KEY = st.secrets["MC_KEY"]
SERVER_PREFIX = 'us2'  # Replace 'usX' with your specific Mailchimp server prefix
BASE_URL = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0/'
HEADERS = {
    'Authorization': f'Bearer {MC_KEY}'
    }

def get_existing_subscriber_ids(file_path):
    """Load existing subscriber IDs from the JSON file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return {member["id"] for member in data.get("data", [])}
    return set()

def get_list_subscribers(list_id, list_name):
    print("GETTING LIST SUBSCRIBERS>>>")
    try:
        MC_KEY = st.secrets["MC_KEY"]
        SERVER_PREFIX = 'us2'
        
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": MC_KEY,
            "server": SERVER_PREFIX
        })

        # Path for checking existing subscribers
        file_path = f"output/{list_name.replace(' ', '_').lower()}.json"

        # Load existing subscriber IDs
        existing_ids = get_existing_subscriber_ids(file_path)

        # Prepare to collect new subscribers
        response_list = []
        offset = 0
        count = 100  # Number of records to fetch per request
        total_members = 0

        # Specify the fields you want to retrieve
        fields = [
            "members.id",
            "members.status",
            "members.stats.avg_open_rate",
            "members.stats.avg_click_rate",
            "members.timestamp_opt",
            "members.tags"
        ]

        # Get total count to manage progress
        list_info = client.lists.get_list(list_id)
        total_count = list_info['stats']['member_count']
        st.write(f"Total members in list: {total_count}")

        progress_bar = st.progress(0)

        while True:
            response = client.lists.get_list_members_info(
                list_id,
                count=count,
                offset=offset,
                fields=fields,
                status='subscribed'
            )
             

            # Filter out existing members
            new_members = [
                member for member in response["members"]
                if member["id"] not in existing_ids
            ]

            total_members += len(new_members)
            response_list.extend(new_members)

            # Update progress
            progress = min((offset + count) / total_count, 1.0)
            progress_bar.progress(progress)
            print(f"Progress: {progress}")

            # Check if we've retrieved all members
            if len(response["members"]) < count:
                 
                break  # No more members to fetch


            offset += count  # Move to the next batch of members

        progress_bar.empty()

        # Save data using store_as_json
        if response_list:
            success, old_metadata, new_metadata = store_as_json(response_list, list_name, {"list_id": list_id})
            return success, old_metadata, new_metadata
        else:
            return False, {}, {}

    except ApiClientError as error:
        print(f"API Client Error: {error.text}")
        return False, {}, {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, {}, {}


def get_list_activities(list_id):
    all_activities = []
    count = 1000
    offset = 0

    while True:
        params = {
            'count': count,
            'offset': offset
        }

        url = BASE_URL + 'lists/'+ list_id + '/activity'
        response = requests.get(url, headers=HEADERS, params=params)

        # Error check
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json()}")
            break

        activities = response.json().get('activity', [])
        if not activities:
            print("No activities found.")
            break

        all_activities.extend(activities)
        offset += len(activities)

        # Break the loop if the number of returned activities is less than the count, meaning it's the last batch
        if len(activities) < count:
            break

    return all_activities



def get_member_activity(list_id, subscriber):

  try:
    client = MailchimpMarketing.Client()
    client.set_config({
      "api_key": API_KEY,
      "server": SERVER_PREFIX
    })

    query_parameters = {
        "count": 100,  # Limit the number of activities to fetch
        "activity_filters": "click"
    }

    response = client.lists.get_list_member_activity(list_id, subscriber,count=100)
    #print(response)
  except ApiClientError as error:
    print("Error: {}".format(error.text))

  return response

def get_member_feed(list_id, subscriber):
    
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
          "api_key": API_KEY,
          "server": SERVER_PREFIX
        })

        response = client.lists.get_list_member_activity_feed(list_id, subscriber)
        print(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
    