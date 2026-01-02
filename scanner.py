import concurrent
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class PortScanner:
    def __init__(self):
        self.computers = []
        self.start_port = 0
        self.end_port = 0
        self.available_ports = []
        self.instructions = ''
        self.services = {}

    def scan(self, host, port, timeout=0.1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        try:
            result = sock.connect_ex((host, port))
            if result == 0:
                self.available_ports.append(port)

                try:
                    sock.send(b'\r\n')
                    banner = sock.recv(1024).decode(errors='ignore').strip()

                    if banner:
                        self.services[port] = banner
                    else:
                        try:
                            self.services[port] = socket.getservbyport(port)

                        except:
                            self.services[port] = "Uknown Service"

                except:
                    try:
                        self.services[port] = socket.getservbyport(port)

                    except:
                        self.services[port] = 'Uknown Service'

        except socket.gaierror:
            return f'URL/IP {host} could not be resolved'

        except:
            pass

        finally:
            sock.close()

    def scan_range(self):

        number_of_ports = self.end_port - self.start_port + 1                   #   scans port ranges using the single
        if number_of_ports < 100:                                               #   port scanner function above
            for host in self.computers:
                for port in range(int(self.start_port), int(self.end_port) + 1):
                    self.scan(host, port)

        else:

            threads = min(100, number_of_ports)
            for host in self.computers:
                with ThreadPoolExecutor(max_workers=threads) as executor:  # multithreaded approach if number of ports to be scanned is > 100
                    scans = {
                        executor.submit(self.scan, host, port): port for port in range(self.start_port, self.end_port + 1)
                    }

                    for future in as_completed(scans):
                        port = scans[future]

                        try:
                            future.result()  # ensures exceptions in threads are caught

                        except Exception as e:
                            return f'Error scanning port {port}: {e}'



