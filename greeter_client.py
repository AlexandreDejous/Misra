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

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

#------

from concurrent import futures

from threading import Thread
#-----------------------

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        print("server received a message : %s" % request.name)
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name) #info is gathered here


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

#----------------------------------------


def run(data):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    with grpc.insecure_channel('localhost:50051') as channel:
    #with grpc.insecure_channel('192.168.1.27:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=data))#info is sent here
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    data = '1'
    #logging.basicConfig()
    t = Thread(target=serve)

    t.start()

    while(data != '0'):
        data = input("")
        run(data)

    sys.exit
