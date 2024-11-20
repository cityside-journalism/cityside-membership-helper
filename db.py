from supabase import create_client
import streamlit as st

SUPABASE_URL =  st.secrets["SB_URL"]
SUPABASE_KEY =  st.secrets["SB_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



def insert_subscriber(subscriber_id, status, timestamp_opt):
    """
    Inserts a new subscriber into the database if they do not already exist.

    Args:
        subscriber_id (str): The subscriber's unique ID or hash.
        status (str): The status of the subscriber (e.g., subscribed).
        timestamp_opt (str): The timestamp when the subscriber opted in.
    """
    try:
        # Check if the subscriber already exists
        existing_subscriber = supabase.table("subscribers").select("subscriber_hash").eq("subscriber_hash", subscriber_id).execute()

        if existing_subscriber.data:
            print(f"Subscriber with hash {subscriber_id} already exists. Skipping insertion.")
            return

        # Insert the new subscriber
        response = supabase.table("subscribers").insert(
            {
                "subscriber_hash": subscriber_id,
                "status": status,
                "created_at": timestamp_opt,
            }
        ).execute()
        

        # Log successful insertion
        print(f"Subscriber inserted: {response.data}")

    except Exception as e:
        # Handle errors raised by the API
        print(f"Error inserting subscriber: {e}")
