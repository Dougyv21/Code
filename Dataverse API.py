import requests
import pandas as pd
from msal import ConfidentialClientApplication

# create a pandas dataframe and send it to output 1
resource = 'https://org7631b14c.crm.dynamics.com'
client_id = '98604c61-3a09-4a83-8c19-56049dd87929'
client_secret = '0Q-8Q~1Sram1RCRYwcO8BONmXtuokZNpvt5Erbtn'
tenant_id = '1e3e71be-fcca-4284-9031-688cc8f37b6b'

# Create a ConfidentialClientApplication instance
app = ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=f'https://login.microsoftonline.com/{tenant_id}'
)

# Acquire a token using the service principal credentials
result = app.acquire_token_for_client(scopes=[resource + '/.default'])

if "access_token" in result:
    access_token = result['access_token']
    
    # Make a request to retrieve data from a specific table (replace 'table_name' with your actual table name)
   #Make sure you use your plural table name.  EX: cr34c_aod will NOT Work, but cr34c_aods will work
    table_name = 'cr34c_aods'
    url = f'{resource}/api/data/v9.1/{table_name}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(data['value'])
        
        # Process the DataFrame as needed