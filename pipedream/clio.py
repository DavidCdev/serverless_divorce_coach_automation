# clio.py
import requests, os

def fetch_deadlines(env):
    """
    Fetch all deadlines (or relevant ones) via Clio OAuth2
    """
    access_token = env["CLIO_ACCESS_TOKEN"]
    base_url = "https://app.clio.com/api/v4"
    headers = {"Authorization": f"Bearer {access_token}"}
    # TODO: Enhance for pagination/filters as needed
    resp = requests.get(f"{base_url}/calendar_entries", headers=headers)
    resp.raise_for_status()
    return [
        {
            "id": entry["id"],
            "type": entry.get("entry_type", "Deadline"),
            "date": entry.get("start_at")[:10]  # ISO date
            # Add more fields as needed, but avoid sensitive data
        }
        for entry in resp.json().get("calendar_entries", [])
    ]

