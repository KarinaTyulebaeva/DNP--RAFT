import grpc
import raft_pb2_grpc as pb2_grpc
import raft_pb2 as pb2
import sys
from concurrent import futures
import random
from threading import Timer
import math

import log_pb2 as log_pb2
import log_pb2_grpc as log_pb2_grpc

class RaftServerHandler(pb2_grpc.RaftService):
    def __init__(self, config_dict, id):
        self.term = 0
        self.state = "follower"

        self.timer = None
        self.timer_count = random.randint(150, 300)

        self.config_dict = config_dict
        self.config_dict['leader'] = None
        self.heartbeat = 50
        self.id = id
        self.votes = 0
        self.restart_timer(self.become_candidate)

        self.voted = False

    def init_timer(self):
        self.timer_count = random.randint(150, 300)    

    def restart_timer(self, function):
        self.timer = Timer(self.timer_count, function)  
        self.timer.start() 

    def update_term(self, n):
        self.term = n
        self.voted = False   

    def check_votes(self):
        if self.state != 'candidare':
            return
        if(self.votes >= math.floor((len(self.config_dict)-1)/2)):
            self.state = 'leader'
            # TODO: отдавать хартбит - тоже добавить таймер с функцией хартбита?
        else:
            self.state = 'follower'
            self.init_timer()
            self.restart_timer(self.become_candidate)


    def become_candidate(self):
        self.update_term(1)
        self.state = 'candidate'  
        self.restart_timer(self.check_votes)
        self.votes = 1
        self.voted = True

        for id, ip_and_port in self.config_dict:
            if(id != 'leader'):
                new_channel = grpc.insecure_channel(ip_and_port)
                new_stub = pb2_grpc.RaftServiceStub(new_channel)

                msg = {"term": self.term, "candidateId": self.id}
                request_vote_response = new_stub.RequestVote(**msg)

                if(request_vote_response.result == True):
                    self.votes+=1

    def reset_votes(self):
        self.votes = 0

    def RequestVote(self, request, context):
        self.timer.restart()
        
        # follower
        if(self.state == 'follower'):
            if(request.term == self.term):
                self.voted = True
                reply = {"term": self.term, "result": True}
                return pb2.RequestVoteResponse(**reply)
            elif(request.term > self.term):
                self.update_term(request.term)
                self.voted = True  
            else:
                reply = {"term": self.term, "result": False}
                return pb2.RequestVoteResponse(**reply)      

        # candidate
        elif(self.state == 'candidate'):
            if(request.term == self.term):
                print('Should never happppppppen ;)')

            elif(request.term > self.term):
                self.update_term(request.term)
                self.state = 'follower'
                self.voted = True
                reply = {"term": self.term, "result": True}
                return pb2.RequestVoteResponse(**reply)    

            else:
                reply = {"term": self.term, "result": False}
                return pb2.RequestVoteResponse(**reply)

        # leader        
        else:
            if(request.term == self.term):
                print('Should never happppppppen ;)')

            elif(request.term > self.term):
                self.update_term(request.term)
                self.voted = True    
                reply = {"term": self.term, "result": True}
                return pb2.RequestVoteResponse(**reply)

            else:
                reply = {"term": self.term, "result": False}
                return pb2.RequestVoteResponse(**reply)    

    def AppendEntries(self, request, context):
        self.timer.restart()

        if(request.term >= self.term):
            # Потому что if the Candidate receives the message (any message) with the term number greater than its own, it stops the election and becomes a Follower
            # Или if the Leader receives a heartbeat message from another Leader with the term number greater than its own, it becomes a Follower 
            self.state = 'follower'

            self.config_dict['leader'] = request.leaderId
            self.update_term(request.term)
            reply = {"term": self.term, "success": True}
            return pb2.AppendEntriesResponse(**reply)
        else:
            reply = {"term": self.term, "success": False}
            return pb2.AppendEntriesResponse(**reply)    

    def GetLeader(self, request, context):
        self.timer.restart()

    def Suspend(self, request, context):           
        self.timer.restart()

    def log(self, message):
        log_channel = grpc.insecure_channel(f'127.0.0.1:5555')
        log_stub = log_pb2_grpc.LogServiceStub(log_channel)
        msg = {"log": f'{self.id}  {message}'}    
        log_stub.SendLog(**msg)

if __name__ == "__main__":
    id = sys.argv[1]

    config_path = r'config.conf' 
    config_file = open(config_path)
    config_dict = config_file.read().split('\n')

    try:
        config = config_dict[int(id)].split(' ')
    except:
        print('No such id in the config file')    
        exit(0)

    raft_service = RaftServerHandler(config_dict, int(id))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RaftServiceServicer_to_server(raft_service, server)

    

    ip_and_port = f'{config[1]}:{config[2]}'

    server.add_insecure_port(ip_and_port)
    server.start()

    try: 
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Termination')    





