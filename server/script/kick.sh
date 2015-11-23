#!/bin/bash
DAEMON="/usr/introbank/introbank-backend/server/daemon/twitter_data_streaming_daemon.py"
source /opt/rh/python27/enable;
nohup python $DAEMON 1 debug > /var/log/introbank/streaming.log &
