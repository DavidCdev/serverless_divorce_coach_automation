# ghl.py
import requests

def send_ghl_message(deadline, rule, env):
    """
    Send via GoHighLevel using appropriate template/channel
    """
    ghl_api_key = env["GOHIGHLEVEL_API_KEY"]
    url = "https://rest.gohighlevel.com/v1/messages"
    headers = {"Authorization": f"Bearer {ghl_api_key}", "Content-Type": "application/json"}
    # You would customize this per requirements and provided templates
    payload = {
        "contactId": deadline.get('contact_id'),
        "templateId": rule.template_id,
        "channel": rule.channel
        # Additional required payload fields can go here
    }
    resp = requests.post(url, json=payload, headers=headers)
    try:
        resp.raise_for_status()
        return ("success", None)
    except Exception as exc:
        return ("failure", str(exc))

