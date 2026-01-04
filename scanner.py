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

    def scan_TCP(self, host, port, timeout=2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        try:
            result = sock.connect_ex((host, port))
            if result == 0:
                self.available_ports.append((port, 'tcp'))

                try:
                    sock.send(b'\r\n')
                    banner = sock.recv(1024).decode(errors='ignore').strip()

                    if banner:
                        self.services[(port, 'tcp')] = banner
                    else:
                        try:
                            self.services[(port, 'tcp')] = socket.getservbyport(port)

                        except:
                            self.services[(port, 'tcp')] = "Uknown Service"

                except:
                    try:
                        self.services[(port, 'tcp')] = socket.getservbyport(port)

                    except:
                        self.services[(port, 'tcp')] = 'Uknown Service'

        except socket.gaierror:
            return f'URL/IP {host} could not be resolved'

        except:
            pass

        finally:
            sock.close()

    def scan_UDP(self, host, port, timeout=2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)

        try:
            sock.sendto(b'', (host, port))
            sock.recvfrom(1024) #   if open
            self.available_ports.append((port, 'udp'))

            try:
                self.services[(port, 'udp')] = socket.getservbyport(port, 'udp')

            except:
                self.services[(port, 'udp')] = 'Uknown Service'

        except socket.timeout:
            pass    #   port has been opened or filtered

        except ConnectionRefusedError:
            pass    #   port closed

        finally:
            sock.close()


    def scan_range(self):

        number_of_ports = self.end_port - self.start_port + 1                   #   scans port ranges using the single
        if number_of_ports < 20:                                               #   port scanner function above
            for host in self.computers:
                for port in range(int(self.start_port), int(self.end_port) + 1):
                    self.scan_TCP(host, port)
                    self.scan_UDP(host, port)


        else:

            threads = min(500, number_of_ports)
            for host in self.computers:
                with ThreadPoolExecutor(max_workers=threads) as executor:
                    scans = {}

                    for port in range(self.start_port, self.end_port + 1):
                        scans[executor.submit(self.scan_TCP, host, port)] = port
                        scans[executor.submit(self.scan_UDP, host, port)] = port

                    for future in as_completed(scans):
                        port = scans[future]

                        try:
                            future.result()  # ensures exceptions in threads are caught

                        except Exception as e:
                            return f'Error scanning port {port}: {e}'
