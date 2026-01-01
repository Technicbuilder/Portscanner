import concurrent
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

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

        number_of_ports = self.end_port - self.start_port + 1
        print(f'Scanning ports [{self.start_port}] ---> [{self.end_port}]')     #   scans port ranges using the single
        time.sleep(1)                                                           #   port scanner function above

        if number_of_ports < 100:
            for host in self.computers:
                for port in range(int(self.start_port), int(self.end_port) + 1):
                    print(f'Scanning port: [{port}]')
                    self.scan(host, port)

        else:

            threads = min(100, number_of_ports)
            print('This may take dome time...')
            for host in self.computers:  # ADD loop over hosts for multithreading
                with ThreadPoolExecutor(max_workers=threads) as executor:  # multithreaded approach
                    scans = {
                        executor.submit(self.scan, host, port): port for port in range(self.start_port, self.end_port + 1)
                    }

                    for future in as_completed(scans):
                        port = scans[future]

                        try:
                            future.result()  # ensures exceptions in threads are caught

                        except Exception as e:
                            print(f'Error scanning port {port}: {e}')




