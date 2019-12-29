# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

#from __future__ import print_function
#import logging
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
#-------------------------

class node:
    def __init__(self):
        #self.m_round = 1#not sure i keep it
        self.computeProba = 3
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

    def ping(self):
        print("%s responding to ping !" % self.selfAddress)


    def computeC(self):
        self.c = ( len(self.links) * ( len(self.links) - 1 ) ) / 2 

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
        

    def doDFS(self):
        #print(self.successors)
        #print(self.fathers)
        if self.successors:#if successors non empty, dig

            destination = self.successors.pop()
            self.sons.append(destination)
            self.nb = self.nb +1
            
            print(self.selfAddress + "---" + destination)
            print(self.nb)
            print("------------------------------------")
            self.sendMarker(destination)
        elif self.fathers:#if successors empty but father non empty, go up

            destination = self.fathers.pop()
            print(self.selfAddress + "---" + destination)
            print(self.nb)
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

    def receiveMarker(self,m_round,sender,nb):#called via rpc
        self.nb = nb
        #add as father the sender
        if self.sons:
            if self.sons[-1] != sender:
                self.fathers.append(sender)

        if sender in self.successors:
            self.successors.remove(sender)
        if m_round > self.round:#re init les valeurs du dfs(father, successor)
            self.newDFS()
            self.round = m_round
            #self.sons = [] #either its here or on newDFS
        if self.color == "black":#if the node was active since last passage, increase the round value
            self.nb = 0
            self.newDFS()
            #self.fathers.append(sender)#changed
            self.round = self.round + 1
        #add as father the sender
        if self.sons:
            if self.sons[-1] != sender:
                self.fathers.append(sender)
        self.doDFS()

    def compute(self):
        print(self.selfAddress + "computing...")
        time.sleep(0.5)
        
    def sendMessagesRandom(self):
        if self.links:
            for destination in self.links:
                rand = random.uniform(0, 10)
                print(self.selfAddress + "generated : %s" % rand)
                if rand < self.computeProba:#if the probs are right
                    callRPCfunc2(destination)#call to rpc of second type
        self.computeProba = self.computeProba - self.decreasingFactor#reducing the probs of sendign messages for next time
    
    def receiveMessage(self):#call this and doDFS in the initiator
        self.color = "black"
        self.compute()
        self.sendMessagesRandom()

def callRPCfunc(destination,m_round,sender,nb):
    #instances[addrDict[destination]].ping()
    #instances[addrDict[destination]].receiveMarker(m_round,sender,nb)
    pass

def callRPCfunc2(destination):
    #instances[addrDict[destination]].receiveMessage()
    pass


#-----------------------server side

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        Thread(target=writeQ(request.name)).start()
        print("server received a message : %s" % request.name)
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name) #info is gathered here


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    server.wait_for_termination()

#----------------------------------------client side

def writeQ(value):
    lock.acquire()
    global q
    q.append(value)
    lock.release()

#def readQ():
#    time.sleep(20)
#    lock.acquire()
#    global q
#    print(q)
#    lock.release()


def send(data, address):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    with grpc.insecure_channel(address) as channel:
    #with grpc.insecure_channel('192.168.1.27:50051') as channel:

        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=data))#info is sent here
        
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    data = '1'

    #logging.basicConfig()
    lock = Lock()
    q = []
    #Thread(target=readQ).start()

    t = Thread(target=serve)

    t.start()

    while(data != '0'):
        data = input("")
        address = 'localhost:50053'
        send(data,address)

    sys.exit
