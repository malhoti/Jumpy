This is my NEA Project for my A-levels

The game has two modes  
* Solo mode (where you play by yourself)
* Mulitplayer ( where you play with someone on the same local network as you)

To play Solo mode:
* run the `client.py` file for the solo mode

To play Mulitplayer mode:
* run the `server.py` file
* an ip address will be displayed on console
* copy that ip address 
* Change `self.ip_address = socket.gethostbyname(self.hostname)` into `self.ip_address = "YOUR IP THAT YOU COPIED"` in the `network.py` file
* The person that is running the server on that device, if you decide to also play on the same device, the above step is not needed
* Once the above steps have been done, you can now run the `client.py` file and then proceed to play
