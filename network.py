import socket
import pickle  #allows to send objects through network, it decodes and encodes for you


class Network:
   
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 'socket.AF_INET' is the internet address family for IPv4  
        # SOCK_STREAM is the socket type for TCP, protocal that is used to trasnport packets on a network
        # you can use socket.SOCK_DGRAM for UDP, but it isnt that reliable

        self.hostname = socket.gethostname()  # this gets the hostname 
        self.ip_address = socket.gethostbyname(self.hostname) # getting the IPv4 address using socket.gethostbyname() method

        self.server = str(self.ip_address)
        self.port = 5555 # port that is open and free to use
        self.address = (self.server, self.port)
        self.p = self.connect()
    
    def getP(self):
        return self.p
    
    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2046))
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))  #pickle.dumps  = encode
            return pickle.loads(self.client.recv(2046)) # pickle.loads = decode
        except:
            print(socket.error())


