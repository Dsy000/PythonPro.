#!/bin/bash

# Check if iperf3 is installed
if ! command -v iperf3 &> /dev/null
then
    echo "iperf3 could not be found, please install it."
    exit
fi

# Parse arguments
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <protocol> <target_ip> <target_port> <duration> <rate_mbps>"
    exit 1
fi

PROTOCOL=$1
TARGET_IP=$2
TARGET_PORT=$3
DURATION=$4
RATE_MBPS=$5

# Validate protocol
if [ "$PROTOCOL" != "tcp" ] && [ "$PROTOCOL" != "udp" ]; then
    echo "Invalid protocol. Use 'tcp' or 'udp'."
    exit 1
fi

# Run iperf3 with the specified parameters
if [ "$PROTOCOL" == "tcp" ]; then
    echo "Generating TCP traffic to $TARGET_IP:$TARGET_PORT at $RATE_MBPS Mbps for $DURATION seconds."
    iperf3 -c $TARGET_IP -p $TARGET_PORT -t $DURATION -b ${RATE_MBPS}M
elif [ "$PROTOCOL" == "udp" ]; then
    echo "Generating UDP traffic to $TARGET_IP:$TARGET_PORT at $RATE_MBPS Mbps for $DURATION seconds."
    iperf3 -c $TARGET_IP -p $TARGET_PORT -t $DURATION -u -b ${RATE_MBPS}M
fi

echo "Traffic generation completed."



#note:
#chmod +x traffic_generator.sh
#./dtg.sh tcp 192.168.1.10 5001 30 100
#sudo apt-get install iperf3   # For Debian/Ubuntu
#sudo yum install iperf3       # For CentOS/RHEL
#iperf3 -s
