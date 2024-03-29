import socket
from _thread import *
import sys
from player import Player
from platforms import Platform
import random
import pickle
import copy

import time



from settings import *

hostname = socket.gethostname()  # this gets the hostname 
ip_address = socket.gethostbyname(hostname) 

server = str(ip_address)
print(server)
port = 5555  # port that is open and free to use

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 'socket.AF_INET' is the internet address family for IPv4  
# SOCK_STREAM is the socket type for TCP, protocal that is used to trasnport packets on a network
# you can use socket.SOCK_DGRAM for UDP, but it isnt that reliable

try:
    sock.bind((server,port)) # this makes a connection to the server host and the port in order to make a functioning connection
except: # if the 'binding' fails instead of crashing we send an output of the error
    print(socket.error)

sock.listen(2) # opens the socket making it ready to accept connection, it takes one arguement, limiting how many clients can join the server. If empty it is unlimited
# if all goes well up to here, the server has started and is waiting for connections


print("SERVER STARTED!")

#players = [Player(0,0,100,100,(0,255,0)),Player(30,200,100,100,(255,0,0))]




def make_platform(onscreen,i,width,height,screen_height):
    
    if onscreen:
        platform = [random.randint(0,screen_width-width),int(i*(screen_height/START_plat_num)),width,height] 

    else:
        try:
            yrange =  random.randint(int(-screen_height*0.06875),int(-screen_height*0.05)) # make platform out of screen
            platform= [random.randint(0,screen_width-width), yrange,width,height] 
        except:
            pass

    return platform

#pos

connected = set()
games = {}
idCount = 0

leaving_players = 0

def threaded_client(connection, player,gameId): 
 
    global idCount

    player1 = 0
    player2 = 1
    player1_platform = 2
    player2_platform = 3

    try:
       
        data = pickle.loads(connection.recv(2048))
        screen_width = data[0]
        screen_height = data[1]
        START_plat_num = data[2]

        plat_width = int(screen_width*0.11)
        plat_height = int (screen_height*0.05)

        start_platform = [0,int((7*screen_height)/8),screen_width,screen_height/8]

        if player == 0:
            if gameId in games:
                game = games[gameId]
                games[gameId][player1_platform].append(start_platform) 
                games[gameId][player2_platform].append(start_platform) 
                

                for i in range(START_plat_num-1):
                    start_plat = make_platform(True,i,plat_width,plat_height,screen_height)
                    games[gameId][player1_platform].append(start_plat) 
                    games[gameId][player2_platform].append(start_plat)   


        connection.send(pickle.dumps((str(player),games[gameId][player+2])))

        try:   
            
            games[gameId][player+2].clear()
        except Exception as e:
            print(e)



    except Exception as e:
        print(e)
        

    reply= []
    
    
    while True:
        try:
            try:
                data = pickle.loads(connection.recv(2048)) # number of bits that the connection can recieve
            except :
                pass     
                
            if gameId in games:
                game = games[gameId]
                game[player] = data[0]
                send_platform = data[1]
                

                if not data:  # if no data was sent from client, it means they are not in connection, so we print disconnected
                    print("Disconnected")
                    game[player] = [0,0,0,False,True,False] #this allows the other player know he won
                    break

                else:

                    if data == "disconnect":
                        break
                    if data == 'lost' or data == 'won':
                        break
                    if send_platform:
                        temp_plat = make_platform(False,0,plat_width,plat_height,screen_height)
                        game[player1_platform].append(temp_plat)
                        game[player2_platform].append(temp_plat)

                    if player == 1:
                        reply = game[player1]
                        
                        new_platform = copy.deepcopy(game[player2_platform]) # this copies the list onto the other
                        if send_platform:
                            for platform in game[player1_platform]:
                                platform[1] = platform[1]-(game[player2][2]-game[player1][2])
                                                
                        
                        game[player2_platform].clear()
                        
                        
                    else: 
                        
                        reply =  game[player2]
                        
                        new_platform= copy.deepcopy(game[player1_platform])
                        if send_platform: 
                            for platform in game[player2_platform]: 
                            
                                platform[1] = platform[1]-(game[player1][2]-game[player2][2])
                    
                        game[player1_platform].clear()

                connection.sendall(pickle.dumps([reply,new_platform])) # this data is sent back to the client in encoded form, meaning it will have to be decoded by the client once again
    
            else:
                break
            
        except Exception as e:
            print(player,'error',e) 
            break
            
    print('Player',player,"Lost connection")

    try:
        del games[gameId]
        print('Closing game', gameId)
    except Exception as e:
        print (e)
    
    idCount += -1
    connection.close() # we close connection if we lose connection, so that client could joi back if they want. not adding this would cause a confusion or crash

# threading is basically allowing many function to be processed at the same time. For this case, whilst the while loop is running, if it callsthreaded_client, it doesnt need that function to finish to carry on the while loop, the while loop will still run whilt the function is also running
# this is so that it is always allowing for connections to connect. if the function is being run, and a client joins the server, then they wont be able to join as te while loop isnt running at that current time. so threading fixes that problem

while True:
    connection, address = sock.accept()
    print("\n\n\nConnected to:" , address)
    idCount += 1
    print(idCount,"this is the idCount")
    player = 0
    gameId = (idCount-1)//2

    if idCount % 2 == 1:
        games[gameId] = [[1,2,3,False,False],[4,5,6,False,False],[],[]]
       
    else:
        
        player = 1

    start_new_thread(threaded_client,(connection,player,gameId))
    
    
    