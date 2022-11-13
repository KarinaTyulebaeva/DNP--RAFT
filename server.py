import threading
import grpc
import raft_pb2_grpc as pb2_grpc
import raft_pb2 as pb2
import sys
from concurrent import futures
import random
from threading import Timer
import math
import time

import log_pb2 as log_pb2
import log_pb2_grpc as log_pb2_grpc

class RaftServerHandler(pb2_grpc.RaftService):
    def __init__(self, config_dict, id):
        self.term = 0
        self.state = "follower"

        print(f'I am a follower. Term: {self.term}')
        
        self.log("стал фолловером")

        self.timer = None
        self.timer_count = random.randint(150, 300)

        self.config_dict = config_dict
        self.config_dict['leader'] = None
        self.heartbeat = 50
        self.id = id
        self.votes = 0
        self.restart_timer(self.become_candidate)

        self.voted = False

        self.election_period = False
        self.voted_for = None

    def init_timer(self):
        self.timer_count = random.randint(150, 300)    

    def restart_timer(self, function):
        self.timer = Timer(self.timer_count, function)  
        self.timer.start() 

    def update_term(self, n):
        self.term = n
        self.voted = False 

    def send_heartbeat(self, id_and_port):
        new_channel = grpc.insecure_channel(ip_and_port)
        new_stub = pb2_grpc.RaftServiceStub(new_channel)

        msg = {"term": self.term, "leaderId": self.id}
        
        request_vote_response = new_stub.AppendEntries(**msg)
        if(request_vote_response.result == False):
            self.update_term()
            self.state = "follower"
            print(f'I am a follower. Term: {self.term}')
            
            self.log("стал фолловером")

    def leader_duty(self, n):
        while self.state == "leader":
            hb_threads = []
            for id, ip_and_port in self.config_dict:
                if(id != 'leader'):
                    hb_threads.append(threading.Thread(target=self.send_heartbeat, args=(ip_and_port)))
            [t.start() for t in hb_threads]
            [t.join() for t in hb_threads]
            time.sleep(50)
            

    def check_votes(self):
        print('Votes received')
        # закончили голосование
        self.election_period = False
        # затираем голос
        self.voted_for = None

        self.log(f"votes: {self.votes}")

        if self.state != 'candidate':
            return
        if(self.votes >= math.floor((len(self.config_dict)-1)/2)):
            self.state = 'leader'

            print(f'I am a leader. Term: {self.term}')

            self.log("стал лидером")

            # Вот тут мы вызываем вечную функцию лидера которая шлет сердцебиения
            self.leader_thread = threading.Thread(target=self.leader_duty)
            self.leader_thread.start()
        else:
            self.state = 'follower'

            print(f'I am a follower. Term: {self.term}')
            self.log("стал фолловером")

            self.init_timer()
            self.restart_timer(self.become_candidate)

    def get_vote(self, ip_and_port):
        new_channel = grpc.insecure_channel(ip_and_port)
        new_stub = pb2_grpc.RaftServiceStub(new_channel)

        msg = {"term": self.term, "candidateId": self.id}
        request_vote_response = new_stub.RequestVote(**msg)

        if(request_vote_response.result == True):
            self.votes+=1

    def become_candidate(self):
        self.update_term(1)
        self.state = 'candidate' 

        print(f'I am a candidate. Term: {self.term}')
        self.log("стал кандидатом")

        self.restart_timer(self.check_votes)
        self.votes = 1
        self.voted = True

        # начали выборы (останавливаю их в функции check_votes, хз нужно ли тут тоже это делать)
        self.election_period = True
        # проголосовали за себя любимого
        self.voted_for = self.id
        vote_threads = []
        for id, ip_and_port in self.config_dict:
            if(id != 'leader'):
                vote_threads.append(threading.Thread(target=self.get_vote, args=(ip_and_port)))
        [t.start() for t in vote_threads]


    def reset_votes(self):
        self.votes = 0

    def RequestVote(self, request, context):
        # снова начались выборы
        self.election_period = True
        self.timer.restart()
        
        # follower
        if(self.state == 'follower'):
            if(request.term == self.term):
                self.voted = True
                self.voted_for = request.candidateId
                print(f'Voted for node {self.voted_for}')
                reply = {"term": self.term, "result": True}
                return pb2.RequestVoteResponse(**reply)
            elif(request.term > self.term):
                self.update_term(request.term)
                self.voted = True 
                self.voted_for = request.candidateId 
                print(f'Voted for node {self.voted_for}')

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

                print(f'I am a follower. Term: {self.term}')
                self.log("стал фолловером")

                self.voted = True
                self.voted_for = request.candidateId
                print(f'Voted for node {self.voted_for}')

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
                self.voted_for = request.candidateId 
                print(f'Voted for node {self.voted_for}')

                reply = {"term": self.term, "result": True}
                return pb2.RequestVoteResponse(**reply)

            else:
                reply = {"term": self.term, "result": False}
                return pb2.RequestVoteResponse(**reply) 

        # голосование закончилось
        self.election_period = False        
        self.voted_for = None   

    def AppendEntries(self, request, context):
        self.timer.restart()

        if(request.term >= self.term):
            # Потому что if the Candidate receives the message (any message) with the term number greater than its own, it stops the election and becomes a Follower
            # Или if the Leader receives a heartbeat message from another Leader with the term number greater than its own, it becomes a Follower 
            self.state = 'follower'
            print(f'I am a follower. Term: {self.term}')

            self.log("стал фолловером")

            self.config_dict['leader'] = request.leaderId
            self.update_term(request.term)

            reply = {"term": self.term, "success": True}
            return pb2.AppendEntriesResponse(**reply)
        else:
            reply = {"term": self.term, "success": False}
            return pb2.AppendEntriesResponse(**reply)    

    def GetLeader(self, request, context):
        self.timer.restart()

        if(self.state == "sleeping"):
            return self.get_leader_response(-1, "Server is suspending")
        else:    
            if(self.election_period):
                if(self.voted_for != None):
                    return self.get_leader_response(-1, "There is election now and server did not voted yet")
                else:
                    return self.get_leader_response(self.voted_for, self.config_dict[str(self.voted_for)])

            else:
                leader_id = self.config_dict['leader']
                return self.get_leader_response(int(leader_id), self.config_dict[leader_id])

    def get_leader_response(self, leader_id: int, address: str):
        msg = {"leaderId": leader_id, "address": address}
        return pb2.GetLeaderResponse(**msg)        

    def Suspend(self, request, context):    
        if(self.state == "sleeping"):
            msg = {"message": "Alredy suspending"}   
            return pb2.SuspendResponse(**msg)
            
        else:        
            self.timer.restart()

            print(f'{self.state} is dead')

            prev_state = self.state
            self.state = "sleeping"
            time.sleep(1000*request.period)
            self.state = prev_state
    

    def log(self, message):
        log_channel = grpc.insecure_channel(f'127.0.0.1:5555')
        log_stub = log_pb2_grpc.LogServiceStub(log_channel)
        msg = {"log": f'{self.id}  {message}  at term {self.term}'}    
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
    print(f'The server starts at {ip_and_port}')

    try: 
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Termination')    
