# components.py

import streamlit as st
from data.newsletters import *
import data.members as members
from datetime import datetime
from utils import store_as_json
import pandas as pd
import os
import json

MC_KEY = st.secrets["MC_KEY"]
SERVER_PREFIX = 'us2'  # Replace 'usX' with your specific Mailchimp server prefix
BASE_URL = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0/'
HEADERS = {
    'Authorization': f'Bearer {MC_KEY}'
    }
 

def get_list_members_button(selected_newsletter):
    """Button component to get list members for the selected newsletter."""
    list_id = newsletter_options[selected_newsletter]
    button_label = f"Get {selected_newsletter} list members"

    if st.button(button_label):
        # Call get_list_subscribers
        success, old_metadata, new_metadata = members.get_list_subscribers(list_id, selected_newsletter)

        # Display messages based on the result
        if success:
            st.success(f"Successfully fetched and saved new members from {selected_newsletter}.")
            st.write("### Metadata Comparison")
            st.write("**Previous Fetch**")
            st.write(f"Timestamp: {old_metadata.get('fetch_timestamp', 'N/A')}")
            st.write(f"Record Count: {old_metadata.get('record_count', 'N/A')}")
            st.write("**Current Fetch**")
            st.write(f"Timestamp: {new_metadata['fetch_timestamp']}")
            st.write(f"Record Count: {new_metadata['record_count']}")
        else:
            st.error(f"Failed to fetch or save members from {selected_newsletter}.")



def get_newsletter_activity(selected_newsletter, store_as_json):
    """Component to fetch and display newsletter activity."""
    # Fetch the chosen newsletter activities
    chosen_newsletter_activities = members.get_list_activities(newsletter_options[selected_newsletter])
    print(f"Total retrieved: {len(chosen_newsletter_activities)}")

    # Save as JSON with metadata and retrieve previous vs. current metadata
    success, old_metadata, new_metadata = store_as_json(chosen_newsletter_activities, selected_newsletter)

    if success:
        st.write(f"The {selected_newsletter} contains {len(chosen_newsletter_activities)} records")
        st.success("Data saved successfully!")
        
        # Display metadata comparison
        st.write("### Metadata Comparison")
        st.write("**Previous Fetch**")
        st.write(f"Timestamp: {old_metadata.get('fetch_timestamp', 'N/A')}")
        st.write(f"Record Count: {old_metadata.get('record_count', 'N/A')}")

        st.write("**Current Fetch**")
        st.write(f"Timestamp: {new_metadata['fetch_timestamp']}")
        st.write(f"Record Count: {new_metadata['record_count']}")
    else:
        st.error("Failed to save data. Please try again.")



def subscriber_activity_component(output_dir="output"):
    """
    A component to select a subscriber list, paginate its subscribers, and show a button for each subscriber.
    Args:
        output_dir (str): The directory containing JSON files with subscriber lists.
    """
    st.subheader("Subscriber Activity")

    # Step 1: Load and select a JSON file
    files = [f for f in os.listdir(output_dir) if f.endswith(".json")]
    subscriber_files = {}
    for file in files:
        file_path = os.path.join(output_dir, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
        if "list_id" in data:  # Check if it's a valid subscriber list
            subscriber_files[file] = data

    if not subscriber_files:
        st.warning("No subscriber lists found.")
        return None, None

    selected_file = st.selectbox("Select a subscriber list:", list(subscriber_files.keys()))
    if not selected_file:
        return None, None

    list_data = subscriber_files[selected_file]["data"]
    st.write(f"Selected List: {selected_file}")

    # Step 2: Paginate and sort subscribers
    page_size = 25  # Show 25 subscribers per page
    df = pd.json_normalize(list_data)
    df = df.sort_values(by="stats.avg_click_rate", ascending=False)  # Sort by open rate
    total_pages = (len(df) - 1) // page_size + 1

    current_page = st.number_input("Page", min_value=1, max_value=total_pages, step=1, value=1) - 1
    paginated_df = df.iloc[current_page * page_size:(current_page + 1) * page_size]

    if paginated_df.empty:
        st.info("No subscribers on this page.")
        return None, None

    #Step 3: Display buttons for each subscriber
    for idx, subscriber in paginated_df.iterrows():
        subscriber_id = subscriber["id"]
        click_rate = subscriber["stats.avg_click_rate"]
        if st.button(f" {idx}: (Click Rate: {click_rate:.2%})"):
            return subscriber_id, selected_file
        
   

    return None, None