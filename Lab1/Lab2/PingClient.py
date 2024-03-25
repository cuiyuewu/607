# Python version 3.6.5

from socket import *
from datetime import datetime
import time
import sys
serverIP = '127.0.0.1'
serverPort = sys.argv[2]
# create an UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
addr = (serverIP, serverPort)

list_rtts = []
packets_lost = 0

for i in range(10):
    time_stamp = datetime.now().isoformat(sep = ' ')[:-3]
    # the message to be sent to the server
    ping_message = "PING" + str(i) + ' ' + time_stamp + '\r\n'
    # time when the message is sent
    time_send = datetime.now()
    # send the message
    clientSocket.sendto(ping_message.encode(), addr)

    try:
        clientSocket.settimeout(1)
        response, serverAddress = clientSocket.recvfrom(1024)
        # time when the message is received by client
        time_receive = datetime.now()

        rtt = round((time_receive - time_send).total_seconds() * 1000)

        list_rtts.append(rtt)

        print(f"ping to {serverIP}, seq = {i}, rtt = {rtt} ms")

        clientSocket.settimeout(None)

    except timeout:
        # the client does not receive any reply from the server
        packets_lost += 1
        print(f'ping to {serverIP}, seq = {i}, rtt = time out')

# print report about the min, max, average RTT and packets loss ratio.
print("\n")
print(f'Minimum RTT = {min(list_rtts)} ms')
print(f'Maximum RTT = {max(list_rtts)} ms')
print(f'Average RTT = {round(float(sum(list_rtts) / len(list_rtts)))} ms')
print(f'{float(packets_lost) / 10 * 100}% of packets have been lost through the network')
clientSocket.close()






