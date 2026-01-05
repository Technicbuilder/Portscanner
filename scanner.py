import concurrent
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import datetime

class PortScanner:
    def __init__(self):
        self.computers = []
        self.start_port = 0
        self.end_port = 0
        self.available_ports = []
        self.instructions = ''
        self.services = {}
        self.payloads = self.payload('udp_payload.json')

    def payload(self, file):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                formatted_payload = {int(k): bytes.fromhex(v) for k, v in data.items()}
                return formatted_payload

        except FileNotFoundError:
            print('udp_payload.json not found')
            return {}

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
        message = self.payloads.get(port, b'hello')

        try:
            sock.sendto(message, (host, port))
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


    def output_results(self):
        data_to_output = {
            f'SCAN: {datetime.datetime.now().strftime("%m/%d/%Y %H")}': {
                'host': self.computers,
                'number of open ports': len(self.available_ports),
                'open ports': self.available_ports,
                'service_details': {f'{port, protocol}': service for (port, protocol), service in self.services.items()}
            }
        }
        try:
            with open('scanner-results.json', 'w') as f:
                json.dump(data_to_output, f, indent=4)

        except Exception as e:
            print(f'Error writing results to scanner-results.json: {e}')



