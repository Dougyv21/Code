# import packages and functions #
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.work_item_tracking.models import Wiql

import requests
import pandas

# define our personal access token #
PAT = ''

# creating our authentication object
Auth = requests.auth.HTTPBasicAuth('', PAT)

# Set up authentication
Org = 'rsmdevops'
Proj = 'Audit Innovation Automation'

# Fill in with your personal access token and organization URL
OrganizationURL = 'https://dev.azure.com/rsmdevops'

# Create a connection to the Azure DevOps organization
Credentials = BasicAuthentication('', PAT)
MyConnection = Connection(base_url = OrganizationURL, creds = Credentials)

# Get a client to interact with the work item tracking API
wit_client = MyConnection.clients.get_work_item_tracking_client()

# Define a WIQL query to get the title, description, state, and assigned-to user of all work items of a specific project
wiql_query = Wiql(query="SELECT [System.Id], [System.Title], [System.Description], [System.State], [System.AssignedTo] FROM workitems WHERE [System.TeamProject] = 'Audit Innovation Automation'")

# Execute the WIQL query and get the work items
WorkItems = wit_client.query_by_wiql(wiql_query).work_items

# Loop through each work item and print its details
WorkItemIds = [WI.id for WI in WorkItems]

# Build the API URL
WorkItemsURL = f'https://dev.azure.com/{Org}/{Proj}/_apis/wit/workitems?api-version=6.0'

# Initialize list attributes #
S = 0
I = 150
WIIDs = []

# Creating sub list because devops doesn't allow to pull more than 200 work items at once #
while S < len(WorkItemIds):
    WIID = WorkItemIds[S:S+I]
    WIIDs.append(WIID)
    S += I

# Initialize DF outside loop to ensure we can append to it during all iterations of each list of work ids #
WorkItemsDF = pandas.DataFrame()

# Print sublists
for WIID in WIIDs:
    
    # create a dictionary for params, creating a string from our work item list
    Params = {'ids': ','.join([str(id) for id in WIID]), '$expand': 'all'}    
    
    # Main Call
    WorkItemsResponse = requests.get(url = WorkItemsURL, auth = Auth, params = Params)
    
    # Using json method of response object to get our data
    WorkItems = WorkItemsResponse.json()
    
    # Drill down into actual values
    WorkItems = WorkItems['value']
    
    # Loop through work items #
    for WI in WorkItems:
    
        # pull the fields as a variable
        WIFields = WI['fields']
        
        # create a dataframe with one column (index = 0) and using System.Title as our value #
        DF = pandas.DataFrame(data = {'WorkItemTitle': WIFields['System.Title']}, index = [0])
        
        # Pull fields if they exist #
        try:
        
            # System fields #
            DF['ID'] = WIFields['System.Id']
            DF['WorkItemType'] = WIFields['System.WorkItemType']
            DF['AssignedTo'] = str(WIFields['System.AssignedTo'])
            DF['WorkItemState'] = WIFields['System.State']
            DF['State'] = WIFields['System.State']
            DF['Tags'] = WIFields['System.Tags']
            DF['Description'] = WIFields['System.Reason']
            DF['CreatedBy'] = WIFields['System.CreatedBy']
            DF['CreatedDate'] = WIFields['System.CreatedDate']
            
            # Microsoft VSTS Fields #
            DF['AcceptanceCriteria'] = WIFields['Microsoft.VSTS.Common.AcceptanceCriteria']
            DF['AcceptedDate'] = WIFields['Microsoft.VSTS.CodeReview.AcceptedDate']
            DF['ActivatedDate'] = WIFields['Microsoft.VSTS.Common.ActivatedDate']
            DF['ClosedBy'] = WIFields['Microsoft.VSTS.Common.ClosedBy']
            DF['StartDate'] = WIFields['Microsoft.VSTS.Scheduling.StartDate']
            DF['TargetDate'] = WIFields['Microsoft.VSTS.Scheduling.TargetDate']
            DF['Issue'] = WIFields['Microsoft.VSTS.Common.Issue']
            
            # Custom Fields #
            DF['Completed'] = WIFields['Custom.Completed']
        
        # Dealing with fields that doesn't always exist - Pull field name from the error and assign it as null #
        except KeyError as Field:
            Field = str(Field).rsplit('.', 1)[-1]
            DF[Field] = None
        
        # All outputs #
        WorkItemsDF = pandas.concat([WorkItemsDF, DF], ignore_index = True)
