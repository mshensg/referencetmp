import boto3
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
access_key= ‘aaa’
secret_key= 'kkk’
 
b3_session = boto3.Session(aws_access_key_id=access_key,
                           aws_secret_access_key=secret_key,
                           region_name='us-east-1')
 
region='us-east-1'
#region='ap-southeast-1'
 
bucket_name='bbb'
 
b3_client = b3_session.client('s3', endpoint_url='https://s3.{}.amazonaws.com'.format(region),verify=False)
 
response = b3_client.list_buckets()
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
b3_resource = b3_session.resource('s3', endpoint_url='https://s3.{}.amazonaws.com'.format(region),verify=False)
b3_bucket = b3_resource.Bucket(bucket_name)
all_objects = [{"bucket_name":i.bucket_name,
  "key":i.key,
  "last_modified":i.last_modified,
  "isotime":i.last_modified.isoformat(),
  "timestamp":i.last_modified.timestamp(),
  "size":i.size,
  "storage_class":i.storage_class,
  "owner":i.owner["DisplayName"],
  "ETag":i.meta.data["ETag"]} for i in b3_bucket.objects.all()]
print("Existing objects:")
print(f'  {len(all_objects)} objects in system')
 
all_objects.sort(key=lambda x: x["timestamp"], reverse=False)
 
buckettsidx=[{
    **i,
    **{
        "index":i["key"].split("/")[1],
        "bucketNo":int(i["key"].split("/")[5].split("~")[0]),
        "server":i["key"].split("/")[5].split("~")[1],
        "startEpoch":int(i["key"].split("/")[-1].split("-")[0]),
        "endEpoch":int(i["key"].split("/")[-1].split("-")[1])
        }
    } for i in all_objects if i["key"][-6:] == ".tsidx"]
 
