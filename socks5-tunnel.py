import paramiko
import threading
import socket
import socks
import sys

def create_ssh_tunnel(username, password, remote_host, remote_port, local_port):
    try:
        # Create an SSH client instance
        ssh_client = paramiko.SSHClient()

        # Automatically add the remote host key (this is not secure in production, handle with care)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Establish SSH connection to the remote server
        ssh_client.connect(remote_host, port=remote_port, username=username, password=password)

        # Retrieve the transport object
        transport = ssh_client.get_transport()

        # Request dynamic port forwarding, which creates a SOCKS5 proxy
        transport.request_port_forward('localhost', local_port)

        print(f"SOCKS5 Proxy is now running on 127.0.0.1:{local_port}")

        # This will keep the SSH tunnel alive
        while True:
            pass

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        ssh_client.close()


def run_ssh_tunnel_in_background():
    # SSH server details and the local port where the SOCKS5 proxy should listen
    username = 'your_ssh_username'
    password = 'your_ssh_password'
    remote_host = 'your_remote_ssh_server'
    remote_port = 22  # Default SSH port
    local_port = 1080  # Local SOCKS5 proxy port

    # Run the tunnel setup in a separate thread
    tunnel_thread = threading.Thread(target=create_ssh_tunnel, args=(username, password, remote_host, remote_port, local_port))
    tunnel_thread.daemon = True  # Daemonize the thread so it exits when the main program exits
    tunnel_thread.start()

    # Allow some time for the tunnel to establish
    tunnel_thread.join()

# Run the tunnel in background
run_ssh_tunnel_in_background()


