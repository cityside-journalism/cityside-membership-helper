import streamlit as st
from components import subscriber_activity_component
import data.members as members
import json
from utils import extract_slug_from_url, get_post_details
from datetime import datetime

st.title("Get Member Feed")

st.markdown("Retrieve and display activity feed for specific members.")

left_column, right_column = st.columns(2)
left_column, right_column = st.columns([3, 2])

with left_column:
    st.subheader("Select a Subscriber")

    subscriber_id, selected_file = subscriber_activity_component()

with right_column:
    st.subheader("See something here")
    if subscriber_id and selected_file:
        st.success(f"Selected Subscriber: {subscriber_id} from List: {selected_file}")

        # Extract list ID from the selected file
        list_id = None
        output_dir = "output"
        try:
            with open(f"{output_dir}/{selected_file}", 'r') as f:
                file_data = json.load(f)
                list_id = file_data.get("list_id", {}).get("list_id")
        except Exception as e:
            st.error(f"Error loading list ID from {selected_file}: {e}")

        # Fetch activity details if list ID is found
        if list_id:
            #st.info(f"Fetching activity for subscriber {subscriber_id}...")
            activity = members.get_member_feed(list_id, subscriber_id)

            # Display clicks with shorter date and slug
            if activity:
                st.write("### Click Activity Details")
                activities = activity.get("activity", [])
                clicks = [
                    act for act in activities if act["action"] == "click"
                ]


                # Track displayed post details
                displayed_posts = set()

                if clicks:
                    for idx, item in enumerate(clicks, start=1):
                        # Format the date
                        date_str = datetime.fromisoformat(item["timestamp"]).strftime("%Y-%m-%d")
                        # Extract the slug from the URL
                        slug = extract_slug_from_url(item.get("url", ""))

                        post_details = get_post_details(slug, list_id)


                        # Display the activity
                    # st.write(f"**{idx}.** Date: {date_str} | Slug: {slug if slug else 'No valid URL found'}")
                        if post_details and post_details not in displayed_posts:
                            st.write("Clicked: " + post_details)
                            displayed_posts.add(post_details)
                        
                else:
                    st.info("No click activity found for this subscriber.")
            else:
                st.error("Failed to fetch activity details. Please try again.")
        else:
            st.error("Unable to determine the list ID. Ensure the JSON file is properly formatted.")