## Cityside Membership Helper

## Setup:

### Setting up Secrets
Create a `.streamlit/secrets.toml` file with the following structure:

```toml
[general]
MC_KEY = "your_mailchimp_api_key"
SERVER_PREFIX = "your_server_prefix"
```

## Run the virtual enviroment: 

```bash
 $ source .venv/bin/activate
```
Run the app:

```bash
 $ streamlit run app.py
```
