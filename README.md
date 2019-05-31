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
