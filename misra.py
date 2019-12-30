#procedure:
#open 4 terminals
#on the initiator: type misra.py 1 1
#on the others: 
#misra.py 2 2
#misra.py 3 2
#misra.py 4 2
#then type "1" in the initiator's console


import sys
import time
import random

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

#------

from concurrent import futures

from threading import Thread, Lock

table = ["localhost:50051","localhost:50052","localhost:50053","localhost:50054"]



#------------------------- NODE -------------------------------------


class node:
    def __init__(self):
        #self.m_round = 1#not sure i keep it
        self.computeProba = 8
        self.decreasingFactor = 1

        self.round = 1
        self.state = "active"#change init
        self.color = "black"
        self.nb = 0#nb of links visited
        self.c = 0#length of a cycle

        self.selfAddress = ""

        self.links = []
        self.fathers = []
        self.successors = []
        self.sons = []
        self.uv = []
        self.f = []
        self.s = []

    def ping(self):
        print("%s responding to ping !" % self.selfAddress)


    def computeC(self):
        self.c = ( len(self.links) * ( len(self.links) - 1 ) ) / 2 
        #self.c = 6#---------------------------------------------------------------TODO

    def createTable(self,addresses):#creates the table of addresses in the node (in links) WORKS
        for i in addresses:
            self.links.append(i)

    def setSelfAddress(self,address):#knows its address, deletes itslef from the links WORKS, and compute c
        self.computeC()
        self.links.remove(address)
        self.selfAddress = address
    

    def newDFS(self):#call this if marker is here and process is active, or if self.round > marker.round
        #self.round = self.round+1
        self.fathers  = []
        self.sons = []
        self.successors = self.links.copy()
        self.uv = self.links.copy()
        self.f = []
        self.s = []
        

    def doDFS(self):
        print("successors, fathers")
        print(self.successors)
        print(self.fathers)

        if self.successors:#if successors non empty, dig

            destination = self.successors.pop()
            self.sons.append(destination)
            self.nb = self.nb +1
            
            
            print(self.selfAddress + "---" + destination)
            #print(self.successors)
            #print(self.nb)
            print("------------------------------------")
            self.sendMarker(destination)
        elif self.fathers:#if successors empty but father non empty, go up

            destination = self.fathers.pop()
            print(self.selfAddress + "---" + destination)
            #print(self.successors)
            #print(self.nb)
            print("------------------------------------")
            self.sendMarker(destination)
        else:#report termination
            print("terminated")
            sys.exit()

    

    def isTerminated(self):
        #if(self.state == "passive" and self.color == "white" and )
        pass
    #def newRound():#flushes nb, 

    def sendMarker(self,destination):#makes the rpc call
        if self.nb == self.c:
            print("terminated")
            sys.exit()
        self.color = "white"
        callRPCfunc(destination,self.round,self.selfAddress,self.nb)
        self.next()#NEXT HERE

    def receiveMarker(self,m_round,sender,nb):#called via rpc
        print("---------------------------")
        print(sender)
        print(nb)
        print(self.selfAddress)
        print("---------------------------")
        time.sleep(0.5)


        if self.color == "black":
            #reset dfs
            self.newDFS()
            #will send a nb of 0
            nb = 0
            #copy round and increase own round and round sent
            self.round = m_round
            self.round = self.round + 1
            m_round = m_round + 1
            #pick a destination and pop uv
            destination = self.uv.pop()
            #add desti to sons
            self.s.append(destination)
            #set White
            self.color = "white"
            #send
            callRPCfunc(destination,m_round,self.selfAddress,nb)
            self.next()
        if self.color == "white":
            #check for termination
            if nb == self.c-1:
                print("Terminated (nb)")
                sys.exit(0)


            if self.round == m_round:
                if self.s:
                    if sender == self.s[-1]:   
                        self.s.pop()#pop son
                        if self.uv:
                            #pop desti from uv and add desti to sons
                            destination = self.uv.pop()
                            self.s.append(destination)
                            nb = nb + 1
                            callRPCfunc(destination,m_round,self.selfAddress,nb)
                            self.next()
                        else:
                            #go to last father
                            if self.f:
                                #pop from f
                                destination = self.f.pop()
                                #just go to f
                                callRPCfunc(destination,m_round,self.selfAddress,nb)
                                self.next()
                            #if no father then terminated
                            else:
                                print("Terminated (f)")
                                sys.exit(0)
                    else:
                        #send back to last sender
                        callRPCfunc(sender,m_round,self.selfAddress,nb)
                        self.next()
                else:
                    print("Terminated (s)")
                    sys.exit(0)
            else:
                #reset DFS f,s and uv
                self.newDFS()
                #add as father the sender
                self.f.append(sender)
                #copy the round
                self.round = m_round
                #remove the sender from the unvisited this round
                self.uv.remove(sender)
                #dont forget to increase nb

                if self.uv:
                    #pop desti from uv and add desti to sons, increase nb, send
                    destination = self.uv.pop()
                    self.s.append(destination)
                    nb = nb + 1
                    callRPCfunc(destination,m_round,self.selfAddress,nb)
                    self.next()
                else:
                    #go to last father
                    if self.f:
                        #pop from f
                        destination = self.f.pop()
                        #just go to f
                        callRPCfunc(destination,m_round,self.selfAddress,nb)
                        self.next()
                    #if no father then terminated
                    else:
                        print("Terminated (f)")
                        sys.exit(0)
   

    def compute(self):
        print(self.selfAddress + "computing...")
        time.sleep(0.5)
        
    def sendMessagesRandom(self):
        if self.links:
            for destination in self.links:
                rand = random.uniform(0, 10)
                #print(self.selfAddress + "generated : %s" % rand)
                if rand < self.computeProba:#if the probs are right
                    callRPCfunc2(destination)#call to rpc of second type
        self.computeProba = self.computeProba - self.decreasingFactor#reducing the probs of sendign messages for next time
    
    def receiveMessage(self):#call this and doDFS in the initiator
        self.color = "black"
        self.compute()
        self.sendMessagesRandom()
        self.next()#NEXT HERE
    
    def next(self):#fetches from the queue to know what's next
        global q
        test = not q
        while test:
            time.sleep(0.5)
            lock.acquire()
            test = not q
            lock.release()

        if q:
            lock.acquire()
            val = q.pop(0)
            lock.release()
            if val.TYPE == "marker":#do the marker part
                if val.SENDER == "root":
                    self.receiveMarker(val.M_ROUND,val.SENDER,val.NB)
                    #self.doDFS()
                else:
                    self.receiveMarker(val.M_ROUND,val.SENDER,val.NB)
            elif val.TYPE == "message":#do the message part
                self.receiveMessage()
        #else:
            #lock.release()
    
    def startNode(self):
        pass


#------------------------ SENDER FUNCTIONS -------------------------


def callRPCfunc(destination,m_round,sender,nb):
    #instances[addrDict[destination]].ping()
    #instances[addrDict[destination]].receiveMarker(m_round,sender,nb)
    with grpc.insecure_channel(destination) as channel:

        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.Marker(helloworld_pb2.MarkerRequest(TYPE="marker", M_ROUND = m_round, SENDER = sender, NB = nb))#info is sent here
        #stub2 = helloworld_pb2_grpc.GreeterStub(channel)
        #stub2.Message(helloworld_pb2.Empty)

    #print("NODE %s has sent to NODE %s a marker: m_round %d, nb %d" % (sender,destination, m_round,nb))


def callRPCfunc2(destination):
    #instances[addrDict[destination]].receiveMessage()
    global NODE
    with grpc.insecure_channel(destination) as channel:

        stub2 = helloworld_pb2_grpc.GreeterStub(channel)
        stub2.Message(helloworld_pb2.MessageRequest(TYPE = "message"))
    #print("NODE %s has sent to NODE %s a message" % (NODE.selfAddress,destination))








#------------------------------------------------ SERVER FUNCTIONS ------------------------------------------------
#these 2 write inside the Q
#TYPE, M_ROUND, SENDER, NB
#TYPE

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    #instances[addrDict[destination]].receiveMarker(m_round,sender,nb)
    def Marker(self, request, context):
        Thread(target=writeQ(request)).start()
        #print("server received a Marker : %s" % request.TYPE)
        return helloworld_pb2.MarkerReply(TYPE='Type : %s , M_ROUND : %d , SENDER : %s , NB : %d' % (request.TYPE, request.M_ROUND, request.SENDER, request.NB)) #info is gathered here

    #instances[addrDict[destination]].receiveMessage()
    def Message(self,request, context):
        Thread(target=writeQ(request)).start()
        #print("Message of start of computation received")
        return helloworld_pb2.MessageReply(TYPE="message")


def writeQ(value):
    #print("waiting for lock, value:")
    #print(value)
    lock.acquire()
    #print("lock acquired")
    global q
    q.append(value)
    lock.release()

#------------------------------------------------ SERVER SETUP -------------------------------------------

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:5005'+sys.argv[1])
    server.start()
    server.wait_for_termination()

#----------------------------------------client side



def readQ():
    time.sleep(20)
    lock.acquire()
    global q
    print(q)
    lock.release()

#-------------------------------------------------------- ANCESTRY __ DO NOT TOUCH --------------------------

def send(data, address):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    with grpc.insecure_channel(address) as channel:
    #with grpc.insecure_channel('192.168.1.27:50051') as channel:

        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.Marker(helloworld_pb2.MarkerRequest(TYPE=data, M_ROUND = 2, SENDER = "PLACEHOLDER", NB = 6))#info is sent here
        #stub2 = helloworld_pb2_grpc.GreeterStub(channel)
        #stub2.Message(helloworld_pb2.Empty)

    print("Greeter client received: " + response.TYPE)

def send2(address):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    with grpc.insecure_channel(address) as channel:
    #with grpc.insecure_channel('192.168.1.27:50051') as channel:

        stub2 = helloworld_pb2_grpc.GreeterStub(channel)
        stub2.Message(helloworld_pb2.MessageRequest(TYPE = "message"))
        print("computationnal message sent!")



#--------------------------------------------------- MAIN ------------------------------------------------

if __name__ == '__main__':



    data = '1'
    #logging.basicConfig()
    lock = Lock()
    q = []
    #Thread(target=readQ).start()

    #START THE SERVER
    t = Thread(target=serve)
    t.start()

    #instanciate local node
    NODE = node()
    NODE.createTable(table)
    NODE.setSelfAddress("localhost:5005"+sys.argv[1])
    NODE.newDFS()

    #address = 'localhost:5005'+sys.argv[2]#address to send to

    if sys.argv[2] == "2":#if this node is not the initiator (arg2 = 2), then, start it without messages
        NODE.next()
        #Thread(target=NODE.next()).start()

    #READS INPUT
    while(data != '0'):
        data = input("")
        if data == "1":
            writeQ(helloworld_pb2.MessageRequest(TYPE = "message"))
            writeQ(helloworld_pb2.MarkerRequest(TYPE="marker", M_ROUND = 1, SENDER = "root", NB = 0))#
            #NODE.round = 0#in case of
            if sys.argv[2] == "1":#if node is initiator, start + w/ initial messages
                NODE.next()
            #Thread(target=NODE.next()).start()
        
        #if data == "1":
        #    send(data,address)
        #if data == "2":
        #    send2(address)
        
        

    sys.exit
