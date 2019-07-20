#!/bin/sh

# first. take a backup from the master machine # influxd backup -portable -database mydatabase -host <remote-node-IP>:8088 /tmp/mysnapshot
# second. restore the backup to new temporary backup # influxd restore -portable -db <databasename> -newdb <newdatabasename> <backuplocation>
# third. execute select command for fetching the data from tmp database to main database
# fouth. delete the temp database
# fifth. delete the database from drive

export master_machine="ec2-47-35-70-.us-east-2.compute.amazonaws.com:8088"

echo "fetching data from master machine"
influxd backup -portable -database telegraf_metrics -host $master_machine bkp
echo "adding data to temp database"
influxd restore -portable -db telegraf_metrics -newdb bkp bkp
echo "transferring data from temp"
influx -execute 'SELECT * INTO telegraf_metrics..:MEASUREMENT FROM /.*/ GROUP BY *' -database="bkp"
echo "removing the temp database"
influx -execute 'drop database bkp'
echo "removing the database from hdd"
rm -r bkp
