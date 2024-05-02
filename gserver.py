import socket
import random 

host = "localhost"
port = 7777

intro_banner = """
Welcome to the Guessing Game 1.0!
Please enter your name: 
"""

diff_banner="""
[]Easy
[]Medium
[]Hard
Please enter a difficulty:
"""

guess_banner = """
== Guessing Game v1.0 ==
Enter your guess:"""

def generate_random_int(low, high):
    return random.randint(low, high)

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print(f"server address is {socket.gethostbyname(host)}")
print(f"server is listening in port {port}")

guessme = 0
conn = None

while True:
    if conn is None:
        print("waiting for connection..")
        conn, addr = s.accept()
        print(f"new client: {addr[0]}")
        
    else:        
        conn.sendall(intro_banner.encode())
        client_name = conn.recv(1024).decode().strip().upper()
        
        while client_name:
            #Setting the difficulty
            conn.sendall(diff_banner.encode())
            client_diff = conn.recv(1024).decode().strip().lower()
            
            if client_diff not in("easy", "medium", "hard"):
                conn.sendall(b"Invalid difficulty choice. Please choose again.")
                continue
                
            #Setting the values
            low, high = {"easy":(1,50), "medium":(1,100), "hard":(1,500)}[client_diff] #Based on difficulty given
            guessme = generate_random_int(low,high)
            print(f"User difficulty choice: {client_diff}")
            
            #Setting client guess
            conn.sendall(guess_banner.encode())
            # cheat_str = f"==== number to guess is {guessme} \n" + banner 
            # conn.sendall(cheat_str.encode())
            
            while True:
                client_guess = conn.recv(1024)
                try:
                    guess = int(client_guess.decode().strip())
                    print(f"User guess attempt: {guess}")
                    
                    if guess == guessme:
                        conn.sendall(b"Correct Answer!")
                        conn.close()
                        conn = None
                        continue
                    elif guess > guessme:
                        conn.sendall(b"Guess Lower!\nenter guess: ")
                        continue
                    elif guess < guessme:
                        conn.sendall(b"Guess Higher!\nenter guess:")
                        continue
                        
                except ValueError:
                    conn.sendall(b"Invalid input. Pleace enter a number.")



