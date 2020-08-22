import socket
import termcolor, tqdm
import sys, os
from datetime import datetime

def scan(remote_addr, *port):
    t1 = datetime.now()
    start = 0
    end = 65535
    is_port_found = False
    port_found = []

    if len(port) == 1:
        end = int(port[0]) + 1
        start = int(port[0])
    elif len(port) == 2:
        start = int(port[0])
        end = int(port[1]) + 1

    try:
        progress_bar = tqdm.tqdm(range(start, end))
        socket.setdefaulttimeout(0.05)
        for port in progress_bar:
            progress_bar.set_description("Scanning")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remote_addr, port))
            if result == 0:
                port_found.append(port)
                is_port_found = True
            else:
                is_port_found = False
            sock.close()
    except KeyboardInterrupt:
        termcolor.cprint("You pressed Ctrl+C, interrupting process...", "yellow")
        sys.exit()
    except socket.gaierror:
        termcolor.cprint("Hostname could not be resolved. Exiting", "red")
        sys.exit()
    except socket.error:
        termcolor.cprint("Couldn't connect to server. Exiting", "red")
        sys.exit()

    if is_port_found:
        for port in port_found:
            text = f"[*] Port {port}"
            space = 18 - len(text)
            f = '{0}: {1:>%d}' % (space)
            termcolor.cprint(f.format(text, "Open"), "green")
    else:
        termcolor.cprint("None of the provided ports are open", "red")
    
    t2 = datetime.now()
    print("Scanning Completed in " + str(t2-t1))

def show_help():
    print(f"""Port Scanner
    Usage:
      {os.path.basename(__file__)} <remote_address> -p <port>
      {os.path.basename(__file__)} <remote_address> -r <start> <end>
      {os.path.basename(__file__)} <remote_address> -a 
      {os.path.basename(__file__)} -h

    Options:
      -h    Show this screen.
      -p    Scan one specific port
      -r    Scan a range of specific ports
      -a    Scan all ports
    """)

def main():
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    if "-h" in opts:
        show_help()
        sys.exit()
    else:
        remote_server_ip = socket.gethostbyname(args[0])
        print("-" * 60)
        print("Please wait, scanning remote host " + remote_server_ip)
        print("-" * 60)

    if "-p" in opts:
        if len(args) == 2:
            scan(remote_server_ip, args[1])
        else:
            termcolor.cprint("You need to enter a digit to specify your port", "red")
    elif "-r" in opts:
        if len(args) == 3:
            scan(remote_server_ip, args[1], args[2])
        else:
            termcolor.cprint("You need to enter two digits to specify range", "red")
    elif "-a" in opts:
        scan(remote_server_ip)
    else:
        raise SystemExit(show_help())

if __name__ == "__main__":
    main()