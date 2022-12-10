import socket
import threading
import time
import sys
import os
import io
import PIL.Image as Image
from torchvision import models
import torch
#import cv2
#from keras.preprocessing import image
#from keras.applications import vgg16
import numpy as np
from torchvision import transforms
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import select
import PIL

transform = transforms.Compose([               #[1]
    transforms.Resize(256),                    #[2]
    transforms.CenterCrop(224),                #[3]
    transforms.ToTensor(),                     #[4]
    transforms.Normalize(                      #[5]
    mean=[0.485, 0.456, 0.406],                #[6]
    std=[0.229, 0.224, 0.225]                  #[7]
    )])

alexnet = models.alexnet(pretrained=True)
with open('imagenet_classes.txt') as f:
    labels = [line.strip() for line in f.readlines()]


def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    print(tensor.shape)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return Image.fromarray(tensor, mode="L")


def predict(image):
    img_t = transform(image)
    batch_t = torch.unsqueeze(img_t, 0)
    alexnet.eval()
    out = alexnet(batch_t)

    '''
    print(img_t.shape)
    print(batch_t.shape)

    reversed_img = tensor_to_image(img_t)
    reversed_img.show()
    reversed_img.save('./image_recv/images.jpeg')
    '''

    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    _, indices = torch.sort(out, descending=True)
    results = [(labels[idx], percentage[idx].item()) for idx in indices[0][:5]]
    best_pred = results[0][0]
    print(results)
    return best_pred


def handle_client(client_socket, address):
    print(f'Server connected to {address}')
    while True:
        client_socket.setblocking(0)
        ready = select.select([client_socket], [], [], 20)
        image_bytes = None
        if ready[0]:
            try:
                image_bytes = client_socket.recv(400000000)
                #print(f'Receive an image from Client {address}' )
            #file = open('./image_recv/images.jpeg', 'wb')
            #file.write(image)
            except socket.error as e:
                print(f'Client {address} forcibly disconnected with {e}.')
                client_socket.close()
                break
        if image_bytes is not None:
            #print(image_bytes)
            im_BytesIO = io.BytesIO(image_bytes)
            im_BytesIO.seek(0)
            try:
                image = Image.open(im_BytesIO)
            except PIL.UnidentifiedImageError:
                #image_bytes = None
                continue
            print(f'Receive an image from Client {address}')
            best_pred = predict(image)
            image_bytes = None
            client_socket.send(bytes("Received image! The best prediction is: " + best_pred, encoding="utf-8"))
            #image_array = image.img_to_array(image_bytes)
            #print(image)            



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <serverPort>')
        sys.exit()

    # Socket init
    PORT = sys.argv[1]
    server_socket = socket.socket()
    server_socket.bind((socket.gethostname(), int(PORT)))
    print(socket.gethostname())
    server_socket.listen(32)
    print(f'Server listening on port {PORT}.')

    while True:
        try:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_client, args=(
                client_socket, address)).start()
        except KeyboardInterrupt:
            break
