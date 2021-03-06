# This script writes the metadata for the selected action task to
# actionTask.json based on the taskID you select when running the script.

# This script assumes you know your workspaceGuid, modelGuid, and action ID.
# If you do not have this information, please run 'getWorkspaces.py',
# 'getModels.py', and 'getActions.py' and retrieve this information from the
# resulting json files.

# If you are using certificate authentication, this script assumes you have
# converted your Anaplan certificate to PEM format, and that you know the
# Anaplan account email associated with that certificate.

# This script uses Python 3 and assumes that you have the following modules
# installed: requests, base64, json

import requests
import base64
import json

# Insert your workspace Guid
wGuid = ''
# Insert your model Guid
mGuid = ''
# Insert your action ID
actionID = ''
# Insert the Anaplan account email being used
username = ''

# If using cert auth, replace cert.pem with your pem converted certificate
# filename. Otherwise, remove this line.
cert = open('cert.pem').read()

# If using basic auth, insert your password. Otherwise, remove this line.
password = ''

# Uncomment your authentication method (cert or basic). Remove the other.
user = 'AnaplanCertificate ' + str(base64.b64encode((
       f'{username}:{cert}').encode('utf-8')).decode('utf-8'))

# user = 'Basic ' + str(base64.b64encode((f'{username}:{password}'
#                                         ).encode('utf-8')).decode('utf-8'))

url = (f'https://api.anaplan.com/1/3/workspaces/{wGuid}/models/{mGuid}/' +
       f'actions/{actionID}/tasks')

getHeaders = {
    'Authorization': user
}

# Gets all taskIDs associated with the action, and asks which the user wants to
# view the status of
getActionTasks = requests.get(url,
                              headers=getHeaders)

with open('actionTasks.json', 'wb') as f:
    f.write(getActionTasks.text.encode('utf-8'))

with open('actionTasks.json', 'r') as f:
    f2 = json.load(f)

count = 0
for i in f2:
    print(f'This task is at index {count}')
    print(i)
    print('\n')
    count += 1

x = f2[int(input('Enter the index for the task you would like to view: '))]
i = x['taskId']
print(i)
# Gets and prints the status of the selected task
actionStatus = requests.get(url + f'/{i}',
                          headers=getHeaders)

with open('actionStatus.json', 'wb') as f:
    f.write(actionStatus.text.encode('utf-8'))

# Loads the status file, and reports status as well as writing any failure
# dump to a csv
with open('actionStatus.json', 'r') as f:
    f2 = json.load(f)
    
if f2['taskState'] != 'COMPLETED':
    print('In progress. See "actionStatus.json"')
    print('Progress: ' + str(f2['progress']))
    print('Task Status: ' + f2['taskState'])
else:
    print('Task Status: ' + f2['taskState'])

