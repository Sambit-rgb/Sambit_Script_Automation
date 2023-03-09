import requests
import json
import os
import subprocess
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import gspread
import google.auth
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import time
import json, datetime
from google.cloud import storage
from googleapiclient._auth import default_credentials






version = input("Enter the yugabte image version: ")
    # '2.14.1.0-b36'
# version = '2.14.2.0-b25'

# Scanning
os.system('docker login quay.io')
os.system('docker pull quay.io/yugabyte/yugabyte:'+version)
id = 'docker images --filter=reference=quay.io/yugabyte/yugabyte:'+version+' --format "{{.ID}}"'
image_id = str(subprocess.check_output(id, shell=True))[2:][:-3]
os.system('docker login ybdb.jfrog.io')
os.system('docker tag '+ image_id + ' ybdb.jfrog.io/ybanywhere-docker-local/yugabyte:'+ version)
os.system('docker push ybdb.jfrog.io/ybanywhere-docker-local/yugabyte:'+version)
# time.sleep(500)
os.system('echo "y" | docker system prune -a')

def api():
    # enter credentials
    username = "smohanty@yugabyte.com"
    password = "cmVmdGtuOjAxOjAwMDAwMDAwMDA6YXQ4aEtLcG1JUjU3bzVITmhybHQ2Zm1xbU1J "
    a = 'curl -u '

    b = a + username + ':' + password + 'https://ybdb.jfrog.io/artifactory/ybanywhere-docker-local/yugabyte/' + version + '/manifest.json.sha256'
    c = str(subprocess.check_output(b, shell=True))[2:][:-1]

    data = {

        "checksums": [

            c

        ]

    }

    # Serializing json
    json_object = json.dumps(data, indent=1)
    # curl -u smohanty@yugabyte.com:Blackduck@1989 https://ybdb.jfrog.io/artifactory/ybanywhere-docker-local/yugabyte/2.14.1.0-b36/manifest.json.sha256

    # Writing to sample.json
    with open("artifact-digest.json", "w") as outfile:
        outfile.write(json_object)

    t = "'https://ybdb.jfrog.io/xray/api/v1/summary/artifact'"
    artifactory = ' -X POST -H "Content-type: application/json" ' + t + ' -d @artifact-digest.json | python -m json.tool >' + version + '.json'  # artifactory URL
    # api = #you can change this API URL to any API method you'd like to use


    url = a + username + ':' + password + artifactory
    # os.system(url)
    subprocess.check_output(url, shell=True)


api()
e = 'cat ' + version + '.json | grep "\\"severity\\": \\"High\\"" | wc -l'
e1 = 'cat ' + version + '.json | grep "\\"severity\\": \\"Low\\"" | wc -l'
e2 = 'cat ' + version + '.json | grep "\\"severity\\": \\"Medium\\"" | wc -l'

tr = str(subprocess.check_output(e, shell=True))[2:][:-3]
tr1 = str(subprocess.check_output(e2, shell=True))[2:][:-3]
tr2 = str(subprocess.check_output(e1, shell=True))[2:][:-3]
print('Number of High issue for image '+version+' is'+tr + ' and Medium issue is'+tr1+' and Low issue is'+tr2)

# print('Number of Medium issue for image '+version+tr1)
# print('Number of Low issue for image '+version+tr2)

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

upload_file_list = [version+'.json']
for upload_file in upload_file_list:
	gfile = drive.CreateFile({'parents': [{'id': '1EldmXdu05o6ZvJNIMQlxV02jthlp-AOC'}]})
	gfile.SetContentFile(upload_file)
	gfile.Upload()


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']



    # add credentials to the account
# creds = ServiceAccountCredentials.from_json_keyfile_name('jfrog-automation-366006-a2d713d36cb6.json', scope)

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='jfrog-automation-366006-a2d713d36cb6.json'
gc = gspread.auth.service_account()

    # authorize the clientsheet
# client = gspread.authorize(creds)

    # get the instance of the Spreadsheet give editor access to the sheet by share sambit@sambit-gcpproject.iam.gserviceaccount.com
    # mv jfrog-automation-366006-a2d713d36cb6.json service_account.json
    #/Users/sambitmohanty/.config/gspread
sheet = gc.open('Jfrog_Issue_Data')
sheet_instance = sheet.get_worksheet(0)
start = 2
    # Retrieve all rows
def get_var_value(filename="v.dat"):
    with open(filename, "a+") as f:
        f.seek(0)
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val

your_counter = get_var_value()
date = str(datetime.datetime.now())
dt = (json.dumps(date))[1:][:-16]
sheet_instance.update_acell('A'+str(your_counter), version)
sheet_instance.update_acell('B'+str(your_counter), tr)
sheet_instance.update_acell('C'+str(your_counter), tr1)
sheet_instance.update_acell('D'+str(your_counter), tr2)
sheet_instance.update_acell('E'+str(your_counter), dt)