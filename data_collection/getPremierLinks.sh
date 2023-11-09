#!/bin/bash

# Run your Python script in the background
python getPremierLinks.py &

# Get the PID of the last background process (your Python script)
PID=$!

# Wait for user input to send the custom signal
read -p "Press Enter to stop the script..."

# Send the SIGUSR1 signal to your Python script
kill -SIGUSR1 $PID

# Wait for the script to finish gracefully
wait $PID

echo "Script has finished gracefully."