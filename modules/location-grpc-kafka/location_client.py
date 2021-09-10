import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a client that generates random location events.
"""

print("Sending location payload...")

channel = grpc.insecure_channel("127.0.0.1:5999", options=(('grpc.enable_http_proxy', 0),))
stub = location_pb2_grpc.LocationServiceStub(channel)

# create the location payload
order = location_pb2.LocationMessage(
    personId=1,
    longitude=58,
    latitude=2
)

response = stub.Create(order)