import grpc
import raft_pb2_grpc as pb2_grpc
import raft_pb2 as pb2
import sys
from concurrent import futures

class RaftServerHandler(pb2_grpc.RaftService):
    def zaglushka():
        return kek
        

if __name__ == "__main__":
    id = sys.argv[1]

    config_path = r'/Users/k.tyulebaeva/DNP-ohno-again/config.conf' 
    config_file = open(config_path)
    config_dict = config_file.read().split('\n')

    raft_service = RaftServerHandler()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RaftServiceServicer_to_server(raft_service, server)

    config = config_dict[int(id)].split(' ')
    ip_and_port = f'{config[1]}:{config[2]}'

    server.add_insecure_port(ip_and_port)
    server.start()

    try: 
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Termination')    





