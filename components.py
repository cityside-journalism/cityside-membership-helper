# components.py

import streamlit as st
from data.newsletters import *
import data.members as members
from datetime import datetime
from utils import store_as_json

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
        # Call the get_list_subscribers function from members.py
        response_list = members.get_list_subscribers(list_id, selected_newsletter)

        # Check if we received a response and save as JSON if successful
        if response_list is not None:
            success, old_metadata, new_metadata = store_as_json(response_list, selected_newsletter)
            if success:
                st.success(f"Successfully fetched and saved {len(response_list)} members from {selected_newsletter}.")
                
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
        else:
            st.error(f"Failed to fetch members from {selected_newsletter}.")


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