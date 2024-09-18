import requests
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import xml.etree.ElementTree as ET
DATAVERSE_API_VERSION = "v9.2"


def get_fetchxml_results(query, org_url):
    """Run the FetchXML query in Dataverse."""
    token = get_access_token(org_url)
    if token:
        result = run_fetchxml_query(query, org_url, token)
        if result:
            return result
    else:
        print("Error getting access token.")
    return None


def get_odata_results(query, org_url):
    """Run the OData query in Dataverse."""
    token = get_access_token(org_url)
    if token:
        result = run_odata_query(query, org_url, token)
        if result:
            return result
    else:
        print("Error getting access token.")
    return None


def extract_entity_name(fetch_xml):
    root = ET.fromstring(fetch_xml)
    entity = root.find('entity')
    if entity is not None:
        return entity.get('name')
    return None


def get_access_token(org_url):
    """Get an access token for Dataverse using DefaultAzureCredential."""
    # Create a credential object using DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Define the resource scope for Dataverse
    token_provider = get_bearer_token_provider(
        credential, f"{org_url}/.default"
    )

    # Retrieve the token
    token = token_provider()
    return token


def run_fetchxml_query(query, org_url, token):
    
    table_name = extract_entity_name(query)
    if table_name[-1] == 's':
        table_name = table_name+'es'
    else:
        table_name = table_name+'s'
    # Encode FetchXML query as part of the URL
    fetchxml_encoded = requests.utils.quote(query)
    odata_query = f"{table_name}?fetchXml={fetchxml_encoded}"
    return run_odata_query(odata_query, org_url, token)


def run_odata_query(query, org_url, token):
    """Run the OData query in Dataverse."""
    headers = {
        "Authorization": f"Bearer {token}",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    url = f"{org_url}/api/data/{DATAVERSE_API_VERSION}/{query}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json(), True
    else:
        return f"Error running query: {response.status_code} - {response.text}", False


if __name__ == "__main__":
    pass
