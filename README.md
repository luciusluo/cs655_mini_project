- cs655_mini_project

- Steps to test the transmissions through ssh:

1. Use ssh to login to server node and leave the terminal open. 
   (The server.py is already running nohup in the background and listening on port 5001. So there's no need to run another server.py)
2. Use ssh to login to any client node
   1. Run command
      ```python
      python3 client.py server1.yuxiaominiproject.ch-geni-net.instageni.sox.net 5001
      ```
   3. 
