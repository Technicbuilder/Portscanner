import socket
import ipaddress

def verify_input(scanner):
    listed = scanner.instructions.split()

    if len(listed) != 4 or listed[0] != 'scan' or listed[2] != '-p':        #   verifys whether input matches format
        return 'Instruction unrecognised enter in format: scan 192.168.4.27/domain name -p 34-65635'

    address = listed[1]     #   singles out the IP address

    try:
        ipaddress.ip_address(address)   #   verifys ip address is a real address
        scanner.computers.append(address)
    except ValueError:

        try:
            new_ip = socket.gethostbyname(address)
            print(f'\nIP address {address} resolved to {new_ip}')
            print('')
            scanner.computers.append(new_ip)

        except socket.gaierror:
            return f'Invalid IP address {address}'

    try:
        ports = listed[3].split('-')

        if len(ports) != 2:
            return 'Invalid port range format. Use: START-END'

        scanner.start_port = int(ports[0])
        scanner.end_port = int(ports[1])

        if scanner.start_port < 1 or scanner.end_port > 65_535:
            return 'Ports must be in range 1 ---> 65,535'

        if scanner.start_port > scanner.end_port:
            return 'Start port must be less than or equal to the end port'

    except (ValueError, IndexError):
        return 'Invalid port range format. Use: START-END'

    if scanner.end_port - scanner.start_port + 1 > 50:
        accepted = False

        while not accepted:
            print('Scanning anything over 100ish ports will take some time')
            user_input = input('Do you understand [Y/n]?').lower()

            if user_input == 'y':
                accepted = True
            elif user_input == 'n':
                return 'cancel scan'
            else:
                print('Input not understood, please try again')
                print('Scanning anything over 50 ports will take some time')
                user_input = input('Do you understand [Y/n]?').lower()

    return True
