import streamlit as st
from components import sync_subscribers_component
from db import insert_subscriber


st.title("Sync Members")
st.markdown("Use this page to sync subscribers from a JSON file to the database.")

# Step 1: Use the component to select and load a file
file_data = sync_subscribers_component()

# Step 2: Sync subscribers if a file is selected
if file_data:
    list_id = file_data.get("list_id", {}).get("list_id")
    subscribers = file_data.get("data", [])

    if not subscribers:
        st.warning("No subscribers found in the selected file.")
    else:
        added_count = 0
        total_subscribers = len(subscribers)
        progress_bar = st.progress(0)

        for idx, subscriber in enumerate(subscribers, start=1):
            try:
                subscriber_id = subscriber["id"]
                status = subscriber["status"]
                timestamp_opt = subscriber["timestamp_opt"]

                # Insert into the database
                insert_subscriber(subscriber_id, status, timestamp_opt)
                added_count += 1

                # Update the progress bar
                progress_percentage = int((idx / total_subscribers) * 100)
                progress_bar.progress(progress_percentage)


            except KeyError as e:
                st.error(f"Missing key in subscriber data: {e}")

        st.success(f"Successfully synced {added_count} subscribers to the database.")
