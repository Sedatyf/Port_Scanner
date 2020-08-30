# Port_Scanner
This script scans port from a remote host address. You can specify directly an IP address or you can provide a website link such as www.google.com. 
You can choose between options like scan one port, scan a range of ports, or scan all ports from the remote address. 

**Made with Python 3.8.5 so it's working on Python 3**

### Module in script
``socket``, ``threading``, ``termcolor``, ``progressbar``, ``sys``, ``os``, ``datetime``.

### Usage
```bash
python3 port_scanner_02.py www.google.com -a
python3 port_scanner_02.py www.google.com -r 1 1500
python3 port_scanner_02.py www.google.com -p 80
```
Please refer to the usage print with
```bash
python3 port_scanner_02.py -h
```

### Legal notices

As the Nmap's legal page said : "The legal ramifications of scanning networks with Nmap [author's note: or any tool] are complex and so controversial that third-party 
organizations have even printed T-shirts and bumper stickers promulgating opinions on the matter".

However – while not explicitly illegal – port and vulnerability scanning without permission can get you into trouble:
  - The owner of a scanned system can sue the person who performed the scan. Even if unsuccessful, the case can waste time and resources on legal costs
  - The owner of a scanned system can report the scanner’s IP to the associated ISP. 
  Many ISPs prohibit unauthorized port scanning. Some will take action – such as with reprimands or canceling of service
  
**With that said, I cannot be made responsible if you have any problems after using this tool.**
So use it with cautions or (this is better) with authorization from the owner's scanned device.
