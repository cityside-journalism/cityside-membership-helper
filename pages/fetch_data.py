import streamlit as st
from components import get_newsletter_activity, get_list_members_button
from data.newsletters import newsletter_options


st.title("Fetch Mailchimp Data")
st.subheader("Pull data from the Mailchimp API")

selected_newsletter = st.selectbox("Choose a newsletter:", list(newsletter_options.keys()))

# Button to get newsletter activity
# if st.button("Get Newsletter Activity"):
#     get_newsletter_activity(selected_newsletter)

if get_list_members_button(selected_newsletter):
    st.write(f"Fetching members for {selected_newsletter}")
