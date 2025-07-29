import requests

# Create session at module level
session = requests.Session()

def get_session():
    return session

def configure_session(**kwargs):
    """Configure session with headers, auth, etc."""
    for key, value in kwargs.items():
        setattr(session, key, value)
    return session