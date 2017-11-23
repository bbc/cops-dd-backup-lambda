Datadog Lambda backup script
============================
Simple script to copy Datadog dashboards, screenboards and monitors to S3 in JSON format via the Datadog API on a scheduled basis.

The stack creates ScheduledRule in CloudFront for MON-FRI 17:30. It requires an existing S3 bucket to output JSON files so ensure appropriate versioning/archival happens there.

Deployment
----------

The Cloudformation stack is defined in dd_stack.json. This takes the following parameters:

Parameter|Notes
:---|:---
DatadogKey|NB- leave this blank and fill in via the secure method after the Lambda function is setup as detailed below  
JSONBackupBucket|Existing S3 bucket to output JSON files to
LambdaFilename|eg. dd-backup.zip  
LambdaFunctionTimeout|Default is 300 seconds which is the maximum. Expect at least 4mins to process at current metric levels.
LambdaMainHandler|Default is in main.py eg. ddbackup.lambda_handler  
SourceBucket|S3 bucket containing the ZIP gile eg: datadog-backup-test

Tweak the script libs/ddbackup.py if required and zip all files in the libs/ directory to make the zipfile specified as LambdaFilenam.

The ddbackup.py script expects JSONBackupBucket and a KMS-encrypted Datadog API JSON key ddKeys as environment variables. 

Secure API/APP Key configuration
--------------------------------
Get valid Datadog API and application keys from the Datadog site under Integrations/API/Application Keys and in the AWS console Lambda Code section for your Function check "Enable encryption helpers" and select the KMS key to encrypt in transit/at rest.

Enter the Datadog API/Application keys in JSON format as follows:
```json
{"api_key":"abcd1234567889etc...", "app_key":"abcd1234567889etc..."}
```

JSON output
-----------
A successful run will produce the following output in the JSONBackupBucket:

  monitors/monitors_all.json

  screenboards/(individual screenboard JSON files in $ID_$TITLE.json format)

  timeboards/(individual timeboard JSON files in $ID_$TITLE.json format)

