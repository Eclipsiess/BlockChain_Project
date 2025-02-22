import socket
import threading
import time
from datetime import datetime

class PeerToPeerChat:
    def __init__(self, team_name, port):
        self.team_name = team_name
        self.port = port
        self.host_ip = self.get_local_ip()
        self.peers = set()  # Stores (ip, port) tuples
        self.lock = threading.Lock()
        self.running = True
        
        # Server socket setup
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host_ip, port))
        self.server_socket.listen(5)
        
        # Start server thread
        self.server_thread = threading.Thread(target=self.accept_connections, daemon=True)
        self.server_thread.start()
        
        # Start peer maintenance thread
        self.maintenance_thread = threading.Thread(target=self.peer_maintenance, daemon=True)
        self.maintenance_thread.start()
        
        # Start UI loop
        self.ui_loop()

    def get_local_ip(self):
        """ Get the local IP address of the machine. """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def accept_connections(self):
        """ Accept incoming connections from peers. """
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except Exception as e:
                if self.running:
                    print(f"⚠️ Server socket error: {e}")
                break

    def handle_client(self, client_socket):
        """ Handle incoming messages and add peers. """
        try:
            data = client_socket.recv(1024).decode()
            if data:
                header_end = data.find('>')
                if header_end != -1:
                    header = data[1:header_end]
                    sender_ip, sender_port = header.split(':')
                    sender_port = int(sender_port)

                    # Add to peer list
                    with self.lock:
                        if (sender_ip, sender_port) not in self.peers:
                            self.peers.add((sender_ip, sender_port))
                            print(f"🔗 New peer added: {sender_ip}:{sender_port}")

                    # Display message
                    message = data[header_end+2:].split(' ', 1)[1]
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"\n[{timestamp}] {sender_ip}:{sender_port} - {message}\nMenu choice: ", end='')
        except Exception as e:
            print(f"⚠️ Error handling client: {e}")
        finally:
            client_socket.close()

    def send_message(self, ip, port, message):
        """ Send a message to a peer. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((ip, port))
                full_msg = f"<{self.host_ip}:{self.port}> {self.team_name} {message}"
                s.send(full_msg.encode())
                print(f"✅ Message sent to {ip}:{port}")
        except Exception as e:
            print(f"❌ Failed to send message to {ip}:{port} - {e}")

    def peer_maintenance(self):
        """ Periodically check and remove inactive peers. """
        while self.running:
            time.sleep(10)
            with self.lock:
                to_remove = []
                for ip, port in list(self.peers):
                    if not self.ping_peer(ip, port):
                        to_remove.append((ip, port))

                for peer in to_remove:
                    self.peers.remove(peer)
                    print(f"🚫 Removed inactive peer: {peer[0]}:{peer[1]}")

    def ping_peer(self, ip, port):
        """ Check if a peer is reachable. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((ip, port))
                return True
        except:
            return False

    def connect_to_peer(self, ip, port):
        """ Connect to a peer and send a handshake. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((ip, port))
                s.send(f"<{self.host_ip}:{self.port}> HANDSHAKE".encode())

                with self.lock:
                    self.peers.add((ip, port))
                print(f"✅ Successfully connected to {ip}:{port}")
                return True
        except Exception as e:
            print(f"❌ Connection to {ip}:{port} failed: {e}")
            return False

    def ui_loop(self):
        """ Main user interface loop. """
        while self.running:
            print("\n***** Menu *****")
            print("1. Send message")
            print("2. Query active peers")
            print("3. Connect to peer")
            print("0. Quit")
            
            choice = input("Enter choice: ")
            
            if choice == '1':
                ip = input("Enter recipient IP: ")
                port = int(input("Enter recipient port: "))
                message = input("Enter message: ")
                self.send_message(ip, port, message)
                
            elif choice == '2':
                with self.lock:
                    if not self.peers:
                        print("\n⚠️ No peers available!")
                    else:
                        print("\nActive peers:")
                        for i, (ip, port) in enumerate(self.peers, 1):
                            print(f"[{i}] {ip}:{port}")
                        
            elif choice == '3':
                ip = input("Enter peer IP: ")
                port = int(input("Enter peer port: "))
                if self.connect_to_peer(ip, port):
                    print("Connection successful")
                else:
                    print("Connection failed")
                    
            elif choice == '0':
                self.running = False
                self.server_socket.close()
                print("👋 Exiting...")
                break

            else:
                print("⚠️ Invalid choice!")

if __name__ == "__main__":
    team = input("Enter team name: ")
    port = int(input("Enter port number: "))
    PeerToPeerChat(team, port)