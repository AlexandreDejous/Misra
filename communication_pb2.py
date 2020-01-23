# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: communication.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='communication.proto',
  package='communication',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x13\x63ommunication.proto\x12\rcommunication\"J\n\rMarkerRequest\x12\x0c\n\x04TYPE\x18\x01 \x01(\t\x12\x0f\n\x07M_ROUND\x18\x02 \x01(\x03\x12\x0e\n\x06SENDER\x18\x03 \x01(\t\x12\n\n\x02NB\x18\x04 \x01(\x03\"\x1b\n\x0bMarkerReply\x12\x0c\n\x04TYPE\x18\x01 \x01(\t\"\x1e\n\x0eMessageRequest\x12\x0c\n\x04TYPE\x18\x01 \x01(\t\"\x1c\n\x0cMessageReply\x12\x0c\n\x04TYPE\x18\x01 \x01(\t2\x93\x01\n\x06Remote\x12\x42\n\x06Marker\x12\x1c.communication.MarkerRequest\x1a\x1a.communication.MarkerReply\x12\x45\n\x07Message\x12\x1d.communication.MessageRequest\x1a\x1b.communication.MessageReplyb\x06proto3')
)




_MARKERREQUEST = _descriptor.Descriptor(
  name='MarkerRequest',
  full_name='communication.MarkerRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='TYPE', full_name='communication.MarkerRequest.TYPE', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='M_ROUND', full_name='communication.MarkerRequest.M_ROUND', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='SENDER', full_name='communication.MarkerRequest.SENDER', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='NB', full_name='communication.MarkerRequest.NB', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=112,
)


_MARKERREPLY = _descriptor.Descriptor(
  name='MarkerReply',
  full_name='communication.MarkerReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='TYPE', full_name='communication.MarkerReply.TYPE', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=114,
  serialized_end=141,
)


_MESSAGEREQUEST = _descriptor.Descriptor(
  name='MessageRequest',
  full_name='communication.MessageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='TYPE', full_name='communication.MessageRequest.TYPE', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=173,
)


_MESSAGEREPLY = _descriptor.Descriptor(
  name='MessageReply',
  full_name='communication.MessageReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='TYPE', full_name='communication.MessageReply.TYPE', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=175,
  serialized_end=203,
)

DESCRIPTOR.message_types_by_name['MarkerRequest'] = _MARKERREQUEST
DESCRIPTOR.message_types_by_name['MarkerReply'] = _MARKERREPLY
DESCRIPTOR.message_types_by_name['MessageRequest'] = _MESSAGEREQUEST
DESCRIPTOR.message_types_by_name['MessageReply'] = _MESSAGEREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MarkerRequest = _reflection.GeneratedProtocolMessageType('MarkerRequest', (_message.Message,), {
  'DESCRIPTOR' : _MARKERREQUEST,
  '__module__' : 'communication_pb2'
  # @@protoc_insertion_point(class_scope:communication.MarkerRequest)
  })
_sym_db.RegisterMessage(MarkerRequest)

MarkerReply = _reflection.GeneratedProtocolMessageType('MarkerReply', (_message.Message,), {
  'DESCRIPTOR' : _MARKERREPLY,
  '__module__' : 'communication_pb2'
  # @@protoc_insertion_point(class_scope:communication.MarkerReply)
  })
_sym_db.RegisterMessage(MarkerReply)

MessageRequest = _reflection.GeneratedProtocolMessageType('MessageRequest', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGEREQUEST,
  '__module__' : 'communication_pb2'
  # @@protoc_insertion_point(class_scope:communication.MessageRequest)
  })
_sym_db.RegisterMessage(MessageRequest)

MessageReply = _reflection.GeneratedProtocolMessageType('MessageReply', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGEREPLY,
  '__module__' : 'communication_pb2'
  # @@protoc_insertion_point(class_scope:communication.MessageReply)
  })
_sym_db.RegisterMessage(MessageReply)



_REMOTE = _descriptor.ServiceDescriptor(
  name='Remote',
  full_name='communication.Remote',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=206,
  serialized_end=353,
  methods=[
  _descriptor.MethodDescriptor(
    name='Marker',
    full_name='communication.Remote.Marker',
    index=0,
    containing_service=None,
    input_type=_MARKERREQUEST,
    output_type=_MARKERREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Message',
    full_name='communication.Remote.Message',
    index=1,
    containing_service=None,
    input_type=_MESSAGEREQUEST,
    output_type=_MESSAGEREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_REMOTE)

DESCRIPTOR.services_by_name['Remote'] = _REMOTE

# @@protoc_insertion_point(module_scope)