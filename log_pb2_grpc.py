# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import log_pb2 as log__pb2


class LogServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendLog = channel.unary_unary(
                '/LogService/SendLog',
                request_serializer=log__pb2.SendLogRequest.SerializeToString,
                response_deserializer=log__pb2.EmptyResponse.FromString,
                )


class LogServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendLog(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LogServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendLog': grpc.unary_unary_rpc_method_handler(
                    servicer.SendLog,
                    request_deserializer=log__pb2.SendLogRequest.FromString,
                    response_serializer=log__pb2.EmptyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'LogService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LogService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendLog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LogService/SendLog',
            log__pb2.SendLogRequest.SerializeToString,
            log__pb2.EmptyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
