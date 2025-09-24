import socket
import threading

SERVER_IP = '0.0.0.0'  # Replace with server IP
PORT = 11223

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Connection closed by server.")
                break
            print(f"\nServer: {data.decode()}")
        except:
            break

def send_messages(sock):
    while True:
        msg = input()
        if msg.lower() == 'exit':
            sock.close()
            break
        try:
            sock.sendall(msg.encode())
        except:
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))
    print(f"Connected to server at {SERVER_IP}:{PORT}")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    send_messages(client_socket)

if __name__ == "__main__":
    main()
