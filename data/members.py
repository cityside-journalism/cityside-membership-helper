import streamlit as st
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError


MC_KEY = st.secrets["MC_KEY"]
SERVER_PREFIX = 'us2'  # Replace 'usX' with your specific Mailchimp server prefix
BASE_URL = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0/'
HEADERS = {
    'Authorization': f'Bearer {MC_KEY}'
    }



def get_list_subscribers(list_id):
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": MC_KEY,
            "server": SERVER_PREFIX
        })

        response_list = []
        offset = 0
        count = 100  # Number of records to fetch per request
        total_members = 0

        # Specify the fields you want to retrieve
        fields = [
            "members.id",
            "members.status",
            "members.interests",
            "members.stats.avg_open_rate",
            "members.stats.avg_click_rate",
            "members.timestamp_opt",
            "members.tags"
        ]

        while True:
            response = client.lists.get_list_members_info(
                list_id,
                count=count,
                offset=offset,
                fields=fields,  # Only return selected fields
                status='subscribed'  # Only fetch subscribed members
            )

            fetched_members = len(response['members'])
            total_members += fetched_members
            response_list.extend(response['members'])  # Collect the members in a list

            # Print progress
            print(f"Fetched {fetched_members} members in this batch, total members fetched so far: {total_members}, current offset: {offset}")

            # Check if we've retrieved all members
            if fetched_members < count:
                break  # No more members to fetch

            offset += count  # Move to the next batch of members

        print(f"Finished fetching {total_members} members.")

        return response_list

    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return None



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