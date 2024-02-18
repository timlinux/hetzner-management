#!/usr/bin/env python
import os
from hcloud import Client

# Retrieve the API token from an environment variable
api_token = os.environ.get("HETZNER_API_TOKEN")

if not api_token:
    print("Please set the HETZNER_API_TOKEN environment variable.")
    exit(1)

# Initialize the client with the API token
client = Client(token=api_token)

# List all servers in your Hetzner Cloud group
servers = client.servers.get_all()
for server in servers:
    print(f"Server ID: {server.id}, Name: {server.name}, Status: {server.status}")

