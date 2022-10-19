


###################################
### USER MODIFIABLE PARAMETERS ####
###################################



BASE_API_ENDPOINT   = "https://ENDPOINT_ID.execute-api.LOCATION.amazonaws.com/PATH"
ACCESS_KEY_ID       = "XXXXXXXXXXXXXXX"
ACCESS_KEY_SECRET   = "XXXXXXXXXXXXXXX"

parameters['single']['database_id']         = None
parameters['single']['device_type']         = None
parameters['multi']['device_ids']          = [None]
parameters['multi']['measurements']        = [None]
parameters['multi']['bounds_low']          = [None]
parameters['multi']['bounds_high']         = [None]
parameters['multi']['times']               = [None]
parameters['multi']['groupings']           = [None]
parameters['multi']['aggregators']         = [None]
parameters['single']['aggregators_only']    = None
parameters['single']['time_zone']           = None




###################################
#### FOR RECOVERING PARAMETERS ####
###################################



# BASE_API_ENDPOINT   = "https://ENDPOINT_ID.execute-api.LOCATION.amazonaws.com/PATH"
# ACCESS_KEY_ID       = "XXXXXXXXXXXXXXX"
# ACCESS_KEY_SECRET   = "XXXXXXXXXXXXXXX"

# parameters['single']['database_id']         = None
# parameters['single']['device_type']         = None
# parameters['multi']['device_ids']          = [None]
# parameters['multi']['measurements']        = [None]
# parameters['multi']['bounds_low']          = [None]
# parameters['multi']['bounds_high']         = [None]
# parameters['multi']['times']               = [None]
# parameters['multi']['groupings']           = [None]
# parameters['multi']['aggregators']         = [None]
# parameters['single']['aggregators_only']    = None
# parameters['single']['time_zone']           = None



##################################
########## CODE SECTION ##########
#### MODIFY AT YOUR OWN RISK! ####
##################################



import boto3    # AWS CLI library 
from aws_requests_auth.aws_auth import AWSRequestsAuth  # Perform authentication credential verification
import requests # Perform GET/POST requests 
import datetime # Get current time
import json # Parse and format output
import os   # Create folder for organization

######

full_url = BASE_API_ENDPOINT + "?"

for param in parameters['single']:
    full_url += "{}={}&".format(param, parameters['single'][param]) if parameters['single'][param] != None else ""
for param in parameters['multi']:
    for value in parameters['multi'][param]:
        full_url += "{}={}&".format(param, value)  if parameters['multi'][param] != [None] else ""

print(full_url)

######

print("Fetching AWS authentication... ")

asdf = AWSRequestsAuth(aws_access_key=ACCESS_KEY_ID,
                           aws_secret_access_key=ACCESS_KEY_SECRET,
                           aws_host=next(x for x in BASE_API_ENDPOINT.split("/") if "." in x),
                           aws_region='us-east-1',
                           aws_service='execute-api')

######  Performing API request 
print("Performing API request... ")

results = (requests.get( full_url , auth=asdf).content)

print("API request complete! ")

######  Parsing results 

try:
    result_set = json.loads(results)
except:
    print("Error with API return!")
    print(results)
    exit()

######  Result exporting 

try: os.mkdir("output", exist_ok=True) 
except: pass

try:
    filename = "output/results_" + str(datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")) + ".json"
    with open(filename, 'w') as writer:
        json.dump(result_set, writer, indent=2)
        print("Output results at: " + filename)

except Exception as e:
    print("Error with result saving!")
    print(str(e))
