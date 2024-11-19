import os
import json
from datetime import datetime
import requests
from urllib.parse import urlparse, parse_qs, unquote
from data.newsletters import *


def get_existing_metadata(file_path):
    """Helper function to read metadata from an existing JSON file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data.get("metadata", {})
        except Exception as e:
            print(f"Error reading metadata from {file_path}: {e}")
    return {}

def store_as_json(list_data, list_name, uid):

    # if extra_metadata and "list_id" in extra_metadata:
    #     print("Got extra metadata: " + extra_metadata["list_id"])
    # else:
    #     print("No extra metadata or 'list_id' not provided.")

        
    os.makedirs('output', exist_ok=True)
    safe_list_name = list_name.replace(" ", "_").lower()
    final_file_path = f'output/{safe_list_name}.json'
    temp_file_path = f'output/{safe_list_name}.json.tmp'
    
    # Get existing metadata (if any)
    existing_metadata = get_existing_metadata(final_file_path)
    
    # Prepare new data with updated metadata
    new_metadata = {
        "fetch_timestamp": datetime.now().isoformat(),
        "record_count": len(list_data)
    }


     

    data_with_metadata = {
        "list_id": uid,
        "metadata": new_metadata,
        "data": list_data  # Original fetched data goes here
    }
    
    # Write to a temporary file first
    try:
        with open(temp_file_path, 'w') as f:
            json.dump(data_with_metadata, f, indent=4)
        
        # Atomically replace the final file with the temporary file
        os.replace(temp_file_path, final_file_path)
        print(f"Data successfully saved to {final_file_path}")
        return True, existing_metadata, new_metadata  # Return True and metadata for comparison
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        print(f"Error saving JSON file: {e}")
        return False, existing_metadata, new_metadata  # Return False with metadata for troubleshooting
    
def extract_slug_from_url(post_url):
    """
    Extract the slug from the given URL, handling nested tracking URLs.

    Args:
        post_url (str): The full URL containing the nested tracking information.

    Returns:
        str: The extracted slug, or None if the URL is invalid or the slug cannot be found.
    """
    if post_url:
        # Parse the outer URL
        parsed_url = urlparse(post_url)
        query_params = parse_qs(parsed_url.query)
        
        # Extract and decode the nested 'url' parameter
        if 'url' in query_params:
            decoded_url = unquote(query_params['url'][0])
            # Parse the decoded URL to get the slug
            parsed_decoded_url = urlparse(decoded_url)
            slug = parsed_decoded_url.path.strip('/').split('/')[-1]
            return slug
    return None


def get_post_details(slug, list_id):
    # Extract the slug from the post URL

    #slug = extract_slug_from_url(post_url)
    #print("Slug:", slug)

    # WordPress REST API URL to get the post details by slug
    wp_api_url = ""

    if list_id == richmondside_newsletter:
        wp_api_url = f"https://richmondside.org/wp-json/wp/v2/posts?slug={slug}"
    elif list_id == berkeleyside_newsletter:
        wp_api_url =  f"https://berkeleyside.org/wp-json/wp/v2/posts?slug={slug}"
    elif list_id == oaklandside_newsletter:
        wp_api_url =  f"https://berkeleyside.org/wp-json/wp/v2/posts?slug={slug}"



 
    

    response = requests.get(wp_api_url)

    if response.status_code == 200 and response.json():
        post_data = response.json()[0]  # Assuming the slug is unique and returns one post
        return post_data.get('title', {}).get('rendered')
    else:
        #print(f"Error: {response.status_code} - {response.text}")
        return None