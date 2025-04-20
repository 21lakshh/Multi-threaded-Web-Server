import socket
from concurrent.futures import ThreadPoolExecutor

def get_local_ip():
    """Get the local IP address of the machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

HOST = get_local_ip()  # Automatically detect the local IP address
PORT = 8080       

# Response to send
HTTP_RESPONSE = b"""\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<html>
    <head><title>My Web Server</title></head>
    <body>
        <h1>Hello Mr. Dibakar Sinha Sir.</h1>
    </body>
</html>
"""

def handle_client(client_socket, address):
    try:
        request = client_socket.recv(1024).decode()
        print(f"[+] Received request from {address}:\n{request.splitlines()[0]}")
        client_socket.sendall(HTTP_RESPONSE)
    except Exception as e:
        print(f"[-] Error handling {address}: {e}")
    finally:
        client_socket.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        print(f"Server listening on http://{HOST}:{PORT}")
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                client_socket, addr = server_socket.accept()
                executor.submit(handle_client, client_socket, addr)

if __name__ == "__main__":
    main()
