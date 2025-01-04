from concurrent import futures
import re
import raft_pb2
import raft_pb2_grpc
import random
import sys
import time
import grpc
import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the fine-tuned GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained('./fine_tuned_gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('./fine_tuned_gpt2')
model.eval()

# Set the logit threshold for uncertainty detection
threshold = -180  # Adjust based on model behavior

# Keywords and exam date handling
required_keywords = ['aos', 'operating systems', 'grpc', 'algorithm', 'deadlock', 'exam', 'date','systems','operating']
exam_dates = {'midterm': 'October 15', 'final': 'December 10'}

# Directory to store uploaded files
UPLOAD_DIR = "uploads/"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Session token structure: {token: (username, expiration_time)}
tokens = {}
TOKEN_EXPIRATION_TIME = 1800  # Token expiration time in seconds (e.g., 30 minutes)

students = ["student1", "student2", "student3"]
instructor = "instructor"

# To store assignments: where key --> student's name and value --> filenames
student_assignments = {student: [] for student in students}
instructor_assignments = []

# Storing queries as {student_name: {"query": "student's query", "reply": "instructor's reply"}}
queries = {}

def is_token_valid(token):
    """Check if a session token is valid based on expiration time."""
    if token in tokens:
        username, expiration_time = tokens[token]
        if time.time() < expiration_time:  # Comparing the current time with expiration time
            return True
        else:
            # If expired remove token
            del tokens[token]
    return False


# Applies corresponding changes upon a term change event 
def invoke_term_change (term):
    global myLeaderId, votedId, timer, myState, myTerm

    if myState != "Follower" or term != myTerm:
        print(f"I am a follower. Term: {term}")

    timer = 0
    myTerm = term
    myLeaderId = -1
    votedId = -1
    myState = "Follower"

# Reads the list of servers from config.conf and saves the data to a global dictionary
def init_servers():
    global servers
    servers = {}

    with open("config.conf", "r") as f:
        for line in f:
            servers[int(line.split(" ")[0])] = f'{line.split(" ")[1]}:{line.split(" ")[2].rstrip()}'

# Initilizes global variables and copies over ID from command line arguments
def startup():
    global id, myTerm, timer, timerLimit, myState, votedId, servers, myLeaderId, suspended, globalPeriod, commitIndex, lastApplied, logs, myDict, nextIndex, matchIndex

    init_servers()

    id = int(sys.argv[1])
    suspended = False
    myDict = {}
    logs = []
    nextIndex = {}
    matchIndex = {}
    lastApplied = 0
    commitIndex = 0
    globalPeriod = 0
    myTerm = 0
    timer = 0
    timerLimit = random.randint(2000,5000) #100,300
    myState = "Follower"
    votedId = -1
    myLeaderId = -1
    
    print(f"The server starts at {servers[id]}")
    print("I am a follower. Term: 0")
    print("mytimer is",timerLimit)

# Responds to a RequestVote request from a candidate
def request_vote(term, candidateId, lastLogIndex, lastLogTerm):
    global votedId, myTerm, myState, logs

    if term > myTerm:
        myTerm = term
        votedId = -1

        return request_vote(term, candidateId, lastLogIndex, lastLogTerm)

    # If term < term number on this server, then reply False or if this server already voted on this term, then reply False.
    if term < myTerm or votedId != -1:
        return (myTerm, False)

    #If lastLogIndex < last log index of the server, then reply False
    if lastLogIndex < len(logs):
        return (myTerm, False)

    #If there is lastLogIndex entry on this server, and its term is not equal to lastLogTerm, then reply False.
    if lastLogIndex != 0 and logs[lastLogIndex - 1]["term"] != lastLogTerm:
        return (myTerm, False)

    votedId = candidateId
    myState = "Follower"

    print(f"Voted for node {candidateId}")
    print(f"I am a follower. Term: {myTerm}")

    return (myTerm, True)

# Receives a heartbeat from the leader
def append_entries(term, leaderId, prevLogIndex, prevLogTerm, entries, leaderCommit):
    global myTerm, myState, timer, myLeaderId, logs, commitIndex


    timer = 0

    if myTerm > term:
        return (myTerm, False)

    if prevLogIndex > len(logs):
        return (myTerm, False)

    entriesIndex = 0
    logsIndex = prevLogIndex

    while logsIndex < len(logs) and entriesIndex < len(entries):
        if logs[logsIndex] != entries[entriesIndex]:
            logs = logs[0:logsIndex]
            break

        logsIndex += 1
        entriesIndex += 1

    logs += entries[entriesIndex:]

    if leaderCommit > commitIndex:
        commitIndex = min(leaderCommit, prevLogIndex + len(entries))
    
    if term > myTerm:
        invoke_term_change(term)
    myLeaderId = leaderId

    return (myTerm, True)

# Responds to a GetLeader request from the client
def get_leader():
    global myLeaderId, votedId, servers

    print("Command from client: getleader")

    if myLeaderId != -1:
        print(f"{myLeaderId} {servers[myLeaderId]}")
        return (myLeaderId, servers[myLeaderId])

    if votedId != -1:
        print(f"{votedId} {servers[votedId]}")
        return (votedId, servers[votedId])

    print("None")
    return ("None", "None")

# Executes a Suspend command issued by the client
def suspend(period):
    global suspended, globalPeriod

    print(f"Command from client: suspend {period}")
    print(f'Sleeping for {period} seconds')

    suspended = True
    globalPeriod = period

# Executes a SetVal command issued by the client
def set_val(key, value):
    global logs

    if myState == "Candidate":
        return False
    
    if myState == "Leader":
        newEntry = {"term" : myTerm, "command" : f"{key} {value}"}
        logs.append(newEntry)
        return True
    
    channel = grpc.insecure_channel(servers[myLeaderId])
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.SetValRequest(key=key, value=value)
        response = stub.SetVal(params)
    except grpc.RpcError:
        return False

    return response.verdict

#===============================
#trying out
def sendsomething(key, value):
    global logs

    if myState == "Candidate":
        return False
    
    if myState == "Leader":
        newEntry = {"term" : myTerm, "command" : f"{key} {value}"}
        logs.append(newEntry)
        return True
    
    channel = grpc.insecure_channel(servers[myLeaderId])
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.sendsomethingproto(key=key, value=value)
        response = stub.SendSome(params)
    except grpc.RpcError:
        return False

    return response.verdict

def sendsomething1(key, value):
    global logs

    if myState == "Candidate":
        return False
    
    if myState == "Leader":
        newEntry = {"term" : myTerm, "command" : f"{key} {value}"}
        logs.append(newEntry)
        return True
    
    channel = grpc.insecure_channel(servers[myLeaderId])
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.sendsomethingproto1(key=key, value=value)
        response = stub.SendSome1(params)
    except grpc.RpcError:
        return False

    return response.verdict


# def nonsense(key, value):
#     global logs

#     if myState == "Candidate":
#         return False
    
#     if myState == "Leader":
#         newEntry = {"term": myTerm, "command": f"{key} {len(value)} bytes received"}
#         logs.append(newEntry)
#         # You may want to save the file somewhere
#         with open(f"{key}_received_file", "wb") as file:
#             file.write(value)
#         return True
    
#     channel = grpc.insecure_channel(servers[myLeaderId])
#     stub = raft_pb2_grpc.RaftServiceStub(channel)

#     try:
#         params = raft_pb2.nonsenserequest(key=key, value=value)  # Send binary data
#         response = stub.nonsenseservice(params)
#     except grpc.RpcError:
#         return False

def nonsense(key, value):
    global logs, myState, myTerm, myLeaderId, servers

    if myState == "Candidate":
        return False

    if myState == "Leader":
        # Leader handling the file and logging the command
        newEntry = {"term": myTerm, "command": f"{key} {len(value)} bytes received"}
        logs.append(newEntry)
        
        # Save the file to the server with an appropriate filename
        try:
            with open(f"{key}_received_file", "wb") as file:
                file.write(value)
            print(f"File received and saved as {key}_received_file")
            return True
        except Exception as e:
            print(f"Failed to write the file: {e}")
            return False

    else:
        # If not a leader, forward the request to the leader
        channel = grpc.insecure_channel(servers[myLeaderId])
        stub = raft_pb2_grpc.RaftServiceStub(channel)

        try:
            # Forward the file and key to the leader
            params = raft_pb2.nonsenserequest(key=key, value=value)  # Send binary data
            response = stub.nonsenseservice(params)

            # Forward leader's response back to the client
            return response.verdict
        except grpc.RpcError as e:
            print(f"Error forwarding to leader: {e.details()}")
            return False





# Executes a GetVal command issued by the client
def get_val(key):

    if key not in myDict:
        return (False, "None")
    
    return (True, myDict[key])

#================================
#dont 

def get_something_rajiv(key):

    if key not in myDict:
        return (False, "None")
    
    return (True, myDict[key])

def get_something_rajiv1(key):

    if key not in myDict:
        return (False, "None")
    
    return (True, myDict[key])



# Applies the necessary immediate changes upon turning into a leader.
def handle_leader_init():
    global myState, myLeaderId, nextIndex, matchIndex

    myState = "Leader"
    print(f"I am a leader. Term: {myTerm}")
    myLeaderId = id
    nextIndex = {}
    matchIndex = {}

    for key in servers:

        if key == id:
            continue
        
        nextIndex[key] = commitIndex + 1
        matchIndex[key] = 0


# Applies the necessary immediate changes upon turning into a candidate
# Sends RequestVote requests to other nodes, and decides whether or not to turn into the leader
def handle_candidate_init():
    global timer, id, myTerm, myState, votedId, myLeaderId

    print("The leader is dead")

    timer = 0
    
    invoke_term_change(myTerm + 1)
    
    myState = "Candidate"
    
    print(f"I am a candidate. Term: {myTerm}")
    
    vote_count = 1
    votedId = id
    
    print(f"Voted for node {id}")
    
    for key in servers:

        if key == id:
            continue
        try:
            address = servers[key]

            channel = grpc.insecure_channel(address)
            stub = raft_pb2_grpc.RaftServiceStub(channel)
            candidate = raft_pb2.TermCandIDPair(term=myTerm, candidateID=id)
            lastLogTerm = 0
            if len(logs) != 0:
                lastLogTerm = logs[-1]["term"]
            params = raft_pb2.RequestVoteRequest(candidate=candidate, lastLogIndex=len(logs), lastLogTerm=lastLogTerm)
            response = stub.RequestVote(params)

            term, result = response.result.term, response.result.verdict

        except grpc.RpcError:
            continue
        
        if term > myTerm:

            invoke_term_change(term)

            return

        vote_count += (result == True)

    print("Votes received")

    if (vote_count >= len(servers)/2 + 1):
        handle_leader_init()

# Handles the follower state
def handle_follower():
    global myState, timer, timerLimit

    if timer >= timerLimit:
        handle_candidate_init()

# Handles the candidate state
def handle_candidate():
    global timer, timerLimit, myState, logs

    if timer >= timerLimit:
        timerLimit = random.randint(150, 300)
        invoke_term_change(myTerm)

# Extracts a log entry from a ProtoBuf LogEntry message
def extract_log_entry_message(entry):
    return {'term' : entry.term, 'command' : entry.command}

# Forms a log entry into a ProtoBuf LogEntry message
def form_log_entry_message(entry):
    return raft_pb2.LogEntry(term=entry['term'], command=entry['command'])

# Handles the leader state
# Sends heartbeats every 50ms
def handle_leader():
    global timer, myTerm, id, commitIndex, nextIndex, matchIndex, logs

    if timer % 50 == 0:
        
        # Resets the timer to avoid overflowing in an infinite leader state
        # Applicable since the leader does not care about the timer limit
        timer = 0

        for key in servers:
            
            if key == id:
                continue

            while True:
                try:
                    # Sending an AppendEntries request

                    address = servers[key]
                    channel = grpc.insecure_channel(address)
                    stub = raft_pb2_grpc.RaftServiceStub(channel)
                    prevLogIndex = nextIndex[key] - 1
                    prevLogTerm = 0
                    if len(logs) != 0 and prevLogIndex != 0:
                        prevLogTerm = logs[prevLogIndex - 1]['term']
                    
                    paramEntries = [form_log_entry_message(x) for x in logs[prevLogIndex:]]
                    leader = raft_pb2.TermLeaderIDPair(term=myTerm, leaderID=id)
                    params = raft_pb2.AppendEntriesRequest(leader=leader, prevLogIndex=prevLogIndex, prevLogTerm=prevLogTerm, leaderCommit=commitIndex)
                    params.entries.extend(paramEntries)
                    response = stub.AppendEntries(params)

                    term, result = response.result.term, response.result.verdict
                        
                except grpc.RpcError:
                    break
                
                # If successful: update nextIndex and matchIndex for the follower.
                if result == True:
                    nextIndex[key] = matchIndex[key] = prevLogIndex + len(paramEntries) + 1
                    matchIndex[key] -= 1
                    nextIndex[key] = max(nextIndex[key], 1)
                    break
                
                # If, as a result of calling this function, the Leader receives a term number greater than its own term number
                # that Leader must update his term number and become a Follower
                if term > myTerm:
                    invoke_term_change(term)
                    return

                # If AppendEntries fails because of log inconsistency: decrement nextIndex and retry.
                nextIndex[key] -= 1
                if nextIndex[key] == 0:
                    nextIndex[key] = 1
                    break
    
        while commitIndex < len(logs):
            newCommitIndex = commitIndex + 1
            validServers = 1
            
            for key in matchIndex:
                if matchIndex[key] >= newCommitIndex:
                    validServers += 1

            if validServers >= len(servers)/2 + 1:
                commitIndex = newCommitIndex
            else:
                break

# If commitIndex > lastApplied: increment lastApplied and apply log[lastApplied] to state machine.
def apply_commits():
    global myDict, lastApplied

    while lastApplied < commitIndex:
        command = logs[lastApplied]['command'].split(' ')
        myDict[command[0]] = command[1]

        lastApplied += 1

# Terminates the server
def terminate():
    print(f"Server {id} is shutting down...")
    sys.exit(0)

# Handles current state
def handle_current_state():
    apply_commits()
    if myState == "Follower":
        handle_follower()
    if myState == "Candidate":
        handle_candidate()
    elif myState == "Leader":
        handle_leader()

# Initializes the server, and makes appropriate handle_current_state calls every 1ms
def main_loop():
    global timer, suspended

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_RaftServiceServicer_to_server(RaftService(), server)
    server.add_insecure_port(servers[id])
    server.start()

    while True:

        if suspended:
            server.stop(0)
            time.sleep(globalPeriod)
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            raft_pb2_grpc.add_RaftServiceServicer_to_server(RaftService(), server)
            server.add_insecure_port(servers[id])
            server.start()
            suspended = False

        init_servers()
        handle_current_state()

        time.sleep(0.001)
        timer += 1


class RaftService(raft_pb2_grpc.RaftServiceServicer):
    def RequestVote(self, request, context):
        term = request.candidate.term
        candidate_id = request.candidate.candidateID
        last_log_index = request.lastLogIndex
        last_log_term = request.lastLogTerm

        voted = request_vote(term, candidate_id, last_log_index, last_log_term)

        result = raft_pb2.TermResultPair(term=voted[0], verdict=voted[1])

        response = raft_pb2.RequestVoteResponse(result=result)

        return response
    
    def AppendEntries(self, request, context):
        term = request.leader.term
        leader_id = request.leader.leaderID
        prev_log_index = request.prevLogIndex
        prev_log_term = request.prevLogTerm
        
        entries = []

        for entry in request.entries:
            entries.append(extract_log_entry_message(entry))

        leader_commit = request.leaderCommit

        appended = append_entries(term, leader_id, prev_log_index, prev_log_term, entries, leader_commit)

        result = raft_pb2.TermResultPair(term=appended[0], verdict=appended[1])

        response = raft_pb2.AppendEntriesResponse(result=result)

        return response

    def GetLeader(self, request, context):
        leader = get_leader()

        if leader[0] == "None":
            response = raft_pb2.GetLeaderResponse(nodeId=-1)
        
        else:
            response = raft_pb2.GetLeaderResponse(nodeId=leader[0], nodeAddress=leader[1])
        
        return response
    
    def Suspend(self, request, context):
        period = request.period

        suspend(period)

        return raft_pb2.Empty()
    
    def SetVal(self, request, context):
        key = request.key
        value = request.value

        set = set_val(key, value)
        response = raft_pb2.SetValResponse(verdict=set) 
        return response
    
    def login(self, request, context):
        if request.username in students and request.password == "pass":
            token = f"{request.username}_token"
            expiration_time = time.time() + TOKEN_EXPIRATION_TIME  # Setting the expiration time for the session
            tokens[token] = (request.username, expiration_time)
            return raft_pb2.LoginResponse(status="success", token=token)
        elif request.username == instructor and request.password == "pass":
            token = "instructor_token"
            expiration_time = time.time() + TOKEN_EXPIRATION_TIME
            tokens[token] = (request.username, expiration_time)
            return raft_pb2.LoginResponse(status="success", token=token)
        else:
            return raft_pb2.LoginResponse(status="failure", token="")

    def logout(self, request, context):
        token = request.token
        if token in tokens:
            del tokens[token]  # Remove token after logging out
            return raft_pb2.LogoutResponse(status="success")
        return raft_pb2.LogoutResponse(status="failure")

    def uploadFile(self, request, context):
        if not is_token_valid(request.token):  # Check if token is valid or not
            return raft_pb2.UploadResponse(status="failure")

        user, _ = tokens[request.token]  # Retrieve user from token
        file_path = os.path.join(UPLOAD_DIR, request.filename)

        with open(file_path, 'wb') as f:
            f.write(request.content)

        if user in students:
            student_assignments[user].append(request.filename)
        elif user == instructor:
            instructor_assignments.append(request.filename)

        print(f"File {request.filename} uploaded by {user}.")
        return raft_pb2.UploadResponse(status="success")


    def downloadFile(self, request, context):
        if not is_token_valid(request.token):
            return raft_pb2.DownloadResponse(status="failure", content=b"")

        file_path = os.path.join(UPLOAD_DIR, request.filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                file_content = f.read()
            return raft_pb2.DownloadResponse(status="success", content=file_content)
        else:
            return raft_pb2.DownloadResponse(status="failure", content=b"")
        

    def getAssignments(self, request, context):
        if not is_token_valid(request.token):
            return raft_pb2.GetResponse(status="failure", assignments=[])

        user, _ = tokens[request.token]

        if user == instructor:
            assignments = []
            for student, files in student_assignments.items():
                for file in files:
                    assignments.append(f"{student}: {file}")
            return raft_pb2.GetResponse(status="success", assignments=assignments)

        elif user in students:
            return raft_pb2.GetResponse(status="success", assignments=instructor_assignments)

        return raft_pb2.GetResponse(status="failure", assignments=[])
    

    def askQuery(self, request, context):
        if not is_token_valid(request.token):
            return raft_pb2.QueryResponse(status="failure", reply="")

        student, _ = tokens[request.token]
        if student in students:
            queries[student] = {"query": request.query, "reply": ""}
            print(f"Query from {student}: {request.query}")
            return raft_pb2.QueryResponse(status="success", reply="Query sent to instructor.")
        return raft_pb2.QueryResponse(status="failure", reply="")

    def getQueries(self, request, context):
        if not is_token_valid(request.token):
            return raft_pb2.QueryListResponse(status="failure", queries=[])

        user, _ = tokens[request.token]

        if user == instructor:
            query_list = [f"{student}: Query: {info['query']}, Reply: {info['reply']}" 
                      for student, info in queries.items()]
            return raft_pb2.QueryListResponse(status="success", queries=query_list)

        elif user in students:
            if user in queries:
                query_info = f"Your query: {queries[user]['query']}, Reply: {queries[user]['reply'] or 'No reply yet.'}"
                return raft_pb2.QueryListResponse(status="success", queries=[query_info])
            else:
                return raft_pb2.QueryListResponse(status="failure", queries=[])

        return raft_pb2.QueryListResponse(status="failure", queries=[])

    
    def replyQuery(self, request, context):
        if not is_token_valid(request.token):
            return raft_pb2.ReplyQueryResponse(status="failure")

        user, _ = tokens[request.token]
        if user == instructor and request.student in queries:
            queries[request.student]["reply"] = request.reply
            print(f"Instructor replied to {request.student}'s query: {request.reply}")
            return raft_pb2.ReplyQueryResponse(status="success")
        return raft_pb2.ReplyQueryResponse(status="failure")

    # checking of keywords
    def check_keywords(self,input_text, keywords):
        """Check if any of the required keywords are present in the input text."""
        for keyword in keywords:
            if re.search(rf'\b{keyword}\b', input_text, re.IGNORECASE):
                return True
        return False
    
    # checking of exam dates
    def check_for_exam_dates(self,input_text):
        """Check if query is about exam dates."""
        if 'exam' in input_text.lower() and ('when' in input_text.lower() or 'date' in input_text.lower()):
            return True
        return False

    # return if the exam dates are available
    def get_exam_date(self,exam_type):
        """Return the exam date if available."""
        return exam_dates.get(exam_type.lower(), "The exam schedule will be shared by the course instructor.")

    def gptQuery(self, request, context):
        if not is_token_valid(request.token):
            return raft_pb2.GPTQueryResponse(status="failure", response="")

        student, _ = tokens[request.token]
        if student in students:
            query = request.query
            # if there are no such keywords in the questions asked by students then llm model shouldnt reply of the question asked
            if not self.check_keywords(query, required_keywords):
                
                return raft_pb2.GPTQueryResponse(status="success", response="Please consult the course instructor; I can't be of help.")
            
        # Check for specific exam-related queries and provide dates
            if self.check_for_exam_dates(query):
                if 'midterm' in query.lower():
                    x10="The midterm exam is scheduled for :"+self.get_exam_date('midterm')
                    return raft_pb2.GPTQueryResponse(status="success", response=x10)
                elif 'final' in query.lower():
                    x10="The final exam is scheduled for :"+self.get_exam_date('final')
                    return raft_pb2.GPTQueryResponse(status="success", response=x10)
                else:
                    return raft_pb2.GPTQueryResponse(status="success", response="The exam schedule will be shared by the course instructor.")
            

        # Tokenize and generate a response using GPT-2
        full_prompt = f"Q: {query}\nA:"  
        inputs = tokenizer.encode(full_prompt, return_tensors='pt', truncation=True, max_length=1024 - 50)
        attention_mask = torch.ones(inputs.shape, dtype=torch.long)

        outputs = model.generate(
            inputs,
            max_new_tokens=150,  
            do_sample=True, 
            temperature=0.85,  
            top_k=50, 
            top_p=0.9,  
            pad_token_id=tokenizer.eos_token_id, 
            attention_mask=attention_mask,
            output_scores=True,  
            return_dict_in_generate=True
        )

        generated_text = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
        logits = outputs.scores

        # Calculate the average of max logits to determine confidence
        max_logits = [torch.max(logit).item() for logit in logits]
        avg_logit_score = torch.mean(torch.tensor(max_logits)).item()

        #print("Average Max Logit Score:", avg_logit_score)

        # Uncertainty check based on the threshold
        is_uncertain = avg_logit_score < threshold

        # Provide fallback if model is uncertain
        if is_uncertain or "I am not sure" in generated_text or len(generated_text.strip()) == 0:
            return raft_pb2.GPTQueryResponse(status="success", response="Ask the instructor, I am not sure about the answer.")
        else:
            return raft_pb2.GPTQueryResponse(status="success", response="Generated Response:\n"+generated_text)

            # Print the final output
    

            
        return raft_pb2.GPTQueryResponse(status="failure", response="")
    
    #added
    def nonsenseservice(self, request, context):
        key = request.key  # Get the file name
        value = request.value  # Get the binary content of the file
        
        # Log the received request
        print(f"nonsenseservice received a request with key: {key} and file size: {len(value)} bytes")

        # Call the local `nonsense` function that handles file storage and forwarding to the leader
        success = nonsense(key, value)

        # Prepare and return the response
        response = raft_pb2.nonsenseresponse(verdict=success)
        return response
    

#=====================
#just dont ask
    def SendSome(self, request, context):
        key = request.key
        value = request.value

        set = sendsomething(key, value)
        response = raft_pb2.sendresponse(verdict=set) 
        return response
    
    def SendSome1(self, request, context):
        key = request.key
        value = request.value

        set = sendsomething1(key, value)
        response = raft_pb2.sendresponse1(verdict=set) 
        return response



    def GetVal(self, request, context):
        key = request.key

        get = get_val(key) 
        response = raft_pb2.GetValResponse(verdict=get[0], value=get[1])
        return response
    
#==========================
#====================
    def getsome(self, request, context):
        key = request.key

        get = get_something_rajiv(key) 
        response = raft_pb2.getrajivResponse(verdict=get[0], value=get[1])
        return response
    
    def getsome1(self, request, context):
        key = request.key

        get = get_something_rajiv1(key) 
        response = raft_pb2.getrajivResponse1(verdict=get[0], value=get[1])
        return response
    
#get taht something
    def GetVal(self, request, context):
        key = request.key

        get = get_val(key) 
        response = raft_pb2.GetValResponse(verdict=get[0], value=get[1])
        return response
    
    # def nonsenseservice(self, request, context):
    #     key = request.key
    #     value = request.value

    #     set = set_val(key, value)
    #     response = raft_pb2.SetValResponse(verdict=set) 
    #     return response
    def nonsenseservice(self, request, context):
        key = request.key  # Get the file name
        value = request.value  # Get the binary content of the file
        
        # Log the received request
        print(f"nonsenseservice received a request with key: {key} and file size: {len(value)} bytes")

        # Call the local `nonsense` function that handles file storage and forwarding to the leader
        success = nonsense(key, value)

        # Prepare and return the response
        response = raft_pb2.nonsenseresponse(verdict=success)
        return response




def init():
    try:
        startup()
        main_loop()
    except KeyboardInterrupt:
        terminate()

init()


# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     lms_pb2_grpc.add_LMSServicer_to_server(LMSService(), server)
#     #server.add_insecure_port('192.168.172.232:50051')
#     server.add_insecure_port('[::]:50051')
#     print("Server started on port 50051.")
#     server.start()
#     server.wait_for_termination()


# if __name__ == '__main__':
#     serve()
