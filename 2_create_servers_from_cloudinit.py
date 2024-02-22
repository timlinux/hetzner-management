#!/usr/bin/env python

import os
import sys
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType


def main():
    if len(sys.argv) != 3:
        print("Usage: python 2_create_servers_from_cloudinit.py <number> <type>")
        sys.exit(1)

    try:
        number = int(sys.argv[1])
        print(f"Creating {number} server(s)")
    except ValueError:
        print("Error: Please provide a valid numeric argument.")

    try:
        server_type = str(sys.argv[2])
        print(f"Creating {server_type} server(s)")
    except ValueError:
        print("Error: Please provide a valid server type.")        

    # Retrieve the API token from an environment variable
    api_token = os.environ.get("HETZNER_API_TOKEN")

    if not api_token:
        print("Please set the HETZNER_API_TOKEN environment variable.")
        exit(1)

    print("Current servers:")
    client = Client(token=api_token)
    servers = client.servers.get_all()
    for server in servers:
        print(f"Server ID: {server.id}, Name: {server.name}, Status: {server.status}")

    cloud_init = """
runcmd:
  - curl https://raw.githubusercontent.com/elitak/nixos-infect/master/nixos-infect | PROVIDER=hetznercloud NIX_CHANNEL=nixos-22.11 bash 2>&1 | tee /tmp/infect.log
    """

    for server_number in range(number): 
      server_name = (f"nix-{server_number}")
      # Create a server named "my-server" from a snapshot
      response = client.servers.create(
          name=server_name,
          #server_type=ServerType(name="cx11"),  # Choose an appropriate server type
          server_type=ServerType(name=server_type),  # Choose an appropriate server type
          image=Image(name="ubuntu-22.04"),
          user_data=cloud_init,
          
      )
    # List all your servers
    servers = client.servers.get_all()
    for server in servers:
        print(f"Server ID: {server.id}, Name: {server.name}, Status: {server.status}")

if __name__ == "__main__":
    main()

