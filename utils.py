import os
import json
from datetime import datetime

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

def store_as_json(list_data, list_name, extra_metadata=None):

    if extra_metadata and "list_id" in extra_metadata:
        print("Got extra metadata: " + extra_metadata["list_id"])
    else:
        print("No extra metadata or 'list_id' not provided.")

        
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


     # Merge optional extra metadata
    if extra_metadata:
        new_metadata.update(extra_metadata)


    data_with_metadata = {
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