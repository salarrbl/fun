#!/bin/bash


now=`date +%s`sec
while true; do
	printf "%s\r" $(TZ=UTC date --date now-$now +%H:%M:%S.%N) 
	sleep 0.1 
	if read -t 0.1 -n 1 input; then
			if [[ $input == "q" ]]; then
				break
			fi
	fi
done


