from concurrent import futures
import grpc
import smp_pb2_grpc
import smp_pb2


class SmartPowerService(smp_pb2_grpc.SmartPowerServiceServicer):
    def CheckStatus(self, request, context):
        # Implement your logic here to check the status.
        # This is just a placeholder implementation.
        return smp_pb2.Response(response="Status OK")

    def CheckTemperature(self, request, context):
        # Implement your logic here to check the temperature.
        # This is just a placeholder implementation.
        return smp_pb2.Response(response="Temperature OK")


class SmartPowerClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = smp_pb2_grpc.SmartPowerServiceStub(self.channel)

    def check_status(self):
        request = smp_pb2.StatusRequest()
        response = self.stub.CheckStatus(request)
        return response.status


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    smp_pb2_grpc.add_SmartPowerServiceServicer_to_server(
        SmartPowerService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("SmartPowerService started")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
