import socket
import time
import argparse

def tcp_traffic(target_ip, target_port, duration, message_size, rate_mbps):
    message = b'x' * message_size
    end_time = time.time() + duration
    bytes_per_second = (rate_mbps * 1_000_000) // 8
    messages_per_second = bytes_per_second // message_size
    delay = 1 / messages_per_second

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((target_ip, target_port))
        print(f"Sending TCP traffic to {target_ip}:{target_port} at {rate_mbps} Mbps")
        while time.time() < end_time:
            start_time = time.time()
            s.sendall(message)
            elapsed_time = time.time() - start_time
            sleep_time = delay - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)
        print("TCP traffic generation completed.")

def udp_traffic(target_ip, target_port, duration, message_size, rate_mbps):
    message = b'x' * message_size
    end_time = time.time() + duration
    bytes_per_second = (rate_mbps * 1_000_000) // 8
    messages_per_second = bytes_per_second // message_size
    delay = 1 / messages_per_second

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        print(f"Sending UDP traffic to {target_ip}:{target_port} at {rate_mbps} Mbps")
        while time.time() < end_time:
            start_time = time.time()
            s.sendto(message, (target_ip, target_port))
            elapsed_time = time.time() - start_time
            sleep_time = delay - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)
        print("UDP traffic generation completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Traffic Generator")
    parser.add_argument("protocol", choices=["tcp", "udp"], help="Protocol to use (tcp or udp)")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("target_port", type=int, help="Target port number")
    parser.add_argument("duration", type=int, help="Duration of the test in seconds")
    parser.add_argument("message_size", type=int, help="Size of each message in bytes")
    parser.add_argument("rate_mbps", type=int, help="Rate of traffic in Mbps")
    
    args = parser.parse_args()
    
    if args.protocol == "tcp":
        tcp_traffic(args.target_ip, args.target_port, args.duration, args.message_size, args.rate_mbps)
    elif args.protocol == "udp":
        udp_traffic(args.target_ip, args.target_port, args.duration, args.message_size, args.rate_mbps)





#note
#python dtg.py tcp 192.168.1.10 5001 30 1024 100
#This command will send TCP traffic to 192.168.1.10 on port 5001 for 30 seconds with a message size of 1024 bytes at a rate of 100 Mbps.
