#ALL COMMUNICATION (between nodes) is going through gRPC
#each node has an internal state which is updated and used when receiving the marker for carrying out the misra algorithm
#each node can simulate computation and reading/sending messages
#each node has its own address, defined by the first argument send by the user, example:

#arg1 = 3
#address of node is : "localhost:5005<arg1>"  =  "localhost:50053"

#the second argument defines whether the node is (what I call) an "initiator", if arg2 = 1
#the initiator receives a message of computation and the marker,
#it allows us to start the computation in the whole network and to introduce the marker in it

#nodes send messages to other nodes with asynchronous functions using gRPC
#nodes receives these messages also asychronously (through gRPC), package them in a queue.

#A node is either:
#computing something
#processing the marker
#sending the marker/messages by triggering asynchronous functions
#reading from its own queue of messages


#procedure:
#open 4 terminals
#if you use python3:
#on the initiator type: python3 misra.py 1 1
#on the others: 
#python3 misra.py 2 2
#python3 misra.py 3 2
#python3 misra.py 4 2
#then type "1" in the initiator's console

#the messages print in the console have this meaning:
#<sender> ==== <nb> : the node received a marker with that nb from sender 

#<nb> ==== <destination> : the node sent a marker with this nb to that destination


import sys
import time
import random

import grpc

import communication_pb2
import communication_pb2_grpc

#------

from concurrent import futures

from threading import Thread, Lock

table = ["localhost:50051","localhost:50052","localhost:50053","localhost:50054"]



#------------------------- NODE -------------------------------------


class node:
    def __init__(self):
        #used for the random generation of messages
        self.computeProba = 8
        self.decreasingFactor = 1

        self.round = 1
        self.color = "black"
        self.nb = 0#nb of links visited
        self.c = 0#length of a cycle

        self.selfAddress = ""#own adress

        self.links = []#available links (addresses) to other nodes (that marker/messages can travel through)
        self.uv = []#unvisited nodes
        self.f = []#father
        self.s = []#sons

    def ping(self):#function used for debug
        print("%s responding to ping !" % self.selfAddress)


    def computeC(self):#computes the length of a cycle
        self.c = ( len(self.links) * ( len(self.links) - 1 ) ) / 2 


    def createTable(self,addresses):#creates the table of addresses in the node (in links) WORKS
        for i in addresses:
            self.links.append(i)

    def setSelfAddress(self,address):#knows its address, deletes itslef from the links, and compute c
        self.computeC()
        self.links.remove(address)
        self.selfAddress = address
    

    def newDFS(self):#call this if marker is here and process is active, or if self.round > marker.round
        #basically resets the values useful for the DFS
        self.uv = self.links.copy()
        self.f = []
        self.s = []
        

    def sendMarker(self,destination):#makes the rpc call
        #turns the process white as the marker leaves the process for another one
        if self.nb == self.c:
            print("terminated")
            sys.exit()
        self.color = "white"
        callRPCfunc(destination,self.round,self.selfAddress,self.nb)
        self.next()#NEXT HERE

    def receiveMarker(self,m_round,sender,nb):#called via rpc
        #contains a large part of the misra algorithm
        #here the marker is processed according to the internal state of the node,
        #which decides if termination has occured, if the round continues, and where to send
        # the marker next 
        print("---------------------------")
        print("%s ==== %d"%(sender,nb))

        time.sleep(0.5)


        if self.color == "black":
            #reset dfs
            print("MARKER RESET")
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
        #simple function that simulates computation time
        print(self.selfAddress + "computing...")
        time.sleep(0.5)
        
    def sendMessagesRandom(self):
        #simulates the sending of messages of the node
        #messages (that trigger computation in other nodes) are sent randomly to other nodes
        if self.links:
            for destination in self.links:
                rand = random.uniform(0, 10)
                if rand < self.computeProba:#if the probs are right
                    callRPCfunc2(destination)#call to rpc of second type (send a message)
        self.computeProba = self.computeProba - self.decreasingFactor#reducing the probs of sending messages for next time
    
    def receiveMessage(self):#this method is called when the node as fetched a message from the queue (computation)
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
            if val.TYPE == "marker":#if we received a marker, call receiveMarker
                if val.SENDER == "root":
                    self.receiveMarker(val.M_ROUND,val.SENDER,val.NB)
                else:
                    self.receiveMarker(val.M_ROUND,val.SENDER,val.NB)
            elif val.TYPE == "message":##if we received a marker, call receiveMessage
                self.receiveMessage()
    


#------------------------ SENDER FUNCTIONS -------------------------
#these functions are called when the node needs to send a message/marker to another node


def callRPCfunc(destination,m_round,sender,nb):
    #is called when the local node whishes to send a marker to another node
    #after called the function immediately returns, allowing the node to instantly resume execution
    print("%d ==== %s"%(nb,destination))
    print("---------------------------")
    
    with grpc.insecure_channel(destination) as channel:

        stub = communication_pb2_grpc.RemoteStub(channel)
        response = stub.Marker(communication_pb2.MarkerRequest(TYPE="marker", M_ROUND = m_round, SENDER = sender, NB = nb))#info is sent here



def callRPCfunc2(destination):
    #same, but for messages (that will trigger computation in the destination node)
    with grpc.insecure_channel(destination) as channel:
        stub2 = communication_pb2_grpc.RemoteStub(channel)
        stub2.Message(communication_pb2.MessageRequest(TYPE = "message"))









#------------------------------------------------ SERVER FUNCTIONS ------------------------------------------------
#these 2 write inside the Q
#TYPE, M_ROUND, SENDER, NB

#These functions are called in an asynchronous manner when another node sends a message/marker to this node.
#the content of the received request is put in a queue, for the local node to read when it needs to.


class Remote(communication_pb2_grpc.RemoteServicer):


    def Marker(self, request, context):
        #is called when the server received a marker
        #it puts the received element in a queue so that the node can read it later, typically when
        #the ode seeks for its next action (next() method)
        Thread(target=writeQ(request)).start()
        return communication_pb2.MarkerReply(TYPE='Type : %s , M_ROUND : %d , SENDER : %s , NB : %d' % (request.TYPE, request.M_ROUND, request.SENDER, request.NB)) #info is gathered here


    def Message(self,request, context):
        #same, but for messages (triggering computation)
        Thread(target=writeQ(request)).start()
        return communication_pb2.MessageReply(TYPE="message")


def writeQ(value):
    #allows to write a queue of received messages and marker
    #once in a while, when the node finished its current action it fetches from the queue to know
    #its next action (next() method)
    #the queue is in a critical section
    lock.acquire()
    global q
    q.append(value)
    lock.release()

#------------------------------------------------ SERVER SETUP -------------------------------------------
#The server listens on the port specified by the user input

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    communication_pb2_grpc.add_RemoteServicer_to_server(Remote(), server)
    server.add_insecure_port('[::]:5005'+sys.argv[1])
    server.start()
    server.wait_for_termination()


#--------------------------------------------------- MAIN ------------------------------------------------

if __name__ == '__main__':
    data = '1'

    #creates a lock and a queue to write incoming messages for a later used by the local node .the local node reads from the queue
    #when it finishes what it was currently doing
    lock = Lock()
    q = []

    #START THE SERVER
    t = Thread(target=serve)
    t.start()

    #instanciate local node
    NODE = node()
    NODE.createTable(table)
    NODE.setSelfAddress("localhost:5005"+sys.argv[1])
    NODE.newDFS()


    if sys.argv[2] == "2":#if this node is not the initiator (arg2 = 2), then, start it without messages
        NODE.next()


    #READS INPUT
    while(data != '0'):
        data = input("")
        if data == "1":
            writeQ(communication_pb2.MessageRequest(TYPE = "message"))
            writeQ(communication_pb2.MarkerRequest(TYPE="marker", M_ROUND = 1, SENDER = "root", NB = 0))

            if sys.argv[2] == "1":#if node is initiator, start + w/ initial messages
                NODE.next()
        

    sys.exit
