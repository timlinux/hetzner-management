#!/usr/bin/env python
import os
from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType

def main():
    # Retrieve the API token from an environment variable
    api_token = os.environ.get("HETZNER_API_TOKEN")

    if not api_token:
        print("Please set the HETZNER_API_TOKEN environment variable.")
        exit(1)

    print("Current servers:")
    client = Client(token=api_token)
    servers = client.servers.get_all()

    # Iterate through servers and delete those with names starting with 'nix'
    for server in servers:
        if server.name.startswith("nix"):
            print(f"Deleting server: {server.name} (ID: {server.id})")
            server.delete()

    print("Deletion completed for servers with names starting with 'nix'.")
    servers = client.servers.get_all()
    for server in servers:
        print(f"Server ID: {server.id}, Name: {server.name}, Status: {server.status}")


if __name__ == "__main__":
    main()



