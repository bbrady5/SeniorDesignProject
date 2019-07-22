'''
Created on Jul 20, 2019

@author: BB070512
'''


import requests
import json

url = "https://api.meraki.com/api/v0/devices/Q2PD-6WK9-V4XS/clients"

querystring = {"timespan":"86400"}

headers = {
    'X-Cisco-Meraki-API-Key': "b70ca858020930863c1542f511ec4267ab077aa6",
    'User-Agent': "PostmanRuntime/7.15.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "338b5785-52d9-412e-9db4-ea90361e0e69,441570a6-a644-42cb-8446-9244f803d755",
    'accept-encoding': "gzip, deflate",
    'referer': "https://api.meraki.com/api/v0/devices/Q2PD-6WK9-V4XS/clients?timespan=86400",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)


json_data = json.loads(response.text)

for item in json_data:
    desc = item.get("description")
    print(desc)


#result = json.loads(response)  # result is now a dict
#print ('"description":', result['description'])

