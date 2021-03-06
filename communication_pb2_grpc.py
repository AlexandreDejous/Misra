# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import communication_pb2 as communication__pb2


class RemoteStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Marker = channel.unary_unary(
        '/communication.Remote/Marker',
        request_serializer=communication__pb2.MarkerRequest.SerializeToString,
        response_deserializer=communication__pb2.MarkerReply.FromString,
        )
    self.Message = channel.unary_unary(
        '/communication.Remote/Message',
        request_serializer=communication__pb2.MessageRequest.SerializeToString,
        response_deserializer=communication__pb2.MessageReply.FromString,
        )


class RemoteServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Marker(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Message(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_RemoteServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Marker': grpc.unary_unary_rpc_method_handler(
          servicer.Marker,
          request_deserializer=communication__pb2.MarkerRequest.FromString,
          response_serializer=communication__pb2.MarkerReply.SerializeToString,
      ),
      'Message': grpc.unary_unary_rpc_method_handler(
          servicer.Message,
          request_deserializer=communication__pb2.MessageRequest.FromString,
          response_serializer=communication__pb2.MessageReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'communication.Remote', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
