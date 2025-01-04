import grpc
import raft_pb2
import raft_pb2_grpc
import sys
import os
import threading
import time
#import server


global user_type
queryidea = []
# Here downloaded files are saved
DOWNLOAD_DIR = "downloads/"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Session timeout (in seconds)
SESSION_TIMEOUT = 6000

# Global variable to tracking the timer thread
session_timer = None

def reset_session_timer(stub, token):
    global session_timer

    def session_timeout():
        print("Session expired due to inactivity.")
        # Automatically log out the user when the session expires after some time
        if token:
            response = stub.logout(raft_pb2.LogoutRequest(token=token))
            print(f"Logout status: {response.status}")
        exit(0)

    # Cancel any existing timer and start a new one
    if session_timer:
        session_timer.cancel()

    session_timer = threading.Timer(SESSION_TIMEOUT, session_timeout)
    session_timer.start()

def upload_file(stub, token):
    reset_session_timer(stub, token)  # Reseting the session timer again
    file_path = input("Enter the path of the file to upload: ")
    nonsense(file_path)
    filename = os.path.basename(file_path)

    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        response = stub.uploadFile(raft_pb2.UploadRequest(token=token, filename=filename, content=file_content))
        print(f"Upload status: {response.status}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")

def download_file(stub, token, filename):
    reset_session_timer(stub, token)  # Reseting the session timer again
    response = stub.downloadFile(raft_pb2.DownloadRequest(token=token, filename=filename))

    if response.status == "success":
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"File {filename} downloaded to {file_path}")
    else:
        print(f"Download failed for {filename}.")

# Remaining functions would also have reset_session_timer(stub, token) added similarly


# Function to get assignments

def get_assignments(stub, token, user_type):
    response = stub.getAssignments(raft_pb2.GetRequest(token=token, type=user_type))

    if response.status == "success":
        print("Assignments available:")
        for assignment in response.assignments:
            print(assignment)
        
        filename = input("Enter the filename to download: ")
        download_file(stub, token, filename)
    else:
        print("Failed to retrieve assignments.")

#def grade_assignments(stub, token, user_type):
def grade_assignments(stub, token):
    #print("enter name of student and marks ")
    print("         This is for grading students         ")
    name1=input("enter name of student:  ")
    marks1=input("enter marks for student:  ")
    set_val(name1,marks1)

def get_grades(stub, token):
    name1=input("enter name of student:  ")
    get_val(name1)



# Function to allow a student to submit a query
def ask_query(stub, token):
    query = input("Enter your query: ")
    response = stub.askQuery(raft_pb2.QueryRequest(token=token, query=query))
    print(f"Query status: {response.status}, Reply: {response.reply}")

# Function for the faculty to view all the queries which are submitted by students
def view_queries(stub, token):
    response = stub.getQueries(raft_pb2.QueryListRequest(token=token))

    # If the request is successful, display all the queries
    if response.status == "success":
        print("Queries received by instructor:")
        for query in response.queries:
            print(query)
        
        student = input("Enter the student's name to reply to their query: ")
        reply = input("Enter your reply: ")
        reply_query(stub, token, student, reply)
    else:
        print("Failed to retrieve queries.")

# Faculty can reply to a student's query
def reply_query(stub, token, student, reply):
    response = stub.replyQuery(raft_pb2.ReplyQueryRequest(token=token, student=student, reply=reply))
    
    print(f"Reply status: {response.status}")

# Student can check the status of their submitted queries
def check_student_query_status(stub, token):
    response = stub.getQueries(raft_pb2.QueryListRequest(token=token))
  
    if response.status == "success":
        for query_info in response.queries:
            print(query_info)
    else:
        print("Failed to retrieve your queries.")

# Function to ask a question to the GPT model and receive response
def ask_gpt_query(stub, token):
    query = input("Enter your question for GPT: ")
    
    response = stub.gptQuery(raft_pb2.GPTQueryRequest(token=token, query=query))
    
    # If the request is successful, display the GPT response
    if response.status == "success":
        print(f"GPT Response: {response.response}")
    else:
        print("Failed to get response from GPT.")

def nonsense(file_path):
    # Ensure you are connected to the leader
    if not connect_to_leader():
        print("Failed to connect to leader.")
        return

    # Read the file in binary mode
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
        #print("checkpoint -1")
        channel = grpc.insecure_channel(server_ip_addr_port_num)
        #print("checkpoint -2")
        stub = raft_pb2_grpc.RaftServiceStub(channel)
        #print("checkpoint -3")
        # Use the file name as key and binary content as value
        params = raft_pb2.nonsenserequest(key=file_path, value=file_content)
        #print("checkpoint -5")
        response = stub.nonsenseservice(params)
        #print("checkpoint -4")
        if response.verdict:
            print("File sent successfully.")
        else:
            print("Failed to send the file.")
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except grpc.RpcError:
        server_failure()

def run():
    global session_timer
    
    #with grpc.insecure_channel('192.168.172.232:50051') as channel:
    with grpc.insecure_channel(server_ip_addr_port_num) as channel:
        stub = raft_pb2_grpc.RaftServiceStub(channel)

        token = None

        while True:
            print("\nOptions:")
            print("1. Login")
            print("2. Upload File")
            print("3. Get Assignments")
            print("4. Ask Query")
            print("5. View/Reply to Queries (Instructor)")
            print("6. Check Query Status (Student)")
            print("7. Ask GPT Query") 
            print("8. Logout")
            print("9. Assign grades for Student")
            print("10. View Grades ")
            print("11. Exit")
            
        

            option = input("Select an option: ")

            if option == "1":
                username = input("Username: ")
                password = input("Password: ")
                response = stub.login(raft_pb2.LoginRequest(username=username, password=password))
                print(f"Login status: {response.status}, Token: {response.token}")
                if response.status == "success":
                    token = response.token
                    reset_session_timer(stub, token)  # Start session timer after loging in successfully.

            elif option == "2":
                if token:
                    #upload_file(stub, token)
                    #if student uploads file it should be visible to instructor
                    #this is related to student
                    name=token+'file.txt'
                    filedata=input("enter contents into file:   ")
                    sendsomething(name,filedata)

                    current_directory ="uploads/"
                    #current_directory
                    file_path = os.path.join(current_directory, name)#here name refers to file name
                    # if not file_path.endswith(".txt"):
                    #     file_path += ".txt"
                    try:
                        with open(file_path, 'w') as file:
                            file.write(filedata)
                        print(f"File created successfully at: {file_path}")
                    except IOError as e:
                        print(f"Error writing to file: {e}")

                else:
                    print("You must log in first!")

            elif option == "3":
                if token:
                    #user_type = "instructor" if "instructor" in token else "student"
                    
                    if "instructor" in token:
                        #user_type = "instructor"
                        #now i am instructor i want to see  file uploaded by student
                        name=input("enter name of student whose file you want to view:  ")
                        name=name+'_token'+'file.txt'
                    else:
                        user_type = "student"
                        # now i have to view files uploaded by instructor
                        name='instructor_token'+'file.txt'

                    current_directory ="downloads/"
                    #current_directory
                    file_path = os.path.join(current_directory, name)#here name refers to file name
                    
                    #get_assignments(stub, token, user_type)
                    #here i fetch value using function
                    poo=get_something_rajiv(name)
                    print("-------")
                    with open(file_path, "w") as file:

                        file.write(str(poo))
                    print("SUCCESS, Check File in Downloads Folder")
                    print("-------")


                else:
                    print("You must log in first!")

            elif option == "4":
                if token:
                    #ask_query(stub, token)
                    name=token
                    queryidea.append(name)
                    print("---------")
                    print(name)
                    print("---------")
                    name=name+'q'
                    query = input("Enter your query: ")
                    sendsomething(name,query)
                else:
                    print("You must log in first!")

            elif option == "5":
                if token and "instructor" in token:

                    #view_queries(stub, token)

                    #queryidea---- print those names 
                    print(queryidea)
                    name=input("enter name of student you want to answer")
                    name=name+'_token'+'q' #for viewing question raised by student
                    get_something_rajiv1(name) #gets the question sent by student
                    name=name+'a'
                    ans=input("enter the reply to query")
                    sendsomething1(name,ans)
                    
                else:
                    print("You must log in as instructor to view/reply to queries!")

            elif option == "6":
                if token and "student" in token:
                    #check_student_query_status(stub, token)

                    name=token
                    # i want question so go with 'q'
                    name1=name+'q'
                    
                    get_something_rajiv1(name1)# this is used to get the question
                    # now i want ot fetch the answer
                    #so go with qa
                    name2=name+'qa'
                    
                    get_something_rajiv1(name2)# this is used to get the answer
                else:
                    print("You must log in as a student to check query status!")

            elif option == "7":
                if token and "student" in token:
                    ask_gpt_query(stub, token)
                else:
                    print("Only students can access GPT.")

            elif option == "8":
                if token:
                    response = stub.logout(raft_pb2.LogoutRequest(token=token))
                    print(f"Logout status: {response.status}")
                    if session_timer:
                        session_timer.cancel()  # Stoping the timer on logout
                    token = None
                else:
                    print("You are not logged in.")

            elif option == "11":
                if session_timer:
                    session_timer.cancel()  # Stoping the timer on exit
                break
            elif option == "9":
                if token and "instructor" in token:
                    #grade_assignments(stub, token, user_type)
                    grade_assignments(stub, token)
                else:
                    print("instructor must log in first!")

                # if token:
                #     user_type = "instructor" if "instructor" in token else "student"
                #     grade_assignments(stub, token, user_type)
                # else:
                #     print("instructor must log in first!")

            elif option == "10":
                if token and "student" in token:
                    get_grades(stub, token)
                else:
                    print("Only logged in  students can view grades ")
            

# The IP address and port number of the server to which commands will be issued
global server_ip_addr_port_num 
#server_ip_addr_port_num = ""
# global server_ip_addr_port_num

# Print a message in case the current server is offline
def server_failure():
    print(f"The server {server_ip_addr_port_num} is unavailable")
    return

# Parse user input from command line
def parse_user_input(message):
    command = message.split(" ")[0]
    parsed_message = message.split(" ")

    if command == "connect":
        return ("Connect", parsed_message[1])
    
    elif command == "getleader":
        return ("GetLeader", "GetLeader")
    elif command == "suspend":
        return ("Suspend", int(parsed_message[1]))
    elif command == "setval":
        return ("SetVal", parsed_message[1], parsed_message[2])
    elif command == "getval":
        return ("GetVal", parsed_message[1])
    elif command == "quit":
        return ("Quit", "quit")
    elif command == "send":
        return ("send", parsed_message[1], parsed_message[2])
    elif command == "needed":
        return ("needed", parsed_message[1])
    elif command=="nonsense":
        return ("nonsense",parsed_message[1])
        
    elif command=="lms":
        return ("lms","lms")
    else:
        return ("Invalid", "invalid")

# Set the global server variable to the provided one
def connect(ip_addr_port_num):

    global server_ip_addr_port_num

    server_ip_addr_port_num = ip_addr_port_num

# Issue a GetLeader command to the server
def get_leader():
    channel = grpc.insecure_channel(server_ip_addr_port_num)
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.Empty()
        response = stub.GetLeader(params)
    except grpc.RpcError:
        server_failure()
        return

    if response.nodeId == -1:
        print("No leader. This node hasn't voted for anyone in this term yet...")
    
    else:
        print(f"{response.nodeId} {response.nodeAddress}")

# Issue a Suspend command to the server
def suspend(period):
    channel = grpc.insecure_channel(server_ip_addr_port_num)
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.SuspendRequest(period=period)
        response = stub.Suspend(params)
    except grpc.RpcError:
            server_failure()
            return

# Issue a SetVal command to the server
def set_val(key, value):
    channel = grpc.insecure_channel(server_ip_addr_port_num)
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.SetValRequest(key=key, value=value)
        response = stub.SetVal(params)
    except grpc.RpcError:
            server_failure()
            return
#=========================
# i have no idea
def sendsomething(key,value):
    channel = grpc.insecure_channel(server_ip_addr_port_num)
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.sendsomethingproto(key=key, value=value) # this should be of type message
        response = stub.SendSome(params)                              # this should be of type rpc
    except grpc.RpcError:
            server_failure()
            return

    return

def sendsomething1(key,value):
    channel = grpc.insecure_channel(server_ip_addr_port_num)
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.sendsomethingproto1(key=key, value=value) # this should be of type message
        response = stub.SendSome1(params)                              # this should be of type rpc
    except grpc.RpcError:
            server_failure()
            return

    return

def connect_to_leader():
    # Issue a GetLeader command to find the current leader
    global server_ip_addr_port_num
    channel = grpc.insecure_channel(server_ip_addr_port_num)
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.Empty()
        response = stub.GetLeader(params)

        if response.nodeId != -1:
            # Update server_ip_addr_port_num to connect to the leader
            #global server_ip_addr_port_num
            server_ip_addr_port_num = response.nodeAddress
            print(f"Connected to leader at {server_ip_addr_port_num}")
        else:
            print("No leader available.")
            return False
    except grpc.RpcError:
        server_failure()
        return False

    return True


def nonsense(file_path):
    # Ensure you are connected to the leader
    if not connect_to_leader():
        print("Failed to connect to leader.")
        return

    # Read the file in binary mode
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
        print("checkpoint -1")
        channel = grpc.insecure_channel(server_ip_addr_port_num)
        print("checkpoint -2")
        stub = raft_pb2_grpc.RaftServiceStub(channel)
        print("checkpoint -3")
        # Use the file name as key and binary content as value
        params = raft_pb2.nonsenserequest(key=file_path, value=file_content)
        print("checkpoint -5")
        response = stub.nonsenseservice(params)
        print("checkpoint -4")
        if response.verdict:
            print("File sent successfully.")
        else:
            print("Failed to send the file.")
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except grpc.RpcError:
        server_failure()



# Issue a GetVal command to the server
def get_val(key):
    channel = grpc.insecure_channel(server_ip_addr_port_num)
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.GetValRequest(key=key)
        response = stub.GetVal(params)

        if response.verdict == False:
            print("None")
        else:
            print(response.value)
                    
    except grpc.RpcError:
            server_failure()
            return


def get_something_rajiv(key):
    channel = grpc.insecure_channel(server_ip_addr_port_num)
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.getrajivRequest(key=key)
        response = stub.getsome(params)

        try:
            #print(response.value)
            return response.value
        except:
            print("RAJIV")
                    
    except grpc.RpcError:
            server_failure()
            return
    

def get_something_rajiv1(key):
    channel = grpc.insecure_channel(server_ip_addr_port_num)
    stub = raft_pb2_grpc.RaftServiceStub(channel)

    try:
        params = raft_pb2.getrajivRequest1(key=key)
        response = stub.getsome1(params)

        if response.verdict == False:
            print("None")
        else:
            print(response.value)
                    
    except grpc.RpcError:
            server_failure()
            return

def terminate():
    print("The client ends")
    sys.exit(0)


def lms():



    return




# Initialize the client
def init():
    print("The client starts")

    while True:
        try:
            user_input = input(">")
            parsed_input = parse_user_input(user_input)

            message_type = parsed_input[0]

            if message_type == "Connect":
                connect(parsed_input[1])
            elif message_type == "GetLeader":
                get_leader()
            elif message_type == "Suspend":
                suspend(parsed_input[1])
            elif message_type == "SetVal":
                set_val(parsed_input[1], parsed_input[2])
            elif message_type == "GetVal":
                get_val(parsed_input[1])
            elif message_type == "Quit":
                terminate()
            elif message_type=="send":
                sendsomething(parsed_input[1],parsed_input[2])
            elif message_type=="needed":
                get_something_rajiv(parsed_input[1])
            elif message_type=="nonsense":
                nonsense(parsed_input[1])
            elif message_type=="lms":
                run()

            else:
                print("Invalid command! Please try again.")

        except KeyboardInterrupt:
            print("Use 'quit' to terminate the client program")

if __name__ == "__main__":
    init()