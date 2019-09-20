#!/bin/sh

#method 1
'''
export master_machine="20.129.1.2:8088"
echo "fetching data from master machine"
influxd backup -portable -database telegraf_metrics -host $master_machine bkp
echo "adding data to temp database"
influxd restore -portable -db telegraf_metrics -newdb bkp bkp
echo "transferring data from temp"
influx -execute -username 'admin' -password 'yourpassword' 'SELECT * INTO telegraf_metrics..:MEASUREMENT FROM /.*/ GROUP BY *' -database="bkp"
echo "removing the temp database"
influx -execute 'drop database bkp'
echo "removing the database from hdd"
rm -r bkp
'''

#method 2

'''
1.  Download the backup from storage
2. untar the backup and run the below command 
influxd restore -portable -db telegraf_metrics telegraf_metrics
3. Run the influx shell and run 'use bkp'
4. run command to transfer data from bkp to telegraf_metrics
SELECT * INTO telegraf_metrics..:MEASUREMENT FROM /.*/ GROUP BY *
5. drop database bkp
'''
