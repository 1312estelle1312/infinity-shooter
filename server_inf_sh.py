import socket
from threading import Thread
from player import Player
import pickle
import constants
import pygame
from bullet import Bullet
import random
from opponent import Opponent
import sys
import copy

server = "YOURIP"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


ready_state = {0: "not_ready", 1: "not_ready"}
game_over_state = [False]
players = [Player(100, constants.HEIGHT/2, 4, 4, 30, "blue", -2, False), Player(100, constants.HEIGHT/2, 4, 4, 30, (118, 31, 184), -2, True)]
list_bullets = [[], []]

#Liste für Gegner
ops1 = []
for _ in range(4):
    x = random.randint(426, 853)
    y = random.randint (240, 480)
    vx = random.randint (-1, 0)
    vy = random.randint (-1, 0)
    opponent = Opponent(x,y,vy,vx)
    ops1.append(opponent)
ops2 = ops1[:]

ops = [ops1, ops2]

connected = [False, False]

world_s = [0, 0]


def threaded_client(conn, player_id):
    conn.send(pickle.dumps([players[player_id], list_bullets[player_id], ops[player_id], game_over_state[0], world_s[player_id]]))
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
            try:
                data_list = pickle.loads(conn.recv(4096))
            except Exception as e:
                break

            players[player_id] = data_list[0]
            list_bullets[player_id] = data_list[1]
            ops[player_id] = data_list[2]
            world_s[player_id] = data_list[4]

            if data_list[3]:
                game_over_state[0] = True

            if not data_list[:]:
                print("Disconnected")
                break 

            else:
                if player_id == 0:

                    reply = [players[1], list_bullets[1], ops[1], game_over_state, world_s[1]]
                else:

                    reply = [players[0], list_bullets[0], ops[0], game_over_state, world_s[0]]
            

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Connection closed")
    connected[player_id] = False
    print(connected)
    running2 = False
    conn.close()


currentPlayer = 0


running = True
s.settimeout(1)

while running:
    try:
        conn, addr = s.accept()
        print("Connected to: ", addr)


        Thread(target=threaded_client, args=(conn, currentPlayer)).start()

        connected[currentPlayer] = True
        currentPlayer += 1
    except socket.timeout:
        if not connected[0] and not connected[1]:
            currentPlayer = 0
            ready_state = {0: "not_ready", 1: "not_ready"}
            game_over_state = [False]
            players = [Player(100, constants.HEIGHT/2, 4, 4, 30, "blue", -2, False), Player(100, constants.HEIGHT/2, 4, 4, 30, (118, 31, 184), -2, True)]
            list_bullets = [[], []]

            ops1 = []
            for _ in range(4):
                x = random.randint(426, 853)
                y = random.randint (240, 480)
                vx = random.randint (-1, 0)
                vy = random.randint (-1, 0)
                opponent = Opponent(x,y,vy,vx)
                ops1.append(opponent)
            ops2 = ops1[:]

            ops = [ops1, ops2]

            world_s = [0, 0]
            number_length = 0.5










