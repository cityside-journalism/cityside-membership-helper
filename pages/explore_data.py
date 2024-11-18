# pages/explore_data.py

import streamlit as st
import json
import pandas as pd
import os

# Set the directory containing JSON files
data_dir = "output"

# Get a list of all JSON files in the directory
data_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]

# File selector in Streamlit
selected_file = st.selectbox("Select a data file to explore:", data_files)

# Only proceed if a file is selected
if selected_file:
    # Load the selected JSON file
    data_file_path = os.path.join(data_dir, selected_file)
    with open(data_file_path, 'r') as f:
        data = json.load(f)

    # Check for type of data based on keys
    if "metadata" in data and "data" in data:  # Subscriber data with stats
        st.title("Subscriber Data Summary")
        
        # Extract metadata
        metadata = data.get("metadata", {})
        record_count = metadata.get("record_count", 0)
        fetch_timestamp = metadata.get("fetch_timestamp", "N/A")
        
        # Extract subscriber data and convert to DataFrame
        subscriber_data = data.get("data", [])
        df = pd.DataFrame(subscriber_data)

        # Calculate statistics
        avg_click_rate = df["stats"].apply(lambda x: x["avg_click_rate"]).mean()
        max_click_rate = df["stats"].apply(lambda x: x["avg_click_rate"]).max()
        avg_open_rate = df["stats"].apply(lambda x: x["avg_open_rate"]).mean()
        max_open_rate = df["stats"].apply(lambda x: x["avg_open_rate"]).max()

        # Display summary
        st.write(f"**Selected File:** {selected_file}")
        st.write(f"**Record Count:** {record_count}")
        st.write(f"**Fetch Timestamp:** {fetch_timestamp}")
        st.write(f"**Average Click Rate:** {avg_click_rate:.4f}")
        st.write(f"**Highest Click Rate:** {max_click_rate:.4f}")
        st.write(f"**Average Open Rate:** {avg_open_rate:.4f}")
        st.write(f"**Highest Open Rate:** {max_open_rate:.4f}")

        # Display the first few rows of the data for context
        st.write("### Sample Data")
        st.write(df.head())

    elif "newsletter_data" in data:  # Newsletter data without stats
        st.title("Newsletter Data Summary")
        
        # Extract and display basic information
        newsletter_metadata = data.get("newsletter_data", {}).get("metadata", {})
        record_count = newsletter_metadata.get("record_count", "Unknown")
        creation_date = newsletter_metadata.get("creation_date", "N/A")
        
        st.write(f"**Selected File:** {selected_file}")
        st.write(f"**Record Count:** {record_count}")
        st.write(f"**Creation Date:** {creation_date}")
        
        # Display raw data or other relevant fields if available
        st.write("### Sample Data")
        st.write(data.get("newsletter_data", {}).get("data", []))

    else:
        st.error("Unknown file format. Unable to process this file type.")
else:
    st.error("No data file selected.")