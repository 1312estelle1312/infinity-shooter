import socket
from _thread import *
from player import Player
import pickle
import constants
import pygame
from bullet import Bullet
import random
from opponent import Opponent

#ip = input("IP Addresse: ")
server = "192.168.1.252"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


ready_state = {0: "not_ready", 1: "not_ready"}
players = [Player(100, constants.HEIGHT/2, 4, 4, 30, "blue", -2, False), Player(100, constants.HEIGHT/2, 4, 4, 30, (118, 31, 184), -2, True)]
list_bullets = [[], []]

#Liste für Gegner
ops1 = []
for _ in range(10):
    x = random.randint(426, 853)
    y = random.randint (240, 480)
    vx = random.randint (-1, 0)
    vy = random.randint (-1, 0)
    opponent = Opponent(x,y,vy,vx)
    ops1.append(opponent)
ops2 = ops1
ops = [ops1, ops2]


def threaded_client(conn, player_id):
    conn.send(pickle.dumps([players[player_id], list_bullets[player_id], ops[player_id]]))
    reply = ""
    running1 = True
    running2 = False
    while running1:
        try:
            data = pickle.loads(conn.recv(2048))
            ready_state[player_id] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player_id == 0:
                    reply = ready_state[1]
                    #print(reply)
                else:
                    reply = ready_state[0]

                print(f"Received from {player_id}: {data}")
                print(f"Sending to {player_id}:  {reply}")

                if data == "done":
                    print(f"working {player_id}")
                    running2 = True
                    running1 = False
                    reply = "done"

            conn.sendall(pickle.dumps(reply))
                
        except:
            break
    
    data_list = []
    reply = ""
    while running2:
        try:
            data_list = pickle.loads(conn.recv(2048))

            players[player_id] = data_list[0]
            list_bullets[player_id] = data_list[1]
            ops[0] = data_list[2]
            ops[1] = data_list[2]
            #print(f"Ops: {len(ops[0]), player_id}")
    
            if not data:
                print("Disconnected")
                break
            else:
                if player_id == 0:
                    reply = [players[1], list_bullets[1], ops[1]]
                else:
                    reply = [players[0], list_bullets[0], ops[0]]

                print(f"Received from {player_id}: {data}")
                print(f"Sending to {player_id}:  {reply}")
                
            if data == "game_over":
                
                reply = "game_over"
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Connection closed")
    conn.close()



currentPlayer = 0


running = True
while running:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))

    currentPlayer += 1

