import socket
from _thread import *
from player import Player
import pickle
import constants
import pygame

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


def threaded_client(conn, player_id):
    conn.send(pickle.dumps(players[player_id]))
    reply = ""
    running1 = True
    running2 = False
    while running1:
        try:
            data = pickle.loads(conn.recv(2048))

            if data == "done":
                print(f"working {player_id}")
                #pygame.time.wait(5000)
                conn.sendall(pickle.dumps("done"))
                if player_id == 0:
                    conn.send(pickle.dumps(players[1]))
                else:
                    conn.send(pickle.dumps(players[0]))
                running2 = True
                running1 = False


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

            conn.sendall(pickle.dumps(reply))
                
        except:
            break
    
    #data = None

    print("sended")
    reply = ""
    while running2:
        print(f"running on second task {player_id}")
        #conn.send(pickle.dumps(players[player_id]))
        try:
            if player_id == 0:
                conn.send(pickle.dumps(players[1]))
            else:
                conn.send(pickle.dumps(players[0]))
            data = pickle.loads(conn.recv(2048))
            players[player_id] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player_id == 0:
                    reply = players[1]
                else:
                    reply = players[0]

                print(f"Received from {player_id}: {data}")
                print(f"Sending to {player_id}:  {reply}")

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

