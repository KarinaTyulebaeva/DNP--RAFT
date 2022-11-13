import log_pb2
import log_pb2_grpc
import grpc
from concurrent import futures

class LogServiceHandler(log_pb2_grpc.LogServiceServicer):
    def SendLog(self, request, context):
        print(request.log)
        return log_pb2.EmptyResponse()


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    log_pb2_grpc.add_LogServiceServicer_to_server(LogServiceHandler(), server)
    server.add_insecure_port('127.0.0.1:5555')
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Shutting down')    