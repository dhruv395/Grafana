# fetch dashboard json and upload to s3
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from datetime import datetime
import requests
import json

# grafana api settings
api_key= "API-KEY"
base_url = "http://grafana-********.us-west-2.elb.amazonaws.com:3000"
# grafana settings end


# s3 settings
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY need read and write access of s3
bucket_name = "BUCKETNAME"
AWS_ACCESS_KEY_ID = 'KEY'
AWS_SECRET_ACCESS_KEY = 'SECRET'
#s3 settings end


headers = {"Authorization":"Bearer %s"%(api_key),
		   "Accept":"application/json",
		   "Content-Type":"application/json"
		   }


# fetching the the dashboard ids
def fetch_list_of_dashboards():
	url = base_url + "/api/search"
	return json.loads(requests.get(url,headers=headers).text)

# fetching the dashboard json from uid
def fetch_dashboard_json(uid):
	url = base_url + "/api/dashboards/uid/%s"%(uid)
	return json.dumps(requests.get(url,headers=headers).json()['dashboard'])


# fetch dashborad and upload to s3
def fetch_dashboard_and_upload_to_s3():
	for dashboard in fetch_list_of_dashboards():
		filename = dashboard['title'].replace(" ","-") + ".json"
		file_content = fetch_dashboard_json(dashboard['uid'])
		folder_location = "/grafana_dashboards/" + datetime.now().date().isoformat() + "/"
		conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
		bucket_conn_obj = conn.get_bucket(bucket_name)
		k = Key(bucket_conn_obj)
		k.key = folder_location + filename
		k.set_contents_from_string(file_content)
		conn.close()
		# printing log
		print dashboard['title'] + " - Done"


if __name__ == '__main__':
    fetch_dashboard_and_upload_to_s3()
