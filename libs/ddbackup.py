from __future__ import print_function
from datadog import initialize, api
from base64 import b64decode

import json
import urllib
import boto3
from pprint import pprint
import os
import time

ENCRYPTED = os.environ['ddKeys']
DECRYPTED = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED))['Plaintext']
datadog_keys = json.loads(DECRYPTED)

outputBucket = os.environ['JSONBackupBucket']

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    
    initialize(**datadog_keys)
    
    
    with open('/tmp/monitors_all.json', 'w') as outfile:
        json.dump(api.Monitor.get_all(), outfile)
    s3.Object(outputBucket, 'monitors/monitors_all.json').put(Body=open('/tmp/monitors_all.json', 'rb'))
    
    timeboards = api.Timeboard.get_all()
    for board in timeboards["dashes"]:
        filename = str(board["id"]) + "-" + board["title"].replace(" ", "_") + ".json"
        filename = filename.replace("/", "-")
        with open('/tmp/' + filename, 'w') as outfile:
            json.dump(api.Timeboard.get(board["id"]), outfile)
            #json.dump(board, outfile)
            outfile.close()
            s3.Object(outputBucket, 'timeboards/' + filename).put(Body=open('/tmp/' + filename, 'rb'))
    
    
    screenboards = api.Screenboard.get_all()
    for board in screenboards["screenboards"]:
        filename = str(board["id"]) + "-" + board["title"].replace(" ", "_") + ".json"
        filename = filename.replace("/", "-")
        with open('/tmp/' + filename, 'w') as outfile:
            json.dump(api.Screenboard.get(board["id"]), outfile)
            #json.dump(board, outfile)
            outfile.close()
            s3.Object(outputBucket, 'screenboards/' + filename).put(Body=open('/tmp/' + filename, 'rb'))
    