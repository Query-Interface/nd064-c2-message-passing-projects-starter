# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: location.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='location.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0elocation.proto\"H\n\x0fLocationMessage\x12\x10\n\x08personId\x18\x01 \x01(\x05\x12\x10\n\x08latitude\x18\x02 \x01(\x02\x12\x11\n\tlongitude\x18\x03 \x01(\x02\x32?\n\x0fLocationService\x12,\n\x06\x43reate\x12\x10.LocationMessage\x1a\x10.LocationMessageb\x06proto3'
)




_LOCATIONMESSAGE = _descriptor.Descriptor(
  name='LocationMessage',
  full_name='LocationMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='personId', full_name='LocationMessage.personId', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='latitude', full_name='LocationMessage.latitude', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='longitude', full_name='LocationMessage.longitude', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=18,
  serialized_end=90,
)

DESCRIPTOR.message_types_by_name['LocationMessage'] = _LOCATIONMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LocationMessage = _reflection.GeneratedProtocolMessageType('LocationMessage', (_message.Message,), {
  'DESCRIPTOR' : _LOCATIONMESSAGE,
  '__module__' : 'location_pb2'
  # @@protoc_insertion_point(class_scope:LocationMessage)
  })
_sym_db.RegisterMessage(LocationMessage)



_LOCATIONSERVICE = _descriptor.ServiceDescriptor(
  name='LocationService',
  full_name='LocationService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=92,
  serialized_end=155,
  methods=[
  _descriptor.MethodDescriptor(
    name='Create',
    full_name='LocationService.Create',
    index=0,
    containing_service=None,
    input_type=_LOCATIONMESSAGE,
    output_type=_LOCATIONMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_LOCATIONSERVICE)

DESCRIPTOR.services_by_name['LocationService'] = _LOCATIONSERVICE

# @@protoc_insertion_point(module_scope)
