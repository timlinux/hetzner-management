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

def check_file_on_server():
    # Set the path to the file you want to check
    remote_file_path = '/path/to/your/file.txt'

    # Get the user's home directory
    user_home = os.path.expanduser("~")

    # Set the path to the private key (assuming default location)
    private_key_path = os.path.join(user_home, '.ssh', 'id_ed25519')

    # Create an SSH client
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Set your server details
    servers = get_servers()
    if not len(servers):
       print(f"No more servers left to check!")

    for server in servers:
        print(f"Server ID: {server.id}, IP: {server.public_net.ipv4.ip}, Name: {server.name}, Status: {server.status}")
        try:
            # Load the private key
            private_key = paramiko.Ed25519Key(filename=private_key_path)

            # Connect to the server using the private key
            client.connect(server.public_net.ipv4.ip, username="root", pkey=private_key)
            while True:
                # Check if the file exists
                stdin, stdout, stderr = client.exec_command(f'test -e {remote_file_path}')
                if stdout.read().strip() == b'':
                    print(f"File '{remote_file_path}' not found. Waiting for 5 minutes...")
                else:
                    print(f"File '{remote_file_path}' found!.")
                    servers.remove(server)
                break
        except paramiko.AuthenticationException:
            print("Authentication failed. Please check your credentials.")
        except paramiko.SSHException as e:
            print(f"SSH error: {e}")
        finally:
            client.close()
        time.sleep(300)  # Wait for 5 minutes


if __name__ == "__main__":
    check_file_on_server()
