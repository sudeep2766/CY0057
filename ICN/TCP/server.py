import socket
import threading

HOST = '0.0.0.0'
PORT = 11223

def receive_messages(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print("Connection closed by client.")
                break
            print(f"\nClient: {data.decode()}")
        except:
            break

def send_messages(conn):
    while True:
        msg = input()
        if msg.lower() == 'exit':
            conn.close()
            break
        try:
            conn.sendall(msg.encode())
        except:
            break

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    # Start receiving thread
    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()
    # Start sending thread (runs in main thread)
    send_messages(conn)

    server_socket.close()

if __name__ == "__main__":
    main()
