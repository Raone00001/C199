import socket
from threading import Thread

#creating server with socket --> first is address family (ones socket can communicate with (common one is ipV4 and ipV6)) and second is socket type
#AF_INET represents IpV4, AF_INET6 is IpV6 (address families through which the server can communicate with)
#Sock_stream is a default value (used to create a TCP socket) (here we are only using TCP, since we aren't using Sock_DGram)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1' #local ip address
port = 8000 #has to be over 1000

#Bind the server with the ip address and port
#Server is a socket object
server.bind((ip_address, port))
server.listen()

list_of_clients = []

print("Server has started...")

def clientthread(conn, addr):
    conn.send("Welcome to this chatroom!".encode('utf-8')) #encoding in comp. language
    #To keep the connection on until/unless it breaks
    while True:
        try:
            message = conn.recv(2048).decode('utf-8') #decode msg to human language
            if message:
                print("<" + addr[0] + ">" + message)

                message_to_send = "<" + addr[0] + ">" + message
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        #client's side connection with address
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + "connected")
    new_thread = Thread(target = clientthread,args=(conn,addr))
    new_thread.start()
