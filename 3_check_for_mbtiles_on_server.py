#!/usr/bin/env python

import os
import time
import paramiko
from hcloud import Client

def get_servers():
    # Retrieve the API token from an environment variable
    api_token = os.environ.get("HETZNER_API_TOKEN")

    if not api_token:
        print("Please set the HETZNER_API_TOKEN environment variable.")
        exit(1)

    # Initialize the client with the API token
    client = Client(token=api_token)

    # List all servers in your Hetzner Cloud group
    servers = client.servers.get_all()
    return servers

def check_file_presence(hostname, username, private_key_path, remote_file_path):
    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Load the private key from the agent
        agent = paramiko.Agent()
        keys = agent.get_keys()
        if not keys:
            print("No private keys found in the agent.")
            return

        # Connect to the server
        client.connect(hostname, username=username, pkey=keys[0])

        while True:
            # Check if the file exists
            stdin, stdout, stderr = client.exec_command(f"ls {remote_file_path}")
            exit_status = stdout.channel.recv_exit_status()

            if exit_status == 0:
                print(f"File '{remote_file_path}' found. Exiting.")
                return True
            else:
                print(f"File '{remote_file_path}' not found. Retrying in 5 minutes...")
                return False
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your private key and credentials.")
        return False
    except paramiko.SSHException as e:
        print(f"SSH error: {e}")
        return False
    finally:
        client.close()

def check_servers():
    username = "root"
    remote_file_path = "/path/to/remote/file.txt"
    # Get the user's home directory
    user_home = os.path.expanduser("~")
    private_key_path = os.path.join(user_home, '.ssh', 'id_ed25519')
    servers = get_servers()
    while len(servers):
        for server in servers:
            print(f"Server ID: {server.id}, IP: {server.public_net.ipv4.ip}, Name: {server.name}, Status: {server.status}")
            try:
                if check_file_presence(hostname, username, private_key_path, remote_file_path):
                    servers.remove(server)
            except:
                print(f"File not found!")
        time.sleep(300)  # Wait for 5 minutes
    print(f"No more servers left to check!")

if __name__ == "__main__":
    check_servers()
