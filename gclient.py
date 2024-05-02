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
        while not "Correct Answer!" in data
            #let get our input from the user
            user_input = input("").strip()
            s.sendall(user_input.encode())
            continue
        break
        
s.close()

