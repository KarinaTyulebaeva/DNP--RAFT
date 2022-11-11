import grpc
import raft_pb2_grpc as pb2_grpc
import raft_pb2 as pb2

class Client:
    def __init__(self):
        self.channel = None
        self.stub = None

    def connect(self, ip_and_port: str):
        try:
            self.channel = grpc.insecure_channel(ip_and_port)
            self.stub =pb2_grpc.RaftServiceStub(ip_and_port)
        except:
            print("something wrong")    

    def get_leader(self):
        response = self.stub.GetLeader(pb2.Empty())
        print(f'{response.leaderId} {response.address}')       

    def suspend(self, period: int):
        self.stub.Suspend(pb2.SuspendRequest(period = period))     

    def quit(self):
        print("The client ends")
        exit(0)    


    def main_function(self):
        try:
            while True:
                user_input = input()
                command = user_input.split(' ')

                # connection
                if(command[0] == "connect"):
                    self.connect(command[1])

                # get leader        
                elif(command[0] == "getleader"):
                    self.get_leader()

                # suspend
                elif(command[0] == "suspend"):
                    self.suspend(int(command[1]))

                # quit
                elif(command[0] == "quit"):
                    self.quit()

                # man?
                else:
                    print("Unknown command")        

        except KeyboardInterrupt:
            print("Terminating")   


if __name__ == "__main__":
    client = Client()
    client.main_function()