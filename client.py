from socket import *
import sys
import time
import os

# To start client: python3 TCPClient.py serverName serverPort
# Use LuciusdeMBP as test server and 5000 as test port
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
# Establish socket connection
clientSocket = socket(AF_INET, SOCK_STREAM) 
clientSocket.connect((serverName,serverPort)) 

if __name__ == '__main__':
    # Start
    print('-------------- Starting Client Socket --------------\n')
    while True:

        # Get the list of all files and directories
        path = "./image_send"
        dir_list = os.listdir(path)
        print("-------------- Available images to send are: --------------")
        print(dir_list)
        cmd = input('Please choose an image to send from the above options: \n') 

        # Send cmd and compute RTT/TPUT
        if cmd not in dir_list:
            print("Your input image is not in current folder. Please select from the available images!")
        else:
            image_file = open('./image_send/'+cmd, 'rb')
            image_data = image_file.read(400000000)
            # 1. compute RTT and throughput
            start_time = round(time.time() * 1000)
            clientSocket.send(image_data)
            sentenceRecv = clientSocket.recv(2048).decode()
            end_time = round(time.time() * 1000)
            RTT = end_time - start_time
            file_size = os.path.getsize('./image_send/'+cmd)
            throughput = file_size * 8 / RTT * 1000
            print("RTT in ms: ",RTT)
            print("File Size is : ", file_size, "bytes")
            print("Throughput is: ", throughput, "bps")
            print(sentenceRecv)
            
      #clientSocket.close() 




