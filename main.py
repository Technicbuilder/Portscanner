from scanner import PortScanner
from clean_input import verify_input

print('Welcome to Port Scanner')
print('Please enter the host you want to scan, followed by the port you want to scan, observe this example below')
print('scan (IP address or Domain name) -p 34-65635   | or for one port | scan 192.168.4.27 -p 34-34 ')

user_input = input('\n>>>> ')

scanner = PortScanner()
scanner.instructions = user_input
result = verify_input(scanner)

while result == 'cancel scan':
    print('\nPlease enter your scan command again:')
    user_input = input('')
    scanner = PortScanner()
    scanner.instructions = user_input
    result = verify_input(scanner)

if result == True:
    print(f'Scanning ports [{scanner.start_port}] ---> [{scanner.end_port}]')
    total_ports = scanner.end_port - scanner.start_port
    if total_ports > 5000:
        print('This may take some time...')
    scanner.scan_range()
    print(f"\n\n[SCAN COMPLETE] Port status:")

    if scanner.available_ports:
        for port in scanner.available_ports:
            print(f"[PORT {port}]: [AVAILABLE]✅ - [SERVICE: {scanner.services[port]}]")
    else:
        print("No open ports available")
else:
    print(result)

