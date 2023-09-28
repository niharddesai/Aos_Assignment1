# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import soldier_pb2 as soldier__pb2


class SoldierMatrixServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GenerateMatrix = channel.unary_unary(
                '/SoldierMatrixService/GenerateMatrix',
                request_serializer=soldier__pb2.SoldierMatrixRequest.SerializeToString,
                response_deserializer=soldier__pb2.SoldierMatrixResponse.FromString,
                )
        self.Move = channel.unary_unary(
                '/SoldierMatrixService/Move',
                request_serializer=soldier__pb2.MoveRequest.SerializeToString,
                response_deserializer=soldier__pb2.MoveResponse.FromString,
                )


class SoldierMatrixServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GenerateMatrix(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Move(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SoldierMatrixServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GenerateMatrix': grpc.unary_unary_rpc_method_handler(
                    servicer.GenerateMatrix,
                    request_deserializer=soldier__pb2.SoldierMatrixRequest.FromString,
                    response_serializer=soldier__pb2.SoldierMatrixResponse.SerializeToString,
            ),
            'Move': grpc.unary_unary_rpc_method_handler(
                    servicer.Move,
                    request_deserializer=soldier__pb2.MoveRequest.FromString,
                    response_serializer=soldier__pb2.MoveResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SoldierMatrixService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SoldierMatrixService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GenerateMatrix(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SoldierMatrixService/GenerateMatrix',
            soldier__pb2.SoldierMatrixRequest.SerializeToString,
            soldier__pb2.SoldierMatrixResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Move(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SoldierMatrixService/Move',
            soldier__pb2.MoveRequest.SerializeToString,
            soldier__pb2.MoveResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)