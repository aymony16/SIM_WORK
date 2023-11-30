# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import smp_pb2 as smp__pb2


class StatusCheckerStub(object):
    """The status checking service definition."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CheckStatus = channel.unary_unary(
            "/smartpower.StatusChecker/CheckStatus",
            request_serializer=smp__pb2.StatusRequest.SerializeToString,
            response_deserializer=smp__pb2.StatusReply.FromString,
        )


class StatusCheckerServicer(object):
    """The status checking service definition."""

    def CheckStatus(self, request, context):
        """Checks the status"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_StatusCheckerServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "CheckStatus": grpc.unary_unary_rpc_method_handler(
            servicer.CheckStatus,
            request_deserializer=smp__pb2.StatusRequest.FromString,
            response_serializer=smp__pb2.StatusReply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "smartpower.StatusChecker", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class StatusChecker(object):
    """The status checking service definition."""

    @staticmethod
    def CheckStatus(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/smartpower.StatusChecker/CheckStatus",
            smp__pb2.StatusRequest.SerializeToString,
            smp__pb2.StatusReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )