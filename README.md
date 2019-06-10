# Grafana
Grafana server installation and configuration

Official URL: 	https://grafana.com/docs/installation/rpm/
https://grafana.com/docs/installation/debian/ 		->for ubuntu

Grafana is an open-source platform for data visualization, monitoring and analysis. It can be used on top of a variety of different data stores but is most commonly used together with Graphite, Influx DB, and also Elastic search and Logz.io.
Grafana is designed for analyzing and visualizing metrics such as system CPU, memory, disk and I/O utilization. Grafana does not allow full-text data querying. 	
Kibana, on the other hand, runs on top of Elastic search and is used primarily for analyzing log messages.
Function: 
•	Collect metrics
•	It uses plugins to gather data.
InfluxDB (port no. 8086)is a high-performance data store written specifically for time series data. It allows for high throughput ingest, compression and real-time querying of that same data. InfluxDB is written entirely in Go and it compiles into a single binary with no external dependencies. It provides write and query capabilities with the command line interface, the built-in HTTP API, a set of client libraries (like Go, Java, and Javascript to name a few) and with plugins for common data formats such as Telegraf, Graphite, Collectd, and OpenTSDB.
Time series data: data that collectively represents how a system/process/behavior changes over time.
How to gather Metrics: 
•	Install telegraf for collecting metrics	
•	https://portal.influxdata.com/downloads/
Telegraf is the Agent for Collecting and Reporting Metrics & Data.
•	Collect and send all kinds of data: Databases, systems, IoT sensors.


https://www.howtoforge.com/tutorial/how-to-install-tig-stack-telegraf-influxdb-and-grafana-on-ubuntu-1804/

https://www.digitalocean.com/community/tutorials/how-to-monitor-system-metrics-with-the-tick-stack-on-centos-7

'https://grafana.com/dashboards/5955'

1. Preparation
Download the Telegraf and InfluxDB rpm packages here: Influxdata Download Page 
You need to install the Telegraf package on every target and client you intend to monitor.
Download the Grafana rpm packages here: Grafana Download Page
The InfluxDB and Grafana package and services only needs to be installed on one host/server which will host the InfluxDB instance and/or the Grafana service/instance. You can install all together on the same host/server or separate hosts/servers.
The NVMesh Telegraf Plugin is only needed on the NVMesh Client machines where the NVMesh Volumes will be attached to and in use. 

2. Installation
Change into the download folder containing the rpm packages.
Install the Telegraf package: sudo yum localinstall telegraf-x.x.x.x86_64.rpm 
Install the InfluxDB package: sudo yum localinstall influxdb-x.x.x.x86_64.rpm 
Install the Grafana package: sudo yum localinstall grafana-x.x.x-x.x86_64.rpm 
Copy the nvmesh_telegraf.py file to /opt/NVMesh/
Make sure its executable chmod+x /opt/NVMesh/nvmesh_telegraf.py
https://github.com/Excelero/telegraf-plugin/blob/master/nvmesh_telegraf.py

3. Verify the services and service configuration
Check if the InfluxDB service is running: sudo systemctl status influxdb
If the service is NOT running, run/issue the following commands:
sudo systemctl daemon-reload
sudo systemctl enable influxdb
sudo systemctl start influxdb
Verify if the InfluxDB service is running now: sudo systemctl status influxdb
Check if the Telegraf service is running:sudo systemctl status telegraf
If the service is NOT running, run/issue the following commands:
sudo systemctl enable telegraf sudo systemctl start telegraf
Verify if the Telegraf service is running now: sudo systemctl status telegraf
The default installation should create a configuration file with System Stats as an input plugin and InfluxDB as an output plugin.
Double check the configuration file at /etc/telegraf/telegraf.conf for the relevant input and output settings. It should be configured with the following settings:

[agent]
interval = "1s"
precision = ""

[[outputs.influxdb]]
urls = ["http://<the IP of your InfluxDB server>:8086"]
database = "telegraf"
retention_policy = ""
write_consistency = "any"
timeout = "5s"

[[inputs.cpu]]
percpu = true
totalcpu = true
collect_cpu_time = false

[[inputs.diskio]]

[[inputs.kernel]]

[[inputs.mem]]

[[inputs.processes]]

[[inputs.system]]

[[inputs.exec]]
commands = ["/opt/NVMesh/nvmesh_telegraf.py"]
timeout = "5s"
data_format = "influx"
Restart the Telegraf service: systemctl restart telegraf
Check if the Grafana service is running: sudo systemctl status grafana-server
If the service is NOT running, run/issue the following commands:
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
Initial Grafana setup and dashboard configuration
Assuming everything is up and running you should be able to connect to and configure Grafana to show NVMesh client and target data.
Point your web browser to: http://the_Grafana_server_IP_address:3000
Login with user: admin and password: adtadmin
The next step is to point and connect Grafana to the InfluxDB data base instance. Configure the data source as shown in the picture below:
 
Click <Save & Test>
Next is to install and configure the preconfigured Dashboards and Views.
From the top left corner, navigate to Dashboards > Import and click on <Upload .json File> and select the Dashboard JSON file which can be found here: Preconfigured NVMesh Grafana Dashboards
or open the sample Grafana dashboard from URL 'https://grafana.com/dashboards/5955' and click the 'Copy the ID to Clipboard' button.
 
Select InfluxDB as the data source and click on .
Repeat the previous step with all the Dashboard JSON files.
Further information can be found here:
Grafana - http://docs.grafana.org/
InfluxDB - https://docs.influxdata.com/influxdb/v1.3/introduction/getting_started/

Influxdb Commands:
CREATE USER "sammy" WITH PASSWORD 'sammy_admin' WITH ALL PRIVILEGES
->login to influxdb
influx -username 'admin' -password '@dmin   
show databases
use telegraf
show measurements

