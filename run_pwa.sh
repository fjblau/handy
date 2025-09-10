#!/bin/bash

# Make the script executable
chmod +x "$0"

# Run the Streamlit app with mobile-friendly settings
echo "Starting Handy Mobile App..."
streamlit run handy.py --server.enableCORS=false --server.enableXsrfProtection=false