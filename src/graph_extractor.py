import configparser
import requests
import msal
import os

def load_config():
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    return config

def get_graph_token(config):
    tenant_id = config.get("azure", "tenant_id", fallback=None)
    client_id = config.get("azure", "client_id", fallback=None)
    client_secret = config.get("azure", "client_secret", fallback=None)

    if not tenant_id or "YOUR_" in tenant_id:
        return None  # Fallback to local offline mode if credentials are not yet entered

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id, authority=authority, client_credential=client_secret
    )

    scopes = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"[AUTH WARNING] {result.get('error_description')}")
        return None

def fetch_po_sent_timestamp(po_number, access_token, buyer_email="buyer@kohinoorpune.com"):
    """Queries Microsoft Graph API for exact PO sent timestamp."""
    if not access_token:
        return None

    headers = {"Authorization": f"Bearer {access_token}"}
    # Strictly scoped query to target SentItems folder for specific PO subject
    query_url = (
        f"https://graph.microsoft.com/v1.0/users/{buyer_email}/mailFolders/SentItems/messages"
        f"?$search=\"{po_number}\""
        f"&$select=subject,sentDateTime"
    )

    try:
        response = requests.get(query_url, headers=headers, timeout=5)
        if response.status_code == 200:
            messages = response.json().get("value", [])
            if messages:
                return messages[0].get("sentDateTime")
    except Exception as e:
        print(f"[API ERROR] Failed to query PO {po_number}: {e}")

    return None