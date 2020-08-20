import socket
import termcolor

remote_server = input("Enter a remote host to scan: ")

def scan(*port):
    start = 0
    end = 65535
    is_port_found = []
    
    if len(port) == 1:
        end = int(port[0]) + 1
        start = int(port[0])
    elif len(port) == 2:
        start = int(port[0])
        end = int(port[1]) + 1
    
    for port in range(start, end):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remote_server, port))
        if result == 0:
            text = f"[*] Port {port}"
            space = 18 - len(text)
            f = '{0}: {1:>%d}' % (space)
            termcolor.cprint(f.format(text, "Open"), "green")
            is_port_found.append(True)
        else:
            is_port_found.append(False)
        sock.close()
    
    if not True in is_port_found:
        print("None of your ports is open")

def main():
    quit = 0
    while quit == 0:
        print("""Do you want to:
        \t1) Scan one specific port
        \t2) Scan a range of port
        \t3) Scan all ports
        \t4) Exit""")

        user_input = input()
        try:
            user_choice = int(user_input)
        except ValueError:
            termcolor.cprint("You need to choose between options by typing the corresponding number", "white", "on_red")
            continue
        else:
            if user_choice == 1:
                port = input("What port do you want to scan? ")
                if port.isdigit():
                    scan(port)
                    quit = 1
                else:
                    termcolor.cprint("You need to enter a digit to specify your port", "red")
            elif user_choice == 2:
                port1 = input("Specify start: ")
                port2 = input("Specify end: ")
                if port1.isdigit() and port2.isdigit():
                    scan(port1, port2)
                    quit = 1
                else:
                    termcolor.cprint("You need to enter two digits to specify range", "red")
            elif user_choice == 3:
                scan()
                quit = 1
            elif user_choice == 4:
                print("Exit")
                quit = 1
            else:
                termcolor.cprint("\nYou need to choose between options by typing 1,2 or 3\n", "red")

if __name__ == "__main__":
    main()

#remote_serverIP = socket.gethostbyname(remote_server)