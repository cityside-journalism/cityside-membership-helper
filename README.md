## Cityside Membership Helper

## Setup:

Run the virtual enviroment: 

- $ source .venv/bin/activate

Run the app:
- $ streamlit run app.py

## Setting up Secrets
Create a `.streamlit/secrets.toml` file with the following structure:

```toml
[general]
MC_KEY = "your_mailchimp_api_key"
SERVER_PREFIX = "your_server_prefix"