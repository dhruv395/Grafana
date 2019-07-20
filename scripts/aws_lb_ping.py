import requests
import socket
from influxdb import InfluxDBClient
from datetime import datetime

url = "http://test-10000003.us-west-2.elb.amazonaws.com/cgi-bn/ciweb.pl"

client = InfluxDBClient('influxdb-load-balancer-dns', 8086, 'username', 'pass', 'telegrafdb')
json_body = [
			    {
			        "measurement": "ping",
			        "tags": {
			            "host": socket.gethostname(),
			            "url": url
			        },
			        "time": datetime.now().isoformat(),
			        "fields": {
			            "result_code": -1,
			            "url": url
			        }
			    }
			]

try:
	if requests.get(url).status_code == 200:
		json_body[0]['fields']['result_code'] = 0
	else:
		json_body[0]['fields']['result_code'] = 1
except requests.exceptions.RequestException:
	json_body[0]['fields']['result_code'] = 1


# writing to influxdb
client.write_points(json_body)
