import socket


host = "127.0.0.1"
port = 7777


s = socket.socket()
s.connect((host, port))


while True:
    # received the banner
    data = s.recv(1024).decode().strip()
    # print banner
    print(data)
    
    if "Please enter your name:" in data:
        #getting name
        user_name = input("").strip()
        s.sendall(user_name.encode())
        continue
        
    if "Please enter a difficulty:" in data:
        #getting difficulty
        user_diff = input("").strip()
        s.sendall(user_diff.encode())
        continue
        
    if "Enter your guess:" in data:
        while True:
            #let get our input from the user
            user_input = input("").strip()
            s.sendall(user_input.encode())
            reply = s.recv(1024).decode().strip()
            if "Correct" in reply:
                print(reply)
                break
            print(reply)
        continue
    if 
        
s.close()

