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
            max_score = {"easy":(50), "medium":100, "hard": 200}[client_diff]
            while True:
                client_guess = conn.recv(1024)
                try:
                    guess = int(client_guess.decode().strip())
                    print(f"User guess attempt: {guess}")
                    if guess == guessme:
                        conn.sendall(b"Correct Answer!")
                        current_score = max_score
                        break
                    elif guess > guessme:
                        conn.sendall(b"Guess Lower!\nenter guess: ")
                        max_score -= 1
                        continue
                    elif guess < guessme:
                        conn.sendall(b"Guess Higher!\nenter guess:")
                        max_score -= 1
                        continue
                        
                except ValueError:
                    conn.sendall(b"Invalid input. Pleace enter a number.")
                    
                    
            try:
                f = open("scoreboard.txt", "r")
                lines = f.readlines()
                
            except FileNotFoundError:
                f = open("scoreboard.txt", "w")
                f.close()
                f = open("scoreboard.txt", "r")
                lines = f.readlines()
                
            lines.append(f"{client_name}, {client_diff}: {current_score}\n")
            lines.sort(key=lambda x: int(x.split(': ')[1]), reverse=True)
            
            f = open("scoreboard.txt", "w")
            f.writelines(lines)
            f.close()
            
            conn.sendall(b"Want to play again? [Yes/No]")
            client_again = conn.recv(1024).decode().strip().lower()
            
            if client_again == "yes":
                client_diff = None
                continue
                
            if client_again == "no":
                conn.sendall(b"Breaking Connection...")
                conn.close()
                conn = None
                f = open("scoreboard.txt", "r")
                scoreboard_contents = f.read()
                f.close()
                print(scoreboard_contents)
                break
            else:
                conn.sendall(b"Invalid Input. Want to play again?[Yes/No]")
    

