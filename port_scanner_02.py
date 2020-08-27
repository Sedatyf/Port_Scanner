import socket
import threading
import termcolor
import progressbar
import sys
import os
from datetime import datetime

# Global variables
n_threads = 20
is_port_found = False
bar = None

# Class for multithreading
class JudgeThread(threading.Thread):
    def __init__(self, threadIndex, remote_addr, *port):
        threading.Thread.__init__(self)
        self.index = threadIndex
        self.addr = remote_addr
        self.ports = port

    # run() method for multithreading
    # it contains port scanner itself
    def run(self):
        # As range is exclusive, we need to add 1 to the second arguments value
        port_start = self.ports[0]
        port_end = self.ports[1] + 1
        global is_port_found

        socket.setdefaulttimeout(0.05)

        for port in range(port_start, port_end):
            # If port modulo n_threads equals the thread index, then give it all task below.
            # For example, if n_threads == 20 then thread 0 will have port 0, port 20, port 40, and so on.
            if port % n_threads == self.index:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((self.addr, port))
                bar.update(port + 1)
                if result == 0:
                    text = f"[*] Port {port}"
                    space = 18 - len(text)
                    # Format and regex to have all "Open" right aligned whatever the port length is
                    f = '{0}: {1:>%d}' % (space)
                    termcolor.cprint(f.format(text, "Open"), "green")
                    is_port_found = True


def scan(remote_addr, *port):
    port_start = 1
    port_end = 65535
    global bar

    # Mandatory list for the multithreading
    spawned_threads = []

    if len(port) == 1:
        port_end = int(port[0]) + 1
        port_start = int(port[0])
    elif len(port) == 2:
        port_start = int(port[0])
        port_end = int(port[1]) + 1

    # This is options to show on the progress bar
    widgets = [progressbar.FormatCustomText(
        "Scanning "), progressbar.Percentage(), progressbar.Bar("■"), progressbar.ETA()]
    bar = progressbar.ProgressBar(
        widgets=widgets, max_value=port_end, redirect_stdout=True).start()

    # This block creates n threads by instancing JudgeThread class. 
    # Then it calls start() which is starting thread and calling run() function
    try:
        for i in range(n_threads):
            t = JudgeThread(i, remote_addr, port_start, port_end-1)
            t.start()
            spawned_threads.append(t)
        for t in spawned_threads:
            t.join()
    except KeyboardInterrupt:
        termcolor.cprint(
            "You pressed Ctrl+C, interrupting process...", "yellow")
        sys.exit()
    except socket.gaierror:
        termcolor.cprint("Hostname could not be resolved. Exiting", "red")
        sys.exit()
    except socket.error:
        termcolor.cprint("Couldn't connect to server. Exiting", "red")
        sys.exit()

    if not is_port_found:
        termcolor.cprint("None of the provided ports are open", "red")

# Usage definition
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
    t1 = datetime.now()

    # If arguments after argument 0 startswith "-" then its an option call and goes on the opts list
    # If not, then it's an argument that goes in the args list
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    if not opts:
        show_help()
        sys.exit()

    if "-h" in opts:
        show_help()
        sys.exit()
    else:
        remote_server_ip = socket.gethostbyname(args[0])

        # Printing a nice banner
        print("-" * 60)
        print("Please wait, scanning remote host " + remote_server_ip)
        print("-" * 60)

    # if statement to call functions with good options
    # Also checking if user provided good amount of arguments
    if "-p" in opts:
        if len(args) == 2:
            scan(remote_server_ip, args[1])
        else:
            termcolor.cprint(
                "You need to enter a digit to specify your port", "red")
    elif "-r" in opts:
        if len(args) == 3:
            scan(remote_server_ip, args[1], args[2])
        else:
            termcolor.cprint(
                "You need to enter two digits to specify range", "red")
    elif "-a" in opts:
        scan(remote_server_ip)
    else:
        raise SystemExit(show_help())

    # Closing the progress bar
    bar.finish()

    t2 = datetime.now()
    print("Scanning Completed in " + str(t2-t1))


if __name__ == "__main__":
    main()
