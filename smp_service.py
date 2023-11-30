import grpc
from concurrent import futures
import smp_pb2
import smp_pb2_grpc


class StatusCheckerServicer(smp_pb2_grpc.StatusCheckerServicer):
    def CheckStatus(self, request, context):
        # Here you can implement the logic to check the status and return "booting", "running", or "error".
        # For now, let's just return "running".
        return smp_pb2.StatusReply(status="running")


class SmartPowerClient:
    def __init__(self, host="localhost", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = smp_pb2_grpc.SmartPowerServiceStub(self.channel)

    def check_status(self):
        request = smp_pb2.StatusRequest()
        response = self.stub.CheckStatus(request)
        return response.status


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    smp_pb2_grpc.add_StatusCheckerServicer_to_server(StatusCheckerServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("Starting server...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    SmartPowerClient().check_status()
