import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = socket.gethostbyname(socket.gethostname())
port = 8888

# server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:100,100"]
chat = ""


def threaded_client(conn):
    global currentId, pos, chat
    conn.send(str.encode(currentId))
    currentId = "1"
    chat = "0:"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            id = int(reply[0])
            arr = reply.split('?')
            pos[id] = str(id)+":"+arr[1]
            print(pos)
            reply = arr[0]
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                if len(reply) > 2:
                    print("Recieved: " + reply)
                    chat = reply

                # arr = reply.split(":")
                # id = int(arr[0])
                # chat[id] = reply

                # if id == 0: nid = 1
                # if id == 1: nid = 0

                if len(reply) > 2: print("Sending: " + chat)

            conn.sendall(str.encode(chat+'?'+str(pos[0])+'?'+str(pos[1])))

        except:
            break

    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))
