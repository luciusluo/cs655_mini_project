- cs655_mini_project

- Steps to test the transmissions through ssh:

1. Use ssh to login to server node and leave the terminal open. 
   (The server.py is already running nohup in the background and listening on port 5001. So there's no need to run another server.py)
2. Use ssh to login to any client node
   1. Run command
      ```python
      cd cs655_mini_project
      python3 client.py server1.yuxiaominiproject.ch-geni-net.instageni.sox.net 5001
      ```
   2. Choose image to classify by inputing the name of the images from available options, i.e., ```hamster.jpeg```
   3. The prediction will be sent back and displayed on client's temrinal. 
