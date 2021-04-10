#!/bin/bash
for i in {1..20} 
do
	process_id=`/bin/ps -ef| grep "logstash" | grep -v "grep" | awk '{print $2}'`
	systemctl stop logstash
	echo "Killing" $process_id
	kill -9 $process_id
	rm -r /home/sats/code/1
	echo "starting logstash"
	/usr/share/logstash/bin/logstash -f /home/sats/buttonpython/logstash-pos.conf --config.reload.automatic --path.data /home/sats/code/1&
	./script1.sh
	./script4.sh
        echo "Sleeping for 5 mins"
	sleep 400
done
