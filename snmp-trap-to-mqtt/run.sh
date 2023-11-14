#!/usr/bin/with-contenv bashio

# Print the files in the directory
ls -l /

echo "Starting snmp-trap-to-mqtt"

# Run the main script
python3 /main.py
