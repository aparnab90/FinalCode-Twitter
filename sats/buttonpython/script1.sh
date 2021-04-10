#!/bin/bash
	rm -r /home/sats/code/2
	sleep 120
	systemctl stop logstash
        process_id=`/bin/ps -ef| grep "logstash" | grep -v "grep" | awk '{print $2}'`
        echo "Killing" $process_id
        kill -9 $process_id
        echo "starting for negative tweets"
	/usr/share/logstash/bin/logstash -f /home/sats/buttonpython/logstash-neg.conf --config.reload.automatic --path.data /home/sats/code/2&

