import socket
import time

class PortScanner:
    def __init__(self):
        self.computers = []
        self.start_port = 0
        self.end_port = 0
        self.available_ports = []
        self.instructions = ''
        self.services = {}


    def scan(self, host, port, timeout = 0.1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #   scans the port determining whether its
        sock.settimeout(timeout)                                    #   available or not

        try:
            if sock.connect_ex((host, port)) == 0:
                self.available_ports.append(port)

            try:
                service_name = socket.getservbyport(port)
                self.services[port] = service_name
            except:
                self.services[port] = "Unknown Service"

        finally:
            sock.close()

    def scan_range(self):
        print(f'Scanning ports [{self.start_port}] ---> [{self.end_port}]')     #   scans port ranges using the single
        time.sleep(1)                                                           #   port scanner function above
        for host in self.computers:
            for port in range(int(self.start_port), int(self.end_port) + 1):
                print(f'Scanning port: [{port}]')
                self.scan(host, port)
