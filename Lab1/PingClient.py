import time
from socket import *
import sys
from datetime import datetime

ping_time = 20
TIMEOUT = 1

def main():
    server = sys.argv[1]
    port = sys.argv[2]
    RTTs = []
    RTT_succ = 0
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    
    local_addr = ('localhost', 5920)
    
    clientSocket.bind(local_addr)
    clientSocket.settimeout(TIMEOUT)

    count = 0
    while count <= ping_time:
        count += 1
        time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        buf = f"PING {int(port) + count} {time_stamp} \r\n".encode()
        receive_addr = (server, int(port))

        try:
            clientSocket.sendto(buf, receive_addr)
            t1 = int(time.time() * 1000)

            data, server_address = clientSocket.recvfrom(1024)
            t2 = int(time.time() * 1000)

            RTTs.append(t2 - t1)
            RTT_succ += 1
            print(f"ping to {server}, seq = {count + int(port)}, rtt = {t2 - t1} ms")
        except timeout:
            print(f"ping to {server}, seq = {count + int(port)}, time out")

    clientSocket.close()

    if RTT_succ != 0:
        min_rtt = min(RTTs)
        max_rtt = max(RTTs)
        avg_rtt = round(sum(RTTs) / RTT_succ, 2)
        print(f"Minimum RTT: {min_rtt} ms, Maximum RTT: {max_rtt} ms, Average RTT: {avg_rtt} ms")

if __name__ == "__main__":
    main()